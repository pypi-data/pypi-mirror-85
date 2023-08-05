#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hdrstats` package."""

import pytest

from click.testing import CliRunner

from hdrstats import hdrstats
import numpy as np


data = np.arange(-10,10.01,.01)
weights1 = np.ones(data.size)
weights2 = np.concatenate((np.full(int(data.size/2), 2.0), np.full(int(data.size/2)+1, 1.0)))


def test_weighted_median():
    r1 = hdrstats.weighted_median(data)
    assert np.isclose(r1, 0)
    r2 = hdrstats.weighted_median(data, weights1)
    assert np.isclose(r2, 0)
    r3 = hdrstats.weighted_median(np.arange(10), np.ones(10))
    assert np.isclose(r3, np.quantile(np.arange(10), .5))
    r4 = hdrstats.weighted_median(data, weights2)
    bf = np.concatenate((data[:1000], data[:1000]-.0025, data[1000:]))
    assert np.isclose(r4, np.quantile(bf, .5, interpolation='linear'))


def test_weighted_quantile():
    q = np.array([0, .2, .336, .744, 1])
    r1 = hdrstats.weighted_quantile(data, q)
    assert np.allclose(r1, np.quantile(data, q))
    r2 = hdrstats.weighted_quantile(data, q, weights1)
    assert np.allclose(r2, np.quantile(data, q))
    r3 = hdrstats.weighted_quantile(np.arange(10), q, np.ones(10))
    assert np.allclose(r3, np.quantile(np.arange(10), q))
    r4 = hdrstats.weighted_quantile(data, q, weights2)
    bf = np.concatenate((data[:1000], data[:1000], data[1000:]))
    # note weighting behaves differently then doubling values for percentiles between results
    assert np.allclose(r4, np.quantile(bf, q), atol=.003)