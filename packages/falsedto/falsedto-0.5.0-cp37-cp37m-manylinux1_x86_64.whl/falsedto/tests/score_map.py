#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import sep

from .. misc import gaussian_line, generate_test_image
from .. hough import HoughTransform


def hough_transformation_score_map_test(
    image_shape, grid, num_line, intensity, sigma, width, logscale=False):
  Ny,Nx = image_shape
  image = generate_test_image(image_shape, num_line, intensity, width)

  fig = plt.figure(figsize=(8,12))
  ax1 = fig.add_subplot(211)
  ax1.imshow(image)
  ax1.invert_yaxis()

  N,M = grid
  ht = HoughTransform(image, sigma)
  R = np.sqrt(Nx**2+Ny**2)/2.0
  box = ht.score_map(-R,R,N,-np.pi/2,np.pi/2,M)

  ax2 = fig.add_subplot(212)
  logbox = np.log(1+np.abs(box))*np.sign(box)
  if logscale is True:
    ax2.imshow(logbox, extent=(-90,90,-R,R), aspect='auto')
  else:
    ax2.imshow(box, extent=(-90,90,-R,R), aspect='auto')

  model = sep.Background(box)
  model.subfrom(box)
  obj = sep.extract(box, 3.0, minarea=5.0, err=1.0)
  print('{} line segments detected.'.format(len(obj)))
  r,t = -90+180*obj['xpeak']/(M-1), R-2*R*obj['ypeak']/(N-1)
  ax2.scatter(r,t,color=(1.0,0.8,0.3,0.3))

  plt.show()


if __name__=='__main__':
  from argparse import ArgumentParser as ap
  parser = ap(description='A Hough-Transformation test.')

  parser.add_argument(
    '-S', '--shape', dest='image_shape', type=int, nargs=2, default=(400,600),
    help='image size')
  parser.add_argument(
    '-n', '--grid', dest='grid', type=int, nargs=2, default=(601,181),
    help='number of grids')
  parser.add_argument(
    '-l', '--line', dest='num_line', type=int, default=5,
    help='number of lines')
  parser.add_argument(
    '-i', '--intensity', dest='intensity', type=float, default=5.0,
    help='line intensity')
  parser.add_argument(
    '-s', '--sigma', dest='sigma', type=float, default=1.00,
    help='white noise')
  parser.add_argument(
    '-w', '--width', dest='width', type=float, default=3.0,
    help='line width')
  parser.add_argument(
    '--log','--log-scale', dest='logscale', action='store_true',
    help='display in log scale')

  from datetime import datetime
  args = parser.parse_args()

  hough_transformation_score_map_test(
    image_shape=args.image_shape, grid=args.grid,
    num_line=args.num_line, intensity=args.intensity,
    sigma=args.sigma, width=args.width, logscale=args.logscale)
