# OpenSeesPy Soil Structure Interaction Analysis

This project provides a Python implementation for soil-structure interaction analysis using OpenSeesPy. The code has been refactored using object-oriented programming principles for better organization and maintainability.

## Features

- **Parameter Management**: Clean OOP implementation for analysis parameters
- **Material Modeling**: Advanced soil material properties with derived mechanical properties
- **Mesh Generation**: Automatic calculation of mesh parameters based on wave propagation requirements
- **Dynamic Analysis**: Complete workflow from gravity application to dynamic loading

## Parameter Classes

### `BaseParams`
The foundation class providing core parameter management functionality:
- `update_params()`: Update multiple parameters with validation
- `get_params_dict()`: Export parameters to dictionary
- `set_from_dict()`: Initialize from dictionary

### `MaterialParams`
Manages soil and rock material properties including:
- Basic properties (Vs, ρ, ν, cohesion)
- Rock properties (rock_Vs, rockDen)
- Derived properties (G, E, K)
- Geometry (soilDepth)

### `MeshParams`
Handles finite element mesh configuration:
- Frequency resolution (f_max)
- Wave-based element sizing
- Node and element calculations
- Automatic mesh density determination

### `AnalysisParams`
Controls numerical analysis parameters:
- Newmark integration (γ, β)
- Rayleigh damping (a₀, a₁)
- Time stepping (dt, steps)
- File paths for I/O

## Usage Example

```python
# Initialize parameters
mat_params = MaterialParams({
    'Vs': 250,
    'rho': 1.7,
    'soilDepth': 30.0
})

mesh_params = MeshParams(mat_params)
analysis_params = AnalysisParams()

# Access parameters
print(f"Element size: {mesh_params.eleSize}")
print(f"Damping coefficients: a0={analysis_params.a0}")
