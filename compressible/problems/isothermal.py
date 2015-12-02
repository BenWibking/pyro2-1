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

    eddington_ratio = rp.get_param("isothermal.eddington")

    dens1 = rp.get_param("isothermal.dens1")

    amp = rp.get_param("isothermal.amp")
    nwaves = rp.get_param("isothermal.nwaves")

    xmax = rp.get_param("mesh.xmax")
    ymax = rp.get_param("mesh.ymax")

    if grav_const != 0.0:
        scale_height = cs*cs/numpy.abs(grav_const)
    else:
        scale_height = 0.1

    print("scale height:",scale_height)

    smallpres = 1.e-10
    smalldens = smallpres/(cs**2)

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

    # compute optical depth
    kappa = 1.0
    c = 1.0
    column_density = dens1*scale_height*(1.0-numpy.exp(-ymax))
    optical_depth = column_density*kappa
    I_0 = (1./numpy.pi)*eddington_ratio*c*numpy.abs(grav_const) \
        *column_density/(1.0-numpy.exp(-optical_depth))
    my_data.set_aux("surface_brightness", I_0)
    my_data.set_aux("speed_of_light", c)
    my_data.set_aux("opacity",kappa)
    print("optical depth:",optical_depth)
    print("surface brightness:",I_0)

    # compute Eddington ratio
    rad_accel = (numpy.pi*I_0)*kappa/c* \
        (1.0-numpy.exp(-optical_depth))/optical_depth \
        # mass weighted flux (plane-parallel radiation, constant kappa)
    net_accel = rad_accel + grav_const
    eddington_ratio = rad_accel/numpy.abs(grav_const)
    print("eddington_ratio:",eddington_ratio)
    print("net accel:",net_accel)

    # set the velocity perturbations
    u = 0.

    A = amp*numpy.random.rand(dens.d.shape[0],dens.d.shape[1])
#    v = A*(1+numpy.cos(nwaves*numpy.pi*myg.x2d/xmax))*0.5
    v = A*(numpy.cos(nwaves*numpy.pi*myg.x2d/xmax))*0.5

    # set the momenta
    xmom.d[:,:] = dens.d * u
    ymom.d[:,:] = dens.d * v

    # set the energy (P = cs2*dens/gamma)
    ener.d[:,:] = p.d[:,:]/(gamma - 1.0) + \
        0.5*(xmom.d[:,:]**2 + ymom.d[:,:]**2)/dens.d[:,:]


def finalize():
    """ print out any information to the user at the end of the run """
    pass
