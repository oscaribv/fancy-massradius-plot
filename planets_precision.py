#!/bin/python
#------------------------------------------------------------------------
#       This script creates a very nice mass_radius plot
#                 Oscar Barragan. May, 2017
#------------------------------------------------------------------------

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

#select the mass and radius range (Jupiter masses)
min_m = 0.0
max_m = 1e3
min_r = 0.0
max_r = 3.0

max_m = 20 * 1.0 / 317.83 
max_r = 3.0 / 11.209

is_plot_zeng_models = True

#Default jupiter to earth masses transformation
mfact = 317.83
rfact = 11.209

#------------------------------------------------------------------------
#All the magic!
#------------------------------------------------------------------------

#I use the well-characterized planets table available at
#http://www.astro.keele.ac.uk/jkt/tepcat/
fname = 'allplanets-csv.csv'
urlname = 'http://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv'
#Download the updated table
urllib.urlretrieve(urlname, filename=fname)

#Read the values of mass and radius
m,mle,mre,r,rle,rre = np.loadtxt(fname,delimiter=',',unpack=True,usecols=range(26,32),skiprows=1)

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
print "between", min_m, ' and ', max_m, 'Jupiter masses'
print "between", min_r, ' and ', max_r, 'Jupiter masses'
print "Precision in m better than ", precision_m
print "Precision in r better than ", precision_r

#----------------------------------------------------------
#             Add theoretical models
#----------------------------------------------------------

#Zeng models
newzeng = np.loadtxt('newZeng.txt',unpack=True)

if ( is_plot_zeng_models ): 
  plt.plot(newzeng[0]/mfact,newzeng[1]/rfact,color='#800000',label='$\mathrm{Fe}$')
  plt.plot(newzeng[0]/mfact,newzeng[2]/rfact,'--',color='#B22222',label='50%$\mathrm{Fe}$-50%$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0]/mfact,newzeng[6]/rfact,'y',label='$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0]/mfact,newzeng[8]/rfact,'b--',label='50%$\mathrm{MgSiO_3}$-50%$\mathrm{H_2O}$')
  plt.plot(newzeng[0]/mfact,newzeng[9]/rfact,'c',label='$\mathrm{H_2O}$')


plt.semilogx()
for o in good_index:
  plt.errorbar(m[o],r[o],yerr=[[rre[o],rle[o]]],xerr=[[mre[o],mle[o]]],fmt='o')
plt.show()
