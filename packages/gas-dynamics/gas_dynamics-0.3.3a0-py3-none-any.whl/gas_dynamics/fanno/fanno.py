#!usr/bin/env
#Equations, plots, and tables for working with constant area flow
#subject to losses from friction, otherwise known as Fanno flow
#
#
#Copyright 2020 by Fernando A de la Fuente
#All rights reserved
from gas_dynamics.fluids import fluid, air
from numpy import log
from scipy.optimize import fsolve



#==================================================
#stagnation enthalpy
#==================================================
def stagnation_enthalpy(enthalpy: float, gas=air) -> float:
    """Return the stagnation enthalpy

    Notes
    -----
    Given the fluid state and a given enthalpy, return its stagnation
    enthalpy

    Parameters
    ----------
    enthalpy : `float`
        The enthalpy of the fluid
    gas : `fluid`
        A user defined fluid object

    Examples
    --------

    """

    ht = enthalpy + gas.mass_velocity**2 / (gas.rho**2 * 2 * gas.gc)
    return ht



#==================================================
#fanno temperature
#==================================================



#==================================================
#fanno pressure
#==================================================



#==================================================
#fanno temperature ratio
#==================================================
def fanno_temperature_ratio(M1: float, M2: float, gas=air) -> float:
    """Return the temperature ratio for a fanno flow given two Mach numbers

    Notes
    -----


    Parameters
    ----------
    M1 : `flaot`
        The mach number at region 1
    M2 : `float`
        The mach number at region 2
    
    Examples
    --------

    """
    gamma = gas.gamma
    T2_T1 = ( 1+ (gamma-1)/2 * M1**2)/( 1+ (gamma-1)/2 * M2**2)
    return T2_T1



#==================================================
#fanno pressure ratio
#==================================================
def fanno_pressure_ratio(M1: float, M2: float, gas=air) -> float:
    """Return the pressure ratio for a fanno flow given two Mach numbers

    Notes
    -----


    Parameters
    ----------
    M1 : `flaot`
        The mach number at region 1
    M2 : `float`
        The mach number at region 2
    
    Examples
    --------

    """
    gamma = gas.gamma
    rho2_rho1 = M1/M2 * (( 1+ (gamma-1)/2 * M1**2)/( 1+ (gamma-1)/2 * M2**2))**.5



#==================================================
#fanno density ratio
#==================================================
def fanno_density_ratio(M1: float, M2: float, gas=air) -> float:
    """Return the density ratio for a fanno flow given two Mach numbers

    Notes
    -----


    Parameters
    ----------
    M1 : `flaot`
        The mach number at region 1
    M2 : `float`
        The mach number at region 2
    
    Examples
    --------

    """
    gamma = gas.gamma
    rho2_rho1 = M1/M2 * (( 1+ (gamma-1)/2 * M2**2)/( 1+ (gamma-1)/2 * M1**2))**.5
    return rho2_rho1



#==================================================
#fanno stagnation pressure ratio
#==================================================
def fanno_stagnation_pressure_ratio(M1: float, M2: float, gas=air) -> float:
    """Return the stagnation pressure ratio pt2/pt1 for a fanno flow given two mach numbers

    Notes
    -----


    Parameters
    ----------
    M1 : `flaot`
        The mach number at region 1
    M2 : `float`
        The mach number at region 2
    
    Examples
    --------

    """
    gamma = gas.gamma
    pt2_pt1 = M1/M2 * (( 1+ (gamma-1)/2 * M2**2)/( 1+ (gamma-1)/2 * M1**2))**((gamma+1)/(2*(gamma-1)))
    return pt2_pt1



#==================================================
#fanno
#==================================================
def fanno_parameter(M1: float, M2: float, gas=air) -> float:
    """Return the product of friction factor and length divided by diameter for two Mach numbers

    Notes
    -----


    Parameters
    ----------
    M1 : `flaot`
        The mach number at region 1
    M2 : `float`
        The mach number at region 2
    
    Examples
    --------

    """
    gamma = gas.gamma
    fanno_ratio = gamma+1 / (2*gamma) * log((( 1+ (gamma-1)/2 * M2**2)/( 1+ (gamma-1)/2 * M1**2))) - 1/gamma * (1/(M2**2) - 1/(M1**2)) - (gamma+1)/(2*gamma) * log((M2**2)/(M1**2) )
    return fanno_ratio



#==================================================
#fanno parameter max
#==================================================
def fanno_parameter_max(M: float, gas=air) -> float:
    """Return the maximum product of friction factor and length divided by diameter

    Notes
    -----
    Given a mach number and a fluid, determine the maximum length to diameter ratio
    for a fluid to reach a Mach number of 1, or a condition of maximum entropy.

    Parameters
    ----------
    M : `float`
        The starting Mach number
    gas : `fluid`
        The user defined fluid object

    Examples
    --------
    
    """

    gamma = gas.gamma
    fanno_ratio_max = (gamma + 1)/(2*gamma) * log(((gamma+1)/2 * M**2) / (1 + (gamma+1)/2 * M**2)) + 1/gamma * (1/(M**2)-1)
    return fanno_ratio_max



#==================================================
#mach from fanno parameter
#==================================================
def mach_from_fanno(fanno: float, M1: float, gas=air) -> float:
    """Return the Mach number that would result from the fanno parameter and initial mach number

    Notes
    -----


    Parameters
    ----------
    fanno : `float`
        The fanno parameter for the system
    M : `float`
        The starting Mach number
    gas : `fluid`
        The user defined fluid object

    Examples
    --------
    

    """

    def mach_solve(M, M1=M1, fanno=fanno, gas=gas):
        zero = fanno_parameter(M1=M, M2=M1, gas=gas) - fanno
        return zero

    sol = fsolve(mach_solve, args=(M, fanno, gas), x0=1)
    return sol