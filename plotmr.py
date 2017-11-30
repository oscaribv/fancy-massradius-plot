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
sns.set(style='whitegrid')
sns.set_color_codes()

#-----------------#
#--User controls--#
#-----------------#

#Select the precision in error bars for the planets 1 is 100%, 0.5 is 50%, etc.
precision_m = 0.20
precision_r = 0.2

#Select units, jupter or earth
units = 'earth'
#units = 'jupiter'

#Some plot controls
#Figure size in inches 
fsize = 25
is_plot_my_planets = True


#select the mass and radius range with units "units"
if ( units == 'jupiter' ):
  min_m = 0.001
  max_m = 13.0
  min_r = 0.0
  max_r = 2.5
  semilog = True
  is_plot_zeng_models = False

if ( units == 'earth' ):
  min_m = 0.0
  max_m = 10.0
  min_r = 1.0
  max_r = 3.0
  semilog = False
  is_plot_zeng_models = True
#  min_m = 1.0
#  max_m = 50.0
#  min_r = 1.0
#  max_r = 6.0

#----------------------------------------------------------------
#                 All the magic stars!
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
#   Load my_planets.csv data
#----------------------------------------------------------
#----------------------------------------------------------
#   Load my_planets.csv data
#----------------------------------------------------------
pnam = np.loadtxt('my_planets.csv',usecols=[0],dtype=str,unpack=True,delimiter=',')
mp,mlep,mrep,rp,rlep,rrep  = np.loadtxt('my_planets.csv',usecols=[1,2,3,4,5,6],unpack=True,delimiter=',')


if ( units == 'earth' ):
  mp = mp * mfact
  mlep = mlep * mfact
  mrep = mrep * mfact
  rp = rp * rfact
  rlep = rlep * rfact
  rrep = rrep * rfact


#Let us store the index for the planets which are inside the range and have error bars 
#smaller than our selection criteria
good_index_myp = []

for o in range(0,len(mp)):
  if ( mp[o] > min_m and rp[o] > min_r and mp[o] < max_m and rp[o] < max_r ):
    if ( mlep[o] / mp[o] < precision_m and mrep[o] / mp[o] < precision_m ):
      if ( rlep[o] / rp[o] < precision_r and rrep[o] / rp[o] < precision_r ):
        good_index_myp.append(o)
#------------


myp = [None]*6
myp[0] = mp[good_index_myp]
myp[1] = mlep[good_index_myp]
myp[2] = mrep[good_index_myp]
myp[3] = rp[good_index_myp]
myp[4] = rlep[good_index_myp]
myp[5] = rrep[good_index_myp]


#----------------------------------------------------------
#             Add theoretical models
#----------------------------------------------------------

#Zeng models
#newzeng = np.loadtxt('newZeng.txt',unpack=True)
newzeng = np.loadtxt('mrtable3.txt',unpack=True,usecols=range(0,42))
#Zeng models are given in earth units, if necessary let us change it to Jupiter
if ( units == 'jupiter' ):
  newzeng[0] = newzeng[0] / mfact
  newzeng[1:] = newzeng[1:] / rfact

#----------------------------------------------------------
#             Start to create the plot
#----------------------------------------------------------

mark = ['D', 's', 'p', 'h', '8', '^', '<', '*', \
        'v','>','.', 'H', 'd','+']

#Create the xtics, this method is brute force!
xtics_vec = [0.01,0.02,0.03,0.04,0.05,0.08,0.1,0.2,0.3,0.4,0.5,0.8,1,2,3,4,5,8,10,20,30,40,50,80,100]
xtics_vec = [0.01,0.02,0.05,0.1,0.2,0.3,0.5,1,2,3,5,10,20,30,50,100]
xtics_vec_str = list(xtics_vec)
for o in range(0,len(xtics_vec)):
   xtics_vec_str[o] = str(xtics_vec[o]) 

a = fsize/2.56
plt.figure(1,figsize=(a,a/1.618))
plt.minorticks_on()
if ( units == 'earth' ):
  plt.ylabel('Radius ($\mathrm{R_{\oplus}}$)',fontsize=fsize)
  plt.xlabel('Mass ($\mathrm{M_{\oplus}}$)',fontsize=fsize)
elif ( units == 'jupiter' ):
  plt.ylabel('Radius ($\mathrm{R_{\mathrm{J}}}$)',fontsize=fsize)
  plt.xlabel('Mass ($\mathrm{M_{\mathrm{J}}}$)',fontsize=fsize)
if ( semilog ):
  plt.semilogx()
  plt.xticks(xtics_vec,xtics_vec_str)
