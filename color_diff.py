# The functions in this module are used for comparing two LabColor objects
# using various Delta E formulas

# Adapted from colormath.color_diff https://python-colormath.readthedocs.io/en/latest/_modules/colormath/color_diff.html
# as it was rendered useless by deprecated function numpy.asscalar()


import numpy as np
from colormath import color_diff_matrix


# Converts an LabColor into a NumPy vector
def _get_lab_color1_vector(color):
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return np.array([color.lab_l, color.lab_a, color.lab_b])


# Converts an LabColor into a NumPy matrix
def _get_lab_color2_matrix(color):
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return np.array([(color.lab_l, color.lab_a, color.lab_b)])


# Calculates the Delta E (CIE1976) of two colors
def delta_e_cie1976(color1, color2):
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie1976(color1_vector, color2_matrix)[0]
    # return numpy.asscalar(delta_e)
    return delta_e.item()


# Calculates the Delta E (CIE1994) of two colors
## K_l:
##      0.045 graphic arts
##      0.048 textiles
## K_2:
##      0.015 graphic arts
##      0.014 textiles
## K_L:
##      1 default
##      2 textiles
def delta_e_cie1994(color1, color2, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie1994(
        color1_vector, color2_matrix, K_L=K_L, K_C=K_C, K_H=K_H, K_1=K_1, K_2=K_2)[0]
    # return numpy.asscalar(delta_e)
    return delta_e.item()


# Calculates the Delta E (CIE2000) of two colors
def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie2000(
        color1_vector, color2_matrix, Kl=Kl, Kc=Kc, Kh=Kh)[0]
    # return numpy.asscalar(delta_e)
    return delta_e.item()


# Calculates the Delta E (CMC) of two colors.
##    CMC values
##      Acceptability: pl=2, pc=1
##      Perceptability: pl=1, pc=1
def delta_e_cmc(color1, color2, pl=2, pc=1):
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cmc(
        color1_vector, color2_matrix, pl=pl, pc=pc)[0]
    # return numpy.asscalar(delta_e)
    return delta_e.item()