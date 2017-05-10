#!/bin/python
#-----------------------------------------------------------------
#       This script creates a very nice mass_radius plot
#                 Oscar Barragan. May, 2017
#-----------------------------------------------------------------

#Load libraries
import numpy as np
import urllib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks')
sns.set_color_codes()

#-----------------#
#--User controls--#
#-----------------#

#Select the precision in error bars for the planets 1 is 100%, 0.5 is 50%
precision_m = 0.2
precision_r = 0.2

#Select units, jupter or earth
units = 'earth'
units = 'jupiter'

#select the mass and radius range with units "units"
min_m = 1/317.83 
max_m = 20.0
min_r = 0
max_r = 2.5

#Figure size in inches 
fsize = 20

is_plot_zeng_models = True

#----------------------------------------------------------------
#All the magic!
#----------------------------------------------------------------

#Default jupiter to earth masses transformation
mfact = 317.83
rfact = 11.209

#I use the well-characterized planets table available at
#http://www.astro.keele.ac.uk/jkt/tepcat/
fname = 'allplanets-csv.csv'
urlname = 'http://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv'
#Download the updated table
urllib.urlretrieve(urlname, filename=fname)

#Read the values of mass and radius
m,mle,mre,r,rle,rre = np.loadtxt(fname,delimiter=',',unpack=True,usecols=range(26,32),skiprows=1)
#By default tepcat values are in Jupiter units, let us change it to "units"
if ( units == 'earth' ):
  m = m * mfact
  mle = mle * mfact
  mre = mre * mfact
  r = r * rfact
  rle = rle * rfact
  rre = rre * rfact

#Let us store the index for the planets which are inside the range and have error bars 
#smaller than our selection criteria
good_index = []

for o in range(0,len(m)):
  if ( m[o] > min_m and r[o] > min_r and m[o] < max_m and r[o] < max_r ):
    if ( mle[o] / m[o] < precision_m and mre[o] / m[o] < precision_m ):
      if ( rle[o] / r[o] < precision_r and rre[o] / r[o] < precision_r ):
        good_index.append(o)

#Print the details
print "There are ", len(good_index), 'exoplanets'
print "between", min_m, ' and ', max_m,' ',units,' masses'
print "between", min_r, ' and ', max_r,' ',units,' masses'
print "Precision in m better than ", precision_m
print "Precision in r better than ", precision_r

#----------------------------------------------------------
#             Add theoretical models
#----------------------------------------------------------

#Zeng models
newzeng = np.loadtxt('newZeng.txt',unpack=True)
#Zeng models are given in earth units, if necessary let us change it to Jupiter
if ( units == 'jupiter' ):
  newzeng[0] = newzeng[0] / mfact
  newzeng[1:] = newzeng[1:] / rfact


a = fsize/2.56
plt.figure(1,figsize=(a,a/1.618))
plt.minorticks_on()
if ( units == 'earth' ):
  plt.ylabel('Radius ($\mathrm{R_{\oplus}}$)',fontsize=fsize)
  plt.xlabel('Mass ($\mathrm{M_{\oplus}}$)',fontsize=fsize)
elif ( units == 'jupiter' ):
  plt.ylabel('Radius ($\mathrm{R_{\mathrm{J}}}$)',fontsize=fsize)
  plt.xlabel('Mass ($\mathrm{M_{\mathrm{J}}}$)',fontsize=fsize)
plt.ylim(min_r,max_r)
plt.xlim(min_m,max_m)
plt.semilogx()
plt.tick_params(labelsize=fsize)

if ( is_plot_zeng_models ): 
  plt.plot(newzeng[0],newzeng[1],color='#800000',label='$\mathrm{Fe}$')
  plt.plot(newzeng[0],newzeng[2],'--',color='#B22222',label='50%$\mathrm{Fe}$-50%$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0],newzeng[6],'y',label='$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0],newzeng[8],'b--',label='50%$\mathrm{MgSiO_3}$-50%$\mathrm{H_2O}$')
  plt.plot(newzeng[0],newzeng[9],'c',label='$\mathrm{H_2O}$')

for o in good_index:
  plt.errorbar(m[o],r[o],yerr=[[rre[o],rle[o]]],xerr=[[mre[o],mle[o]]],fmt='o')
plt.show()
