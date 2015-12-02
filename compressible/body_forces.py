"""
compute body forces for this problem.
"""

import numpy as np
from raytrace import py_raytrace_grid

def compute(my_data, rp):
    myg = my_data.grid
    dens = my_data.get_var("density")
    grav = rp.get_param("compressible.grav")

    c = my_data.get_aux("speed_of_light")
    kappa = my_data.get_aux("opacity")
    I = my_data.get_aux("surface_brightness")

    nangles = myg.nx/2

    Fx = np.zeros((myg.nx,myg.ny))
    Fy = np.zeros((myg.nx,myg.ny))
    E = np.zeros((myg.nx,myg.ny))

    xmax = rp.get_param("mesh.xmax")
    ymax = rp.get_param("mesh.ymax")

    py_raytrace_grid(dens.v(),Fx,Fy,E,myg.nx,myg.ny,xmax,ymax,kappa,I,nangles)

    xacc = myg.scratch_array()
    yacc = myg.scratch_array()

    xacc.v()[:,:] = kappa*Fx/c
    yacc.v()[:,:] = grav + kappa*Fy/c

    # compute mass-weighted acceleration
    weighted_acc = yacc.v()*dens.v()
    mean_weighted_acc = np.sum(weighted_acc)/np.sum(dens.v())
    print("density-weighted net acceleration:",mean_weighted_acc)

    return xacc, yacc
