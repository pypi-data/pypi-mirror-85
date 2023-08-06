#!/bin/csh -fe
# original author: Greg Ward
# modified by: Stephen Wasilewski
# lorentzian is approximated with 3 gaussians
# improved coefficients for gaussian fit using scipy.optimize.curve_fit
# reduced RMSE for range 0-3 degrees from 0.002 to 0.0002


# blur image according to double pass line spread that accounts for aberrations, diffraction, and scatter
# cited study found a mean FWHM across ages of 11.9, FWHM=11 ~ 25 year old with healthy/corrected vision.

# python optimization code:

# import numpy as np
# from scipy import stats
# from scipy.optimize import curve_fit
#
# def fit_3norms(x, a, b, c, d, e):
#     y2a = stats.norm.pdf(x ,0, a) * d
#     y2b = stats.norm.pdf(x ,0, b) * e
#     y2c = stats.norm.pdf(x ,0, c) * (1 - (d+e))
#     return y2a + y2b + y2c
#
# xfit = np.arange(0,360, .01)
# x = np.arange(0,180, .01)
# cauchy = stats.cauchy(0, 5.5)
# y = cauchy.pdf(x)
# (a,b,c,d,e), pcov = curve_fit(fit_3norms, xfit, cauchy.pdf(xfit),
# 							  p0=[5.7, 22.6, 42.4, .85, .11],
# 							  maxfev=12000, bounds=([1,1,1,.04, .04],
# 								   					[50,50,50,.92, .92]))

# Simulate Lorentzian function with FWHM=11 (based on Yang, Y., Wanek, J. & Shahidi, M. Representing the retinal line spread shape with mathematical functions. J. Zhejiang Univ. Sci. B 9, 996–1002 (2008). https://doi.org/10.1631/jzus.B0820184)
#
set vhoriz=`getinfo < $1 | sed -n 's/^VIEW=.*-vh \([^ ]*\) .*$/\1/p'`
set rhoriz=`getinfo -d < $1 | sed 's/^.*+X //'`
set pparcmin=`ev "$rhoriz/(60*$vhoriz)"`
set rad=`ev "3.53*$pparcmin" "9.36*$pparcmin" "41.54*$pparcmin"`
echo "#?RADIANCE"
echo ""
set filta = 'pgblur'
set filtb = 'pgblur'
if ( "$rad[1]" !~ [1-9]* ) then
	set filta = 'pfilt -1 -e 1'
endif
if ( "$rad[2]" !~ [1-9]* ) then
	set filtb = 'pfilt -1 -e 1'
endif
pcomb -s .319 -o "\!$filta -r $rad[1] $1" -s .446 -o "\!$filtb -r $rad[2] $1" \
	  -s .235 -o "\!pgblur -r $rad[3] $1" | getinfo -