plt.tick_params(labelsize=0.7*fsize)
plt.ylim(min_r,max_r)
plt.xlim(min_m,max_m)

#Shall I plot the zeng models?
if ( is_plot_zeng_models ): 
  plt.plot(newzeng[0],newzeng[41],'c',label='$\mathrm{H_2O}$')
  plt.plot(newzeng[0],newzeng[31],'b--',label='50%$\mathrm{MgSiO_3}$-50%$\mathrm{H_2O}$')
  plt.plot(newzeng[0],newzeng[21],'y',label='$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0],newzeng[11],'--',color='#B22222',label='50%$\mathrm{Fe}$-50%$\mathrm{MgSiO}_3$')
  plt.plot(newzeng[0],newzeng[1],color='#800000',label='$\mathrm{Fe}$')

#
#ADD FORTNEY MODELS LATER
#
def density_earth(mmin,mmax,rho):

  nx = int(1e5)

  r_dene = [None]*nx
  m_dene = [None]*nx

  dme = (mmax - mmin)/np.float(nx)

  m_dene[0] = mmin
  r_dene[0] = (m_dene[0]/(rho))**(1./3.)
  for i in range(1,nx):
    m_dene[i] = m_dene[i-1] + dme
    r_dene[i] = (m_dene[i]/(rho))**(1./3.)

  return np.array(m_dene), np.array(r_dene)

#Plot neptune like density
#http://nssdc.gsfc.nasa.gov/planetary/factsheet/neptunefact.html
neptune_mass = 17.15 #Earth mass
neptune_radi = 3.883 #Earth radii
neptune_vol  = 3.883**3 #Earth volume
neptune_den  = neptune_mass / neptune_vol #earth densitu
#http://nssdc.gsfc.nasa.gov/planetary/factsheet/uranusfact.html
uranus_mass = 14.54 #Earth mass
uranus_radi = 4.007 #Earth radii
uranus_vol  = 4.007**3 #Earth volume
uranus_den  = uranus_mass / uranus_vol #earth densitu


mf = 1
rf = 1
if ( units == 'jupiter' ):
  mf = 1/mfact
  rf = 1/rfact

eden_m, eden_r = density_earth(min_m/mf,max_m/mf,1.0)
nden_m, nden_r = density_earth(min_m/mf,max_m/mf,neptune_den)
uden_m, uden_r = density_earth(min_m/mf,max_m/mf,uranus_den)

#plt.plot(uden_m*mf,uden_r*rf,'--',label='Uranus-like density')
#plt.plot(nden_m*mf,nden_r*rf,'--',label='Neptune-like density')
#plt.plot(eden_m*mf,eden_r*rf,'--',label='Earth-like density')

#Plot all the planets 
for o in good_index:
  if ( is_plot_my_planets ):
    plt.errorbar(m[o],r[o],yerr=[[rre[o],rle[o]]],xerr=[[mre[o],mle[o]]],fmt='o',color='#C0C0C0')
  else:
    plt.errorbar(m[o],r[o],yerr=[[rre[o],rle[o]]],xerr=[[mre[o],mle[o]]],fmt='o',color='b')
  #plt.plot(m[o],r[o],'o',color='#C0C0C0',alpha=0.75)

#Plot my planets
if ( is_plot_my_planets ):
  from random import randint, seed

  pcolors = []
  seed(2128)
  for i in range(len(myp[0])):
      pcolors.append('#00%02X00' % randint(0x88, 0xFF))

  for o in range(0,len(myp[0])):
    plt.errorbar(myp[0][o],myp[3][o],yerr=[[myp[4][o],myp[5][o]]],xerr=[[myp[1][o],myp[2][o]]],fmt='o',color='#c61d01',markersize=fsize/3)
    #plt.errorbar(myp[0][o],myp[3][o],yerr=[[myp[4][o],myp[5][o]]],xerr=[[myp[1][o],myp[2][o]]],fmt='o')
    #plt.plot(myp[0][o],myp[3][o],'ro')
    #plt.plot(myp[0][o],myp[3][o],'o',color=pcolors[o])

titlestr = int(precision_m*1e2)
titlestr = 'Precision better than = ' + str(titlestr) + '%. N_planets = ' + str(len(good_index))
plt.title(titlestr,fontsize=0.7*fsize)
plt.legend(loc=0, ncol=1,scatterpoints=1,numpoints=1,frameon=True,fontsize=0.5*fsize)
plt.savefig('plot_mr.pdf',format='pdf',bbox_inches='tight')
plt.savefig('plot_mr.png',format='png',bbox_inches='tight',dpi=300)
plt.show()

#----------------------------------------------------------
#                     END OF FILE
#----------------------------------------------------------
