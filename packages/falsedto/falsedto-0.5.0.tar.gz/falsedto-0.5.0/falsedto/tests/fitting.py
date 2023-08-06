#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from .. misc import gaussian_line, generate_test_image
from .. hough import HoughTransform


def single_segment_fitting_test(
    image_shape=(400,600),
    intensity=1.25, sigma=1.0, width=4.0, band_width=10.0):
  Ny,Nx = image_shape
  x0,y0 = np.random.uniform(20,Nx-20), np.random.uniform(20,Ny-20)
  x1,y1 = np.random.uniform(20,Nx-20), np.random.uniform(20,Ny-20)

  image = intensity*gaussian_line((Ny,Nx), (y0,x0), (y1,x1), width)\
          +sigma*np.random.normal(size=(Ny,Nx))
  fig = plt.figure(figsize=(16,9))
  ax1 = fig.add_subplot(221)
  ax1.imshow(image)
  ax1.scatter(x0,y0, color=(1.0,0.5,0.5))
  ax1.scatter(x1,y1, color=(1.0,0.5,0.5))
  ax1.invert_yaxis()

  ht = HoughTransform(image, sigma)
  theta = np.arctan2(y1-y0,x1-x0)
  cos,sin = np.cos(theta),np.sin(theta)
  r = (sin*(x0-(Nx-1)/2.) - cos*(y0-(Ny-1)/2.))

  el = ht.elements_along(r,theta,band_width)
  res = ht.fit(r,theta,band_width)
  dm1,dm2 = res[2],res[3]

  ax2 = fig.add_subplot(222)
  ax2.imshow(image * ht.mask(r, theta, band_width))
  ax2.invert_yaxis()
  p1 = ht.locate(r, theta, dm1)
  p2 = ht.locate(r, theta, dm2)
  ax2.scatter(p1[0]+(Nx-1)/2,p1[1]+(Ny-1)/2, color=(0.3,0.3,1.0))
  ax2.scatter(p2[0]+(Nx-1)/2,p2[1]+(Ny-1)/2, color=(0.3,0.3,1.0))

  ax3 = fig.add_subplot(223)
  ax3.plot(el[0],el[1])
  ax3.plot(el[0],ht.ramp_sigmoid(el[0],res))

  prof = ht.profile(r, theta, dm1, dm2, 2*band_width)
  ax4 = fig.add_subplot(224)
  ax4.plot(prof[0],prof[1])

  fig.tight_layout()
  plt.show()


if __name__=='__main__':
  from argparse import ArgumentParser as ap
  parser = ap(description='A fitting procedure test with a single segment.')

  parser.add_argument(
    '-S', '--shape', dest='shape', type=int, nargs=2, default=(400,600),
    help='image size')
  parser.add_argument(
    '-i', '--intensity', dest='intensity', type=float, default=1.25,
    help='line intensity')
  parser.add_argument(
    '-s', '--sigma', dest='sigma', type=float, default=1.00,
    help='white noise')
  parser.add_argument(
    '-w', '--width', dest='width', type=float, default=4.0,
    help='line width')
  parser.add_argument(
    '-b', '--band-width', dest='band_width', type=float, default=6.0,
    help='extraction band width')

  args = parser.parse_args()

  single_segment_fitting_test(
    image_shape=args.shape, intensity=args.intensity,
    sigma=args.sigma, width=args.width, band_width=args.band_width)
