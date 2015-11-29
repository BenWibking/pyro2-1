"""
compute body forces for this problem.
"""

import numpy as np

def compute(my_data, rp):
    myg = my_data.grid
    dens = my_data.get_var("density")
    grav = rp.get_param("compressible.grav")

    xacc = myg.scratch_array()
    yacc = myg.scratch_array()

    xacc.v()[:,:] = 0.
    yacc.v()[:,:] = grav

    return xacc, yacc
