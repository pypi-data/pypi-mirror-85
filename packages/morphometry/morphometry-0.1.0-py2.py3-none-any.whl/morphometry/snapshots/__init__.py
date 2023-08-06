import os
import re
import sys
import math
import glob
import string
import random
import shutil
import logging
import numpy as np
import nibabel as nib
import tempfile as tf
import subprocess as sp
import morphometry.freesurfer as fs
from retry import retry
from natsort import natsorted
from PIL import Image, ImageDraw, ImageFont
from .. import commons

logger = logging.getLogger(__name__)

DIR = os.path.dirname(__file__)

class Snapshotter(object):
    def __init__(self, d, headless=True):
        '''
        :param d: FreeSurfer output directory
        :type d: str
        :param headless: Render snapshots without a display
        :type headless: bool
        '''
        self.d = d
        self.headless = headless
        self.xvfb = commons.which('xvfb-run')
        self.freeview = commons.which('freeview')
        self.output_dir = os.path.join(d, 'snapshots')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _mosaic(self, expr, saveas, size=(5,3)):
        mosaic_w, mosaic_h = size
        files = natsorted(glob.glob(expr))
        tile_w, tile_h = Image.open(files[0]).size
        new = Image.new('RGB', (tile_w * mosaic_w, tile_h * mosaic_h))
        pos_x,pos_y = 0,0
        for f in files:
            tile = Image.open(f)
            new.paste(tile, (pos_x * tile_w, pos_y))
            pos_x += 1
            if pos_x == mosaic_w:
                pos_y += tile_h
                pos_x = 0
        new.save(saveas)

    def _caption(self, expr):
        '''
        Add caption to input file
        '''
        files  = glob.glob(expr)
        for f in files:
            z = re.match('.*_slice-(\d+)', f).group(1)
            caption = 'z={0}'.format(z)
            img = Image.open(f)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            _,text_h = draw.textsize(caption, font)
            img_w,img_h = img.size
            pad = 3
            draw.text((pad, (img_h - text_h) - pad), caption, (255,255,255))
            img.save(f)

    def _crop(self, expr, size=None, pad=None):
        '''
        Crop images captured by the passed in glob expression 
        expr. The cropped image will be centered within a black 
        image of specified (width, height). If no size is passed 
        in by the user, images will be cropped and re-centered to 
        the size of the image with the most content. Deciding what 
        is "content" and what isn't is done by converting the image 
        to greyscale, then mapping pixels greater than 20 to white 
        and everything else to black. This tends to eliminate most 
        of the noise but preserves the image.
        '''
        if not size:
            w,h = self._maxsize(expr)
        else:
            w,h = size
        if pad:
            w = w + pad
            h = h + pad
        for f in glob.glob(expr):
            im = Image.open(f)
            im_ = im.convert('L')
            im_ = im_.point(lambda p: p > 20 and 255)
            bbox = im_.getbbox()
            im = im.crop(bbox)
            x,y = im.size
            im2 = Image.new('RGB', (w,h), (0,0,0,0))
            im2.paste(im, (int((w-x) / 2), int((h-y) / 2)))
            base,ext = os.path.splitext(f)
            saveas = '{0}_crop{1}'.format(base, ext)
            logger.info('saving cropped image: %s', saveas)
            im2.save(saveas)

    def _maxsize(self, expr):
        '''
        Return the maximum bounding box surrounding a set of images 
        sitting against a (mostly) black background. The images are 
        first converted to grayscale, then all pixels greater than 20 
        are set to white and everything else to black.

        :param expr: A glob expression of files to include
        :type expr: str
        '''
        maxarea = 0
        maximg = None
        maxbb = (0,0)
        logger.info('_maxsize glob expression: %s', expr)
        for f in glob.glob(expr):
            im = Image.open(f)
            im_ = im.convert('L')
            im_ = im_.point(lambda p: p > 20 and 255)
            bbox = im_.getbbox()
            w,h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            area = w * h
            if area > maxarea:
                maximg = f
                maxarea = area
                maxbb = bbox
        w,h = maxbb[2] - maxbb[0], maxbb[3] - maxbb[1]
        return w,h

    @retry(tries=5)
    def run_freeview(self, preamble, slices, verify=None):
        if not verify:
            verify = list()
        # write command to file
        with tf.NamedTemporaryFile(suffix='.txt', prefix='freeview') as fo:
            logger.debug('writing temporary freeview file %s', fo.name)
            fo.write((sp.list2cmdline(preamble) + os.linesep).encode())
            for s in slices:
                fo.write((sp.list2cmdline(s) + os.linesep).encode())
            fo.write(('-quit' + os.linesep).encode())
            with open(fo.name) as f:
                print(f.read())
            fo.flush()
            cmd = [
                self.xvfb,
                'freeview',
                '-cmd', fo.name
            ]
            logger.info(sp.list2cmdline(cmd))
            self.check_output(cmd)
        for f in verify:
            if not os.path.exists(f):
                raise FileNotFoundError(f)

    def check_output(self, cmd):
        try:
            sp.check_output(cmd, stderr=sp.PIPE)
        except sp.CalledProcessError as e:
            stderr = e.stderr.decode() if e.stderr else ''
            if e.returncode == 1 and 'No such process' in stderr:
                logger.debug("ignoring xvfb-run kill 'No such process' error")
            else:
                raise e

    def aseg(self, size=(5,3)):
        img = os.path.join(self.d, 'mri', 'aparc+aseg.mgz')
        aseg = os.path.join(self.d, 'mri', 'aparc+aseg.mgz')
        x,y,z = nib.load(img).shape
        tiles = size[0] * size[1]
        top,bottom = self.bounds(aseg, axis=1)
        step = math.ceil((bottom - top) / tiles)
        logger.info('aseg top=%s, bottom=%s, step=%s', top, bottom, step)
        # build and execute freeview command
        asegv = '{0}:colormap=lut:opacity=0.4'.format(
            os.path.join(self.d, 'mri', 'aparc+aseg.mgz')
        )
        preamble = [
            'freeview',
            '-v', os.path.join(self.d, 'mri', 'T1.mgz'),
            '-v', asegv,
            '-layout', '1',
            '-cc',
            '-nocursor',
            '-viewsize', str(x), str(y)
        ]
        slices = list()
        output_files = list()
        for i in range(top, bottom + 1, step):
            saveas = os.path.join(
                self.output_dir,
                'img-aseg_axis-axial_slice-{0}.png'.format(i)
            )
            cmd = [            
                '-viewport', 'axial',
                '-slice', str(int(x / 2)), str(i), str(int(z / 2)),
                '-ss', saveas,
                '-noquit'
            ]
            slices.append(cmd)
            output_files.append(saveas)
        self.run_freeview(preamble, slices, verify=output_files)
        # check for all expected output files
        for f in output_files:
            if not os.path.exists(f):
                raise FileNotFoundError(saveas)
        # remove previously cropped images
        expr = os.path.join(self.output_dir, 'img-aseg_axis-axial_slice-*_crop.png')
        for f in glob.glob(expr):
            os.remove(f) 
        # crop derived images
        expr = os.path.join(self.output_dir, 'img-aseg_axis-axial_slice-*.png')
        self._crop(expr, pad=10)
        # add slice number caption to cropped images
        expr = os.path.join(self.output_dir, 'img-aseg_axis-axial_slice-*_crop.png')
        self._caption(expr)
        # create mosaic from captioned cropped images
        saveas = os.path.join(self.output_dir, 'img-aseg_axis-axial_mosaic.png')
        self._mosaic(expr, saveas=saveas, size=size)

    def surfaces(self, size=(5,3)):
        brainmask = os.path.join(self.d, 'mri', 'brainmask.mgz')
        rh_white = os.path.join(self.d, 'surf', 'rh.white')
        rh_pial = os.path.join(self.d, 'surf', 'rh.pial')
        lh_white = os.path.join(self.d, 'surf', 'lh.white')
        lh_pial = os.path.join(self.d, 'surf', 'lh.pial')
        x,y,z = nib.load(brainmask).shape
        tiles = size[0] * size[1]
        top,bottom = self.bounds(brainmask, axis=1)
        step = math.ceil((bottom - top) / tiles)
        logger.info('aseg top=%s, bottom=%s, step=%s', top, bottom, step)
        # build and execute freeview command
        preamble = [
            'freeview',
            '-v', os.path.join(self.d, 'mri', 'T1.mgz'),
            '-f',
            '{0}:edgecolor=cyan:edgethickness=2'.format(lh_pial),
            '{0}:edgecolor=yellow:edgethickness=2'.format(lh_white),
            '{0}:edgecolor=magenta:edgethickness=2'.format(rh_pial),
            '{0}:edgecolor=lime:edgethickness=2'.format(rh_white),
            '-layout', '1',
            '-cc',
            '-nocursor',
            '-viewsize', str(x), str(y)
        ]
        slices = list()
        output_files = list()
        for i in range(top, bottom + 1, step):
            saveas = os.path.join(
                self.output_dir,
                'img-surf_axis-axial_slice-{0}.png'.format(i)
            )
            cmd = [
                '-viewport', 'axial',
                '-slice', str(int(x / 2)), str(i), str(int(z / 2)),
                '-ss', saveas,
                '-noquit'
            ]
            slices.append(cmd)
            output_files.append(saveas)
        self.run_freeview(preamble, slices, verify=output_files)
        # remove previously cropped images
        expr = os.path.join(self.output_dir, 'img-surf_axis-axial_slice-*_crop.png')
        for f in glob.glob(expr):
            os.remove(f)
        # crop derived images
        expr = os.path.join(self.output_dir, 'img-surf_axis-axial_slice-*.png')
        self._crop(expr, pad=10)
        # add slice number caption to cropped images
        expr = os.path.join(self.output_dir, 'img-surf_axis-axial_slice-*_crop.png')
        self._caption(expr)
        # create mosaic from captioned cropped images
        saveas = os.path.join(self.output_dir, 'img-surf_axis-axial_mosaic.png')
        self._mosaic(expr, saveas=saveas, size=size)

    def brainmask(self, size=(5,3)):
        brainmask = os.path.join(self.d, 'mri', 'brainmask.mgz')
        x,y,z = nib.load(brainmask).shape
        tiles = size[0] * size[1]
        top,bottom = self.bounds(brainmask, axis=1)
        step = math.ceil((bottom - top) / tiles)
        logger.info('brainmask top=%s, bottom=%s, step=%s', top, bottom, step)
        # build and execute freeview command
        bmv = '{0}:colormap=heat:opacity=0.4'.format(
            os.path.join(self.d, 'mri', 'brainmask.mgz')
        )
        preamble = [
            'freeview',
            '-v', os.path.join(self.d, 'mri', 'T1.mgz'),
            '-v', bmv,
            '-layout', '1',
            '-cc',
            '-nocursor',
            '-viewsize', str(x), str(y)
        ]
        slices = list()
        output_files = list() 
        for i in range(top, bottom, step):
            saveas = os.path.join(
                self.output_dir,
                'img-brainmask_axis-axial_slice-{0}.png'.format(i)
            )
            cmd = [
                '-viewport', 'axial',
                '-slice', str(int(x / 2)), str(i), str(int(z / 2)),
                '-ss', saveas,
                '-noquit'
            ]
            slices.append(cmd)
            output_files.append(saveas)
        self.run_freeview(preamble, slices, verify=output_files)
        # remove previously cropped images
        expr = os.path.join(self.output_dir, 'img-brainmask_axis-axial_slice-*_crop.png')
        for f in glob.glob(expr):
            os.remove(f)
        # crop derived images
        expr = os.path.join(self.output_dir, 'img-brainmask_axis-axial_slice-*.png')
        self._crop(expr, pad=10)
        # add slice number caption to cropped images
        expr = os.path.join(self.output_dir, 'img-brainmask_axis-axial_slice-*_crop.png')
        self._caption(expr)
        # create mosaic from captioned cropped images
        saveas = os.path.join(self.output_dir, 'img-brainmask_axis-axial_mosaic.png')
        self._mosaic(expr, saveas=saveas, size=size)

    def orig(self, size=(5,3)):
        orig = os.path.join(self.d, 'mri', 'orig.mgz')
        x,y,z = nib.load(orig).shape
        brainmask = os.path.join(self.d, 'mri', 'brainmask.mgz')
        top,bottom = self.bounds(brainmask, axis=1)
        tiles = size[0] * size[1]
        step = math.ceil((bottom - top) / tiles)
        # build freeview command
        preamble = [
            'freeview',
            '-v', orig,
            '-layout', '1',
            '-cc',
            '-nocursor',
            '-viewsize', str(x), str(y)
        ]
        slices = list()
        output_files = list()
        for i in range(top, bottom, step):
            saveas = os.path.join(
                self.output_dir,
                'img-T1w_axis-axial_slice-{0}.png'.format(i)
            )
            cmd = [
                '-viewport', 'axial',
                '-slice', str(int(x / 2)), str(i), str(int(z / 2)),
                '-ss', saveas,
                '-noquit'
            ]
            slices.append(cmd)
            output_files.append(saveas)
        self.run_freeview(preamble, slices, verify=output_files)
        # remove previously cropped images
        expr = os.path.join(self.output_dir, 'img-T1w_axis-axial_slice-*_crop.png')
        for f in glob.glob(expr):
            os.remove(f)
        # crop derived images
        expr = os.path.join(self.output_dir, 'img-T1w_axis-axial_slice-*.png')
        self._crop(expr, pad=10)
        # add slice number caption to cropped images
        expr = os.path.join(self.output_dir, 'img-T1w_axis-axial_slice-*_crop.png')
        self._caption(expr)
        # create mosaic from captioned cropped images
        saveas = os.path.join(self.output_dir, 'img-T1w_axis-axial_mosaic.png')
        self._mosaic(expr, saveas=saveas, size=size)

    def bounds(self, img, threshold=(100, 100), axis=1):
        nimg = nib.load(img)
        dat = nimg.get_fdata()
        start = 0
        stop = nimg.shape[axis] - 1
        logger.debug('find top boundary')
        for i in range(0, nimg.shape[axis] - 1):
            frame = dat.take(i, axis=axis)
            if np.count_nonzero(frame) > threshold[0]:
                start = i
                break
        logger.debug('find bottom boundary')
        dat = np.flip(dat, axis=axis)
        for i in range(0, nimg.shape[axis] - 1):
            frame = dat.take(i, axis=axis)
            if np.count_nonzero(frame) > threshold[1]:
                stop = nimg.shape[axis] - i - 1
                break
        logger.debug('boundary top=%s, bottom=%s', start, stop)
        return start, stop

class FreeviewError(Exception):
    pass
