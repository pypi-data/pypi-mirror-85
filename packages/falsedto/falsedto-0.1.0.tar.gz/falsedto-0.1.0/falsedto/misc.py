#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def gaussian_line(shape,start,end,width):
  ''' Draw a gaussian-blurred line in an image.

  Parameters:
    shape (list): a (ny,nx)-shape of a generated image.
    start (list): the starting point of the line segment.
    end (list): the end point of the line segment.
    width (float): the width of line segments in FWHM.

  Return:
    An image with a line segment.
  '''
  ny,nx = shape
  y0,x0 = start
  y1,x1 = end
  length = np.sqrt((x1-x0)**2+(y1-y0)**2)
  cos,sin = (x1-x0)/length, (y1-y0)/length

  ay = np.arange(ny).reshape((ny,1))
  ax = np.arange(nx).reshape((1,nx))

  dl = np.abs(-sin*(ax-x0)+cos*(ay-y0))
  d0 = cos*(ax-x0)+sin*(ay-y0)
  d1 = cos*(ax-x1)+sin*(ay-y1)
  dx = dl**2*(d1*d0<0) \
    + ((d0<0)&(d1<0))*((ax-x0)**2+(ay-y0)**2) \
    + ((d0>0)&(d1>0))*((ax-x1)**2+(ay-y1)**2)
  sig = 4.*np.log(2.)/width**2

  line = np.exp(-sig*dx**2)
  return line/line.sum()*length


def generate_test_image(shape, n_line=1, intensity=5.0, width=3.0):
  ''' Generate an image with line segments.

  Parameters:
    shape (list): a (ny,nx)-shape of a generated image.
    n_line (int): the number of line segments.
    intensity (float): the line intensity of line segments.
    width (float): the width of line segments in FWHM.

  Return:
    An image with generated line segments.
  '''
  ny,nx = shape
  vy = np.random.uniform(0,ny,(2*n_line))
  vx = np.random.uniform(0,nx,(2*n_line))
  image = np.zeros(shape)
  for n in range(n_line):
    start = vy[2*n],vx[2*n]
    end   = vy[2*n+1],vx[2*n+1]
    image += intensity*gaussian_line(shape, start, end, width)

  image += np.random.normal(size=(ny,nx))
  return image
