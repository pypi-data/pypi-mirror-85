import numpy as np
from pymeteo import constants
from .. import OptionsWidget

class sickle(OptionsWidget.OptionsWidget):

  def __init__(self):
    super(sickle,self).__init__()
    name = 'curved90 (quartercircle)'
    variables = [ ('z_curve,top',     '500', 'm'),
                  ('z_constabv',     '6000', 'm'),
                  ('z_constblo',        '0', 'm'),
                  ('u_straight,min', '12.0', 'm/s'),
                  ('u_straight,max', '31.0', 'm/s'),
                  ('eccentricity'  ,  '0.2' , ''),
                  ('u_adjust'     ,   '0.0', 'm/s'),
                  ('v_adjust'      ,  '0.0', 'm/s') ]
    self.initUI(name, variables)
 
  def plot(self):
    # nned z, t, th, p and qv
    z = np.arange(0., 22000., 50.)
    u = np.zeros(len(z))
    v = np.zeros(len(z))

    # parameters
    zdep0 = self.getOption('z_constblo')
    zdep1 = self.getOption('z_curve,top')
    zdep2 = self.getOption('z_constabv')
    umax1 = self.getOption('u_straight,min')
    umax2 = self.getOption('u_straight,max')
    ecc   = self.getOption('eccentricity')
    cx = self.getOption('u_adjust')
    cy = self.getOption('v_adjust')

    for k in range(len(z)):
      if (z[k] < zdep0):
        u[k] = ecc*umax1
        v[k] = 0  
      elif (z[k] < zdep1): # curvature section
        a = ((z[k]-zdep0)/(zdep1-zdep0))*(np.pi/2.)+(3.*np.pi/2.)
        u[k] = ecc*umax1+ecc*umax1*(-np.cos(a))
        v[k] = umax1*(1.+np.sin(a))
      elif (z[k] < zdep2): # straight section
        u[k] = ((z[k]-zdep1)/(zdep2-zdep1))*umax1+(z[k]-zdep1)*(umax2-umax1)/(zdep2-zdep1)
        v[k] = umax1
      else: # constant section
        u[k] = umax2
        v[k] = umax1

    u[:] = u[:] - cx
    v[:] = v[:] - cy

    #emit
    return (z,u,v)
    
