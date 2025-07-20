# Import Libraries
import numpy as np
import pandas as pd
import openseespy.opensees as ops
import os

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
        self.Vs  = 100
        self.rho = 1.7
        self.nu = 0
        self.cohesion = 95.0
        self.peakStrain = 0.05
        self.ref_press = 100
        self.rock_Vs = 760
        self.soilDepth = 30

        if params_dict:
            self.update_params(**params_dict)
