# FINDSYM: Crystal Structure Symmetry Detection

FINDSYM is a Python package for detecting and analyzing crystal structure symmetries. It provides tools to identify space groups, point groups, and Wyckoff positions in crystalline materials.

## Features

- **Space Group Detection**: Automatically identifies the space group of crystal structures
- **Point Group Analysis**: Determines the point group symmetries
- **Wyckoff Position Assignment**: Assigns atoms to their corresponding Wyckoff positions
- **Primitive Cell Finding**: Converts structures to their primitive cells
- **3D Visualization**: Interactive visualization of crystal structures (optional)
- **Multiple File Formats**: Supports CIF, POSCAR, XYZ, and other common structure formats

## Installation

### From PyPI (recommended)

```bash
pip install findsym
```

### With visualization support

```bash
pip install findsym[visualization]
```

### From source

```bash
git clone https://github.com/yourusername/findsym.git
cd findsym
pip install -e .
```

## Dependencies

- `numpy` >= 1.18.0
- `ase` >= 3.20.0 (Atomic Simulation Environment)
- `spglib` >= 1.16.0 (Space group library)
- `matplotlib` >= 3.3.0 (optional, for visualization)

## Quick Start

### Command Line Usage

```bash
# Basic symmetry analysis
findsym structure.cif

# With custom tolerance
findsym structure.cif --tolerance 1e-4

# With 3D visualization
findsym structure.cif --visualize
```

### Python API

```python
from findsym import findsym

# Analyze a crystal structure
result = findsym("SrTiO3.cif", tolerance=1e-3, visualize=True)

print(f"Space group number: {result['number']}")
print(f"Point group: {result['point group']}")
```

## Examples

### Analyzing SrTiO3

```python
import findsym

# Load and analyze SrTiO3 structure
result = findsym.findsym("SrTiO3_mp-4651_primitive.cif")

# Output will show:
# - Space group information
# - Standardized lattice parameters
# - Wyckoff positions for each atom
# - Symmetry operations
```

### Batch Processing

```python
import glob
from findsym import findsym

# Process multiple structures
for cif_file in glob.glob("*.cif"):
    print(f"Processing {cif_file}...")
    result = findsym(cif_file)
    print(f"Space group: {result['number']}")
```

## Output Information

FINDSYM provides detailed symmetry information including:

- **Space Group**: International symbol and number
- **Point Group**: Point group symbol
- **Lattice Parameters**: Standardized unit cell
- **Wyckoff Positions**: Site symmetries for each atom
- **Symmetry Operations**: Complete set of symmetry transformations
- **Equivalent Atoms**: Grouping of symmetrically equivalent atoms

## Supported File Formats

- CIF (Crystallographic Information File)
- POSCAR/CONTCAR (VASP)
- XYZ
- PDB
- And many others supported by ASE

## Visualization

When using the `--visualize` flag or `visualize=True` parameter, FINDSYM creates an interactive 3D plot showing:

- Crystal structure with atoms colored by element
- Unit cell boundaries
- Proper atomic radii
- Structure information overlay

## Advanced Usage

### Custom Tolerance

```python
# For high-precision structures
result = findsym("precise_structure.cif", tolerance=1e-5)

# For experimental/noisy data
result = findsym("experimental_structure.cif", tolerance=1e-2)
```

### Programmatic Access

```python
from findsym.core import (
    parse_input,
    find_primitive_cell,
    identify_point_group,
    match_to_standard_space_group
)

# Load structure
structure = parse_input("structure.cif")

# Find primitive cell
primitive = find_primitive_cell(structure)

# Get space group
dataset = match_to_standard_space_group(primitive, tolerance=1e-3)
print(f"Space group: {dataset['international']}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the original [FINDSYM](https://stokes.byu.edu/iso/findsymform.php) from BYU's [Isotropy Software Suite](https://stokes.byu.edu/iso/isotropy.php)
- Built on top of [spglib](https://spglib.github.io/spglib/) for symmetry operations
- Uses [ASE](https://wiki.fysik.dtu.dk/ase/) for structure handling
- Visualization powered by [matplotlib](https://matplotlib.org/)
