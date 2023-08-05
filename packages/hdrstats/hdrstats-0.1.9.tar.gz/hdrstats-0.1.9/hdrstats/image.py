# -*- coding: utf-8 -*-
# Copyright (c) 2020 Stephen Wasilewski
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""dat parsing and statistical analysis."""
import numpy as np

import clasp.script_tools as cst


def img_size(img):
    """returns x and y pixel dimensions of image"""
    geti = 'getinfo -d {}'.format(img)
    dims = cst.pipeline([geti]).split()
    y = int(dims[2])
    x = int(dims[4])
    return x, y


def get_omegas(image, xres, yres):
    """get solid angle of each pixel in image"""
    pcomb = f"pcomb -e 'lo=S(1)' {image}"
    pval = "pvalue -o -H -h -d -b"
    imdat = [float(i) for i in cst.pipeline([pcomb, pval]).strip().split()]
    imarray = np.reshape(imdat, (yres, xres)).swapaxes(0, 1)
    return np.flip(imarray, 1)


def get_cos(res):
    """generate a 2D array of cos(r) values"""
    a = np.linspace(-np.pi/2, np.pi/2, res)
    x, y = np.meshgrid(a, a, sparse=True)
    z = np.cos(np.sqrt(np.square(x) + np.square(y)))
    z[z < 0] = 0
    return z


def read_im_to_array(image, xres, yres, color=False, prepipe=None):
    """read hdr image to numpy array
    
    prepipe should be a format string correctly placing image, eg:
    
        "pcomb -s .8 {} | pfilt -1 -e 1 -x 500 -y 500"
    
    """
    pval = "pvalue -o -H -h -d "
    if not color:
        pval += "-b "
    if prepipe is not None:
        imdat = [float(i) for i in cst.pipeline([prepipe.format(image),
                                                 pval]).strip().split()]
    else:
        imdat = [float(i) for i in cst.pipeline([pval + image]).strip().split()]
    if color:
        imarray = np.reshape(imdat, (yres, xres, 3)).swapaxes(0, 1)
    else:
        imarray = np.reshape(imdat, (yres, xres)).swapaxes(0, 1)
    return np.flip(imarray, 1)


def img_2_stats(img, res=None, omegas=None, cos=None, scale=179, hblur=False):
    """read image and return Ev and luminance ratio"""
    if hblur:
        imarray = read_im_to_array(img, res, res, prepipe='humanblur.csh {}')
    else:
        imarray = read_im_to_array(img, res, res)
    wlum = imarray * omegas * scale
    inv = cos > 0
    illum = np.sum(wlum * cos)
    alum = np.sum(wlum[inv])/(np.pi * 2)
    alum2 = np.sum((np.square(imarray * scale) * omegas)[inv])/(np.pi * 2)
    l2l2 = alum2/np.square(alum)
    # std (with samples weighted by omega)
    std = np.sqrt(np.average(np.square((imarray * scale)[inv] - alum),
                             weights=omegas[inv]))
    # absolute deviation
    ad = np.average(np.abs((imarray * scale)[inv] - alum),
                             weights=omegas[inv])
    return illum, l2l2, std, ad

def evalglare(img, options="", detail=True, **kwargs):
    """return dict of evalglare output"""
    if detail:
        options += " -d"
    output = cst.pipeline([f'evalglare {options} {img}'])
    lines = output.splitlines()
    calchdr = lines[-1].split(':')[0].strip().split(',')
    calcs = lines[-1].split(':')[-1].strip().split()
    result = dict()
    for h, c in zip(calchdr, calcs):
        result[h] = float(c)
    if detail:
        srcs = lines[1:-1]
        srchdr = lines[0].split()[2:]
        result['srcs'] = []
        for src in srcs:
            src = src.split()[1:]
            srcstats = dict()
            for h, c in zip(srchdr, src):
                srcstats[h] = float(c)
            result['srcs'].append(srcstats)
        result['T1'], result['T2'] = dgp_comp(result['srcs'])
    return result


def dgp_comp(srcs):
    Ls = np.square(np.array([i['L_s'] for i in srcs]))
    omega = np.array([i['Omega_s'] for i in srcs])
    Ev = srcs[0]['E_vert']
    P = np.array([i['Posindx'] for i in srcs])
    if np.sum(Ls) > 0:
        t2 = np.round(.0918*np.sum(np.log10(Ls*omega/(np.square(P)*
                      np.power(Ev,1.87))+1)), 6)
    else:
        t2 = 0
    t1 = np.round(.0000587*Ev, 6)
    return t1, t2