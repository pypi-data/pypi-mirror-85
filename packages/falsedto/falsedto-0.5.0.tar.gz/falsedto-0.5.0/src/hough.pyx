#!/usr/bin/env cython
# -*- coding: utf-8 -*-
from libcpp.vector cimport vector as vec
from libcpp.list cimport list as clist
from numpy cimport ndarray, float64_t
import numpy as np
import scipy.optimize as opt
import itertools


cdef extern from 'hough.h' namespace 'hough':
  ctypedef double* pixmap

  cdef pixmap generate_hough_transformed_map(
    const pixmap input, const size_t& naxis1, const size_t& naxis2,
    const double& r0, const double& r1, const size_t& naxis_r,
    const double& t0, const double& t1, const size_t& naxis_t,
    const double& width)


class HoughTransform(object):
  ''' Hough Transformation
  '''
  def __init__(self, image, sigma):
    self.image = image
    self.sigma = sigma
    ny,nx = image.shape
    self.center = (ny-1)/2.0,(nx-1)/2.0
    self.axis1 = np.arange(nx).reshape((1,nx))-self.center[1]
    self.axis2 = np.arange(ny).reshape((ny,1))-self.center[0]
    self.radius = np.sqrt(nx**2+ny**2)/2.0
    self.append_x = self.radius * np.array([-1,1])
    self.append_y = np.zeros(2)

  def dl(self, float r, float theta):
    cdef float cos,sin
    cos,sin = np.cos(theta), np.sin(theta)
    return (-sin*self.axis1+cos*self.axis2+r)

  def dm(self, float r, float theta):
    cdef float cos,sin
    cos,sin = np.cos(theta), np.sin(theta)
    return (cos*self.axis1+sin*self.axis2)

  def p0(self, float r, float theta):
    return np.array([r*np.sin(theta),-r*np.cos(theta)])

  def n0(self, float r, float theta):
    return np.array([np.cos(theta), np.sin(theta)])

  def dmlim(self, float r, float theta):
    cdef float ny,nx
    cdef ndarray p,b,X,Xm,Xp
    ny,nx = self.image.shape
    p = np.tile(self.p0(r,theta), 2)
    b = np.tile(self.n0(r,theta),2)
    b[np.abs(b)<1e-8] = 1e-8
    X = (np.array([-(nx-1)/2,-(ny-1)/2,(nx-1)/2,(ny-1)/2])-p)/b
    Xm,Xp = X[X<0], X[X>0]
    return np.max(Xm),np.min(Xp)

  def locate(self, float r, float theta, float dm):
    return self.p0(r,theta)+dm*self.n0(r,theta)

  def score_map(self, float r0, float r1, int nr,
                float t0, float t1, int nt, float width=1.0):
    ''' Create Score Map
    '''
    cdef int n,ny,nx
    cdef double r,t
    cdef ndarray score = np.zeros((nr*nt,))
    cdef ndarray[float64_t,ndim=2,mode='c'] numpy_input
    numpy_input = np.ascontiguousarray(self.image.T,dtype=np.float64)

    ny,nx = self.image.shape
    cdef pixmap outbuf = generate_hough_transformed_map(
      <double*>numpy_input.data,ny,nx,r0,r1,nr,t0,t1,nt,width)
    for n in range(nr*nt): score[n] = outbuf[n]
    return score.reshape((nr,nt))

  def mask(self, float r, float theta, float w):
    return np.abs(self.dl(r,theta))<w

  def elements_along(self, float r, float theta, float w):
    cdef ndarray mask,dm,px,index,elem
    mask = self.mask(r,theta,w)
    dm = self.dm(r,theta)[mask]
    px = self.image[mask]
    dm = np.append(dm, self.append_x)
    px = np.append(px, self.append_y)
    index = dm.argsort()
    elem = np.vstack((dm[index],np.cumsum(px[index])))
    return elem

  def snr(self, float r, float theta, float w):
    cdef int N
    cdef float m,M
    cdef ndarray E
    E = self.elements_along(r, theta, w)
    N,m,M = E[1].size,E[1].min(),E[1].max()
    return (M-m)/self.sigma/np.sqrt(N)

  def fit(self, float r, float theta, float w):
    cdef int N
    cdef float m,M,dm,dM
    cdef ndarray E,s
    E = self.elements_along(r, theta, w)
    N,m,M = E[1].size,E[1].min(),E[1].max()
    s = self.sigma*np.sqrt(1+np.arange(N))
    dm,dM = self.dmlim(r, theta)
    bounds = opt.Bounds([-np.inf,-np.inf,dm,dm],[np.inf,np.inf,dM,dM])
    init = [m, (M-m)/N, dm, dM-dm]
    func = lambda p: np.sum((E[1]-self.ramp_sigmoid(E[0],p))**2/s**2)
    res = opt.minimize(func, init, method='L-BFGS-B',bounds=bounds)
    return np.hstack((res.x, np.sqrt(res.fun)/N))

  def profile(self, float r, float theta, float dm1, float dm2, float w):
    cdef ndarray dm,mask,dl,px,hist,edge
    dm = self.dm(r,theta)
    mask = (self.mask(r,theta,w)) & (dm>dm1) & (dm<dm2)
    dl = self.dl(r,theta)[mask]
    px = self.image[mask]
    hist,edge = np.histogram(dl, weights=px/(dm2-dm1), bins=int(4*w))
    edge = edge[1:]-np.diff(edge)
    return np.vstack((edge,hist))

  def ramp_sigmoid(self, ndarray x, ndarray p):
    return p[0]+p[1]*np.clip((x-p[2]), 0, max(p[3]-p[2],1e-8))
