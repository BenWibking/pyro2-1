"""
compute body forces for this problem.
"""

import numpy as np
from raytrace import py_raytrace_grid

def compute(my_data, rp):
    myg = my_data.grid
    dens = my_data.get_var("density")
    grav = rp.get_param("compressible.grav")

    c = 1.0
    kappa = 1.0
    I = 0.5

    nangles = myg.nx/2

    Fx = np.zeros((myg.nx,myg.ny))
    Fy = np.zeros((myg.nx,myg.ny))

    xmax = rp.get_param("mesh.xmax")
    ymax = rp.get_param("mesh.ymax")

    py_raytrace_grid(dens.v(),Fx,Fy,myg.nx,myg.ny,xmax,ymax,kappa,I,nangles)

    xacc = myg.scratch_array()
    yacc = myg.scratch_array()

    xacc.v()[:,:] = kappa*Fx/c
    yacc.v()[:,:] = grav + kappa*Fy/c

    return xacc, yacc
