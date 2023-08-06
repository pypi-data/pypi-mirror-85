#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.optimize as opt
import itertools


class HoughTransform(object):
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

  def score_box(self, rarr, tarr, width):
    nr,nt = rarr.size,tarr.size
    score = []
    for r,t in itertools.product(rarr,tarr):
      score.append(self.snr(r,t,width))
    return np.array(score).reshape((nr,nt))

  def p0(self, r, theta):
    return np.array([r*np.sin(theta),-r*np.cos(theta)])

  def n0(self, r, theta):
    return np.array([np.cos(theta), np.sin(theta)])

  def dl(self, r, theta):
    cos,sin = np.cos(theta),np.sin(theta)
    return (-sin*self.axis1+cos*self.axis2+r)

  def dm(self, r, theta):
    cos,sin = np.cos(theta),np.sin(theta)
    return cos*self.axis1+sin*self.axis2

  def dmlim(self, r, theta):
    ny,nx = self.image.shape
    p = np.tile(self.p0(r,theta), 2)
    b = np.tile(self.n0(r,theta),2)
    b[np.abs(b)<1e-8] = 1e-8
    X = (np.array([-(nx-1)/2,-(ny-1)/2,(nx-1)/2,(ny-1)/2])-p)/b
    Xm,Xp = X[X<0], X[X>0]
    return np.max(Xm),np.min(Xp)

  def locate(self, r, theta, dm):
    return self.p0(r,theta)+dm*self.n0(r,theta)

  def mask(self, r, theta, w):
    return np.abs(self.dl(r,theta))<w

  def elements_along(self, r, theta, w):
    mask = self.mask(r,theta,w)
    dm,px = self.dm(r, theta)[mask], self.image[mask]
    dm = np.append(dm, self.append_x)
    px = np.append(px, self.append_y)
    index = dm.argsort()
    elem = np.vstack((dm[index],np.cumsum(px[index])))
    return elem

  def snr(self, r, theta, w):
    E = self.elements_along(r, theta, w)
    N,m,M = E[1].size,E[1].min(),E[1].max()
    return (M-m)/self.sigma/np.sqrt(N)

  def fit(self, r, theta, w):
    E = self.elements_along(r, theta, w)
    N,m,M = E[1].size,E[1].min(),E[1].max()
    s = self.sigma*np.sqrt(1+np.arange(N))
    dm,dM = self.dmlim(r, theta)
    bounds = opt.Bounds([-np.inf,-np.inf,dm,dm],[np.inf,np.inf,dM,dM])
    init = [m, (M-m)/N, dm, dM-dm]
    func = lambda p: np.sum((E[1]-self.ramp_sigmoid(E[0],p))**2/s**2)
    res = opt.minimize(func, init, method='L-BFGS-B',bounds=bounds)
    return np.hstack((res.x, np.sqrt(res.fun)/N))

  def profile(self, r, theta, dm1, dm2, w):
    dm = self.dm(r,theta)
    mask = (self.mask(r,theta,w)) & (dm>dm1) & (dm<dm2)
    dl = self.dl(r, theta)[mask]
    px = self.image[mask]
    hist,edge = np.histogram(dl, weights=px/(dm2-dm1), bins=int(4*w))
    edge = edge[1:]-np.diff(edge)
    return np.vstack((edge,hist))

  def ramp_sigmoid(self, x, p):
    return p[0]+p[1]*np.clip((x-p[2]), 0, max(p[3]-p[2],1e-8))
