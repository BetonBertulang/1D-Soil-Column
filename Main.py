# Import Libraries
import numpy as np
import pandas as pd
import openseespy.opensees as ops
import os
from math import ceil, pi

# PARAMETERS CLASSES
class BaseParams:
    """A base class for parameter management."""
    def update_params(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' has no parameter '{key}'")
    
    def get_params_dict(self):
        """Get all parameters as dictionary, excluding private attributes"""
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_') and not callable(value)}
    
    def set_from_dict(self, params_dict):
        """Alternative method specifically for dictionary input"""
        self.update_params(**params_dict)



class MaterialParams(BaseParams):
    '''Manages material properties for soil and rock'''
    def __init__(self, params_dict=None):
        # Soil properties
        self.Vs = 100          # Shear wave velocity [m/s]
        self.rho = 1.7         # Density [Mg/m³]
        self.nu = 0            # Poisson's ratio
        self.cohesion = 95.0   # Cohesion [kPa]
        self.peakStrain = 0.05 # Peak shear strain
        self.ref_press = 100   # Reference pressure [kPa]
        self.frictionAng = 0.0 # Friction angle [degrees]
        self.pressDependCoe = 0.0 # Pressure dependency coefficient
        
        # Rock properties
        self.rock_Vs = 760     # Rock shear wave velocity [m/s]
        self.rockDen = 2.4     # Rock density [Mg/m³]
        
        # Geometry
        self.soilDepth = 30    # Soil depth [m]
        
        # Initialize derived properties
        self.update_derived_properties()

        if params_dict:
            self.update_params(**params_dict)
    
    def update_derived_properties(self):
        '''Calculate derived mechanical properties'''
        self.G = self.rho * self.Vs**2       # Shear modulus [kN/m²]
        self.E = 2 * self.G * (1 + self.nu)   # Young's modulus [kN/m²]
        self.K = self.E / (3*(1 - 2*self.nu)) # Bulk modulus [kN/m²]

class MeshParams(BaseParams):
    '''Manages the finite element mesh properties for the soil domain.'''
    def __init__(self, mat_params):
        self.f_max = 25.0
        self.ele_per_wave = 4
        self.node_start = 1
        self.calculate_mesh_parameters(mat_params)
    
    def calculate_mesh_parameters(self,mat_params):
        """Calculate mesh parameters based on material properties"""
        wavelength = mat_params.Vs / self.f_max
        hTrial = wavelength / self.ele_per_wave

        # Calculate trial element size based on wavelength resolution requirements
        self.numEle = ceil(mat_params.soilDepth / hTrial)
        self.eleSize = mat_params.soilDepth / self.numEle

        self.numNodeY = 2 * (self.numEle + 1)
        self.sizeEleX = self.eleSize

class AnalysisParams(BaseParams):
    '''Manages parameters for numerical analysis.'''
    def __init__(self):
        self.gamma = 0.5
        self.beta = 0.25
        self.damp = 0.02
        self.motion_dt = 0.005
        self.motion_steps = 7990
        self.ground_motion_file = 'velocityHistory.out'
        self.update_damping()
    
    def update_damping(self):
        omega1 = 2 * pi * 0.2
        omega2 = 2 * pi * 20
        self.a0 = 2 * self.damp * omega1 * omega2 / (omega1 + omega2)
        self.a1 = 2 * self.damp / (omega1 + omega2)

