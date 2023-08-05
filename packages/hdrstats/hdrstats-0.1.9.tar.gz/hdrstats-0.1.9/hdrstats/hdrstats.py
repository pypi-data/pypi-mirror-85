# -*- coding: utf-8 -*-
# Copyright (c) 2020 Stephen Wasilewski
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""dat parsing and statistical analysis."""
from scipy import stats
from scipy.special import softmax
import numpy as np
import sys
from sklearn.linear_model import LogisticRegression

from hdrstats import __version__


def corr_header(lin=True, spearman=False, pearson=False, pvals=True, rbc=False,
                rmse=False, rrmse=False, mae=False, rmae=False, msd=False,
                rmsd=False, **kwargs):
    """generate headers for corr_calc"""
    out = []
    if lin:
        out += ['r^2', 'p']
    if spearman:
        out += ['spearman_rho', 'spearman_pval']
    if pearson:
        out += ['pearson_rho', 'pearson_pval']
    if rbc:
        out += ['rank_biserial', 'wilcoxon_pval']
    if not pvals:
        out = out[0::2]
    if rmse:
        out += ['RMSE']
    if mae:
        out += ['MAE']
    if rrmse:
        out += ['RMSE_relative']
    if rmae:
        out += ['MAE_relative']
    if msd:
        out += ['MSD']
    if rmsd:
        out += ['MSD_relative']
    return out


def rel_error(x, y):
    return np.where(np.abs(y) > 0, 1 - x/y, np.where(np.abs(x) > 0, 1, 0))

def corr_calc(x, y, lin=True, spearman=False, pearson=False, pvals=True,
              rbc=False, rmse=False, rrmse=False, mae=False, rmae=False,
              msd=False, rmsd=False, **kwargs):
    """calculate correlations between pairs of data"""
    out = []
    x = np.asarray(x)
    y = np.asarray(y)
    if lin:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        out += [r_value**2, p_value]
    if spearman:
        rho, pval2 = stats.spearmanr(x,y)
        out += [rho, pval2]
    if pearson:
        rho, pval2 = stats.pearsonr(x,y)
        out += [rho**2, pval2]
    if rbc:
        T, p = stats.wilcoxon(x, y)
        rbc = abs(2*(T/sum(range(len(y)+1))-.5))
        out += [rbc, p]
    if not pvals:
        out = out[0::2]
    if rmse:
        err = (np.sum(y-x)**2/len(x))**.5
        out += [err]
    if mae:
        err = np.sum(np.abs(y-x))/len(x)
        out += [err]
    if rrmse:
        rerr = rel_error(x, y)
        err = (np.sum(rerr)**2/len(x))**.5
        out += [err]
    if rmae:
        rerr = rel_error(x, y)
        err = np.sum(np.abs(rerr))/len(x)
        out += [err]
    if msd:
        err = np.sum(y-x)/len(x)
        out += [err]
    if rmsd:
        rerr = rel_error(x, y)
        err = np.sum(rerr)/len(x)
        out += [err]
    return out


def qq(x, y):
    """calculate qq plot data"""
    x = stats.rankdata(x)
    y = stats.rankdata(y)
    return np.stack((x,y)).T


def g_err(a, b, c, sigma, scale=1.0, conf=.95, zero=False):
    """apply kernel density estimate from b to c at a"""
    n = stats.norm(loc=a, scale=sigma)
    weights = n.pdf(b)
    if np.sum(weights) > 0:
        mu = np.average(c, weights=weights)
        if zero:
            sigma2 = np.sqrt(np.average(np.square(c), weights=weights))
        else:
            sigma2 = np.sqrt(np.average(np.square(c - mu), weights=weights))
        interval = stats.norm.interval(conf, loc=mu, scale=sigma2)
        ssize = np.sum(weights)*scale*len(b)/np.sum(b)
        err = (interval[1]- interval[0])/(2*np.sqrt(ssize))
    else:
        mu = 0
        ssize = 0
        err = 1
        print(f'KD is insufficient at {a}', file=sys.stderr)
    return mu, mu - err, mu + err, ssize


def g_ssize(a, b, sigma):
    n = stats.norm(loc=a, scale=sigma)
    ssize = np.sum(n.pdf(b))*len(b)*sigma*np.sqrt(2*np.pi)/np.sum(b)
    return ssize


def kde_cont(b, resample=None, ksigma=None):
    if ksigma is None:
        sigma = np.sqrt(np.cov(b)*len(b)**(-.4))
    else:
        sigma = ksigma
    if resample is None:
        samples = b.reshape(-1, 1)
    else:
        samples = np.asarray(resample).reshape(-1, 1)
    ssize = np.apply_along_axis(g_ssize, 1, samples, b, sigma)
    return np.vstack((samples.flatten(), ssize)).T

def error_cont(b, adif, rdif, scale=1, resample=None, ksigma=None):
    """calculate continuous moving average of error (adif, rdif)
    based on the kernel density estimate of b, at b or if resample, at resample
    """
    # gaussian kernel selection by Scott's rule, see:
    # https://docs.scipy.org/doc/scipy/reference/generated/
    # scipy.stats.gaussian_kde.html
    if ksigma is None:
        sigma = np.sqrt(np.cov(b)*len(b)**(-.4))
    else:
        sigma = ksigma
    print(sigma)
    if resample is None:
        samples = b.reshape(-1, 1)
    else:
        samples = np.asarray(resample).reshape(-1, 1)
    MSD = np.apply_along_axis(g_err, 1, samples, b, rdif, sigma, scale, zero=True)
    MAD = np.apply_along_axis(g_err, 1, samples, b, adif, sigma, scale, zero=True)
    i = samples.flatten()
    result = np.stack((i, MAD[:,0], np.maximum(MAD[:,1], 0), MAD[:,2],
                          MSD[:,0], MSD[:,1], MSD[:,2], MSD[:,3])).T
    return result


def error_lgw(x, adif, rdif, coefs, y, t=0.0):
    c = coefs[:,0:1]
    i = coefs[:,1:]
    weights = softmax((x+i/c)*c, 0)
    header = ['category','MSD.025', 'MSD.05', 'MSD', 'MSD.95', 'MSD.975', 'MAD.025', 'MAD.05', 'MAD', 'MAD.95', 'MAD.975', 'neff']
    print(''.join([f'{i: >10}' for i in header]))
    for i, w in enumerate(weights):
        row = (list(conf_box([rdif,], [w,], ci=.9, ciw=.95, nsamp=1000, t=t)[0].values()) +
               list(conf_box([adif,], [w,], ci=.9, ciw=.95, nsamp=1000, t=t)[0].values()) +
               [np.sum(w[w >=t]),])
        print(f'{i: >10}' + ''.join([f'{j: >10.05f}' for j in row]))
    result = np.stack((x, adif, rdif, weights[0], weights[1], weights[2], y)).T
    return result


def weighted_quantile(d, q, w=None, t=0.0):
    if w is None:
        return np.quantile(d, q)
    else:
        si = np.argsort(d)
        d = np.asarray(d)[si]
        w = np.asarray(w)[si]
        d = d[w >= t]
        w = w[w >= t]
        cw = np.cumsum(w)
        cw = cw - cw[0]
        midp = np.asarray(q) * cw[-1]
        li = np.searchsorted(cw, midp, side='right') - 1
        ri = np.where(np.isclose(q, 1), li, li+1)
        dn = np.where(np.isclose(q, 1), 1, (cw[ri] - cw[li]))
        result = d[li] + (d[ri] - d[li]) * (midp - cw[li])/dn
        return result


def weighted_median(d, w=None, t=0.0):
    return weighted_quantile(d, .5, w, t)


def kernel(d, w=None, mi=None, mx=None, n=1000, t=1e-4, bws=.5):
    """prepare a gaussian kernel

    bws is a scale factor to the bw_method

    gaussian kernel selection by Scott's rule, see:
    https://docs.scipy.org/doc/scipy/reference/generated/
    scipy.stats.gaussian_kde.html
    """
    if w is None:
        neff = len(d)
    else:
        d = d[w >= t]
        w = w[w >= t]
        neff = np.sum(w)**2 / np.sum(w**2)
    k = stats.gaussian_kde(d, weights=w, bw_method=neff**(-1./(1+4))*bws)
    if mi is None:
        mi = np.min(d)
    if mx is None:
        mx = np.max(d)
    inc = (mx - mi)/(n+1)
    vstats = {}
    vstats['min'] = mi
    vstats['max'] = mx
    vstats['median'] = weighted_median(d, w, t)
    vstats['mean'] = np.average(d, weights=w)
    vstats['coords'] = np.arange(mi, mx+inc/2, inc)
    vstats['vals'] = k(vstats['coords'])
    return vstats


def box_stats(d, wg=None, ci=.75, ciw=.95, t=0.0):
    qs = np.array([.5 - ciw/2,.5 - ci/2, .5, .5 + ci/2, .5 + ciw/2])
    ps = [weighted_quantile(d, q, wg, t=t) for q in qs]
    keys = ['whislo', 'q1', 'med', 'q3', 'whishi']
    return dict(zip(keys, ps))


def bootsamps(samples, d, w=None):
    i = np.random.choice(np.arange(d.size), size=d.size)
    if w is not None:
        return np.average(d[i], weights=w[i])
    else:
        return np.average(d[i])

def conf_box(x, w=None, ci=.75, ciw=.95, nsamp=100, t=0.0):
    """bootstrap a confidence interval for the mean of a weighted sample"""
    bstats = []
    if w is None:
        w = (None,)*len(x)
    for d, wg in zip(x, w):
        d = np.asarray(d)
        samples = np.zeros((nsamp, d.size))
        boots = np.apply_along_axis(bootsamps, 1, samples, d, wg)
        bstats.append(box_stats(boots, None, ci, ciw, t=t))
    return bstats


def quant_box(x, w=None, ci=.75, ciw=.95):
    """create box and whiskers for weighted data"""
    if w is None:
        w = (None,)*len(x)
    return [box_stats(d, wg, ci, ciw) for d, wg in zip(x,w)]


def softmax_c(x, coefs):
    c = coefs[:,0:1]
    i = coefs[:,1:]
    return softmax((x+i/c)*c, 0)


def train_logit(xt, yt, w):
    logreg = LogisticRegression(solver='lbfgs', multi_class='multinomial',
                            max_iter=1000000, tol=1e-6, class_weight=w)
    logreg.fit(xt.reshape(-1, 1), yt)
    smaxc = np.vstack((logreg.coef_.flatten(), logreg.intercept_)).T
    return smaxc
