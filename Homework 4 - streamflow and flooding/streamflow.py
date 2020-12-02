# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 00:35:50 2020

@author: Brian Chung
The purpose of this module is to calculate/model streamflow
"""

# %%
"""The Soil Conservation Service Curve Number method. This method calculates
direct runoff aka rainfall excess aka effective rainfall (P*) aka event flow
volume (Q*). This method seems to have come from the Soil Conservation Service,
which is formerly a wing under the USDA and is now called the Natural Resources
Conservation Service"""


def initialAbstraction(S):
    """Calculates the initial abstraction (Ia)

    Parameters
    ----------
    S : float or numpy array
        Potential max retention, which is the total amount of water that a soil
        can hold (inches)

    Returns
    -------
    Ia = initial abstraction; the initial infiltrated amount (inches)

    """
    Ia = 0.2*S
    return Ia


def potentialMaxRetention(CN):
    """Calculates the potential max retention, which is the total amount of
    water that a soil can hold (inches)

    Parameters
    ----------
    CN : float, int, or numpy array
        The curve number, which is a number that represents soil properties.
        Curve numbers are also used to described paved surfaces as well.

    Returns
    -------
    S : float or numpy array
        Potential max retention, which is the total amount of water that a soil
        can hold (inches)

    """
    S = (1000/CN) - 10
    return S


def QfromIa_S_P(Ia, S, P):
    """Calculates runoff using the initial abstraction (Ia), the potential max
    retention (S), and the precipitation (P)

    Parameters
    ----------
    Ia : float or numpy array
        initial abstraction; the initial infiltrated amount (inches)
    S : float or numpy array
        Potential max retention, which is the total amount of water that a soil
        can hold (inches)
    P : float or numpy array
        rainfall amount (inches)

    Returns
    -------
    Q : float or numpy array
        direct runoff amount (inches)

    """
    numerator = (P - Ia)**2
    denominator = P - Ia + S
    Q = numerator/denominator
    return Q


def QfromS_P(S, P):
    """Calculates runoff using the potential max retention (S), and
    precipitation (P)

    Parameters
    ----------
    S : float or numpy array
        Potential max retention, which is the total amount of water that a soil
        can hold (inches)
    P : float or numpy array
        rainfall amount (inches)

    Returns
    -------
    Q : float or numpy array
        direct runoff amount (inches)

    """
    numerator = (P - (0.2*S))**2
    denominator = P + (0.8*S)
    Q = numerator/denominator
    return Q


def QfromP_CN(P, CN):
    """Calculates runoff using precipitation (P) and the curve number (CN).

    Parameters
    ----------
    P : float or numpy array
        rainfall amount (inches)
    CN : float, int, or numpy array
        The curve number, which is a number that represents soil properties.
        Curve numbers are also used to described paved surfaces as well.

    Returns
    -------
    Q : float or numpy array
        direct runoff amount (inches)

    """
    numerator = P - (200/CN) + 2
    denominator = P + (800/CN) - 8
    Q = numerator/denominator
    return Q
