from __future__ import print_function

import math
import numpy

import sys
import mesh.patch as patch
from util import msg

def init_data(my_data, rp):
    """ initialize the isothermal atmosphere problem """

    msg.bold("initializing the isothermal atmosphere problem...")

    # make sure that we are passed a valid patch object
    if not isinstance(my_data, patch.CellCenterData2d):
        print("ERROR: patch invalid in isothermal.py")
        print(my_data.__class__)
        sys.exit()

    # get the density, momenta, and energy as separate variables
    dens = my_data.get_var("density")
    xmom = my_data.get_var("x-momentum")
    ymom = my_data.get_var("y-momentum")
    ener = my_data.get_var("energy")

    gamma = rp.get_param("eos.gamma")

    grav_const = rp.get_param("compressible.grav")
    cs = rp.get_param("isothermal.cs")

    dens1 = rp.get_param("isothermal.dens1")

    amp = rp.get_param("isothermal.amp")
    sigma = rp.get_param("isothermal.sigma")

    if grav_const != 0.0:
        scale_height = cs*cs/numpy.abs(grav_const)
    else:
        scale_height = 0.1

    print("scale height:",scale_height)

    smalldens = 1.e-8

    # initialize the components, remember, that ener here is
    # rho*eint + 0.5*rho*v**2, where eint is the specific
    # internal energy (erg/g)
    xmom.d[:,:] = 0.0
    ymom.d[:,:] = 0.0
    dens.d[:,:] = 0.0

    # set the density to be stratified in the y-direction
    myg = my_data.grid

    p = myg.scratch_array()

    dens.d[:,:] = dens1*numpy.exp(-myg.y2d/scale_height)
    dens.d[dens.d < smalldens] = smalldens
    p.d[:,:] = dens.d * cs**2 / gamma

    # set the energy (P = cs2*dens)
    ener.d[:,:] = p.d[:,:]/(gamma - 1.0) + \
        0.5*(xmom.d[:,:]**2 + ymom.d[:,:]**2)/dens.d[:,:]


def finalize():
    """ print out any information to the user at the end of the run """
    pass
