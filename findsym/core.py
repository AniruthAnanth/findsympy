import sys

import numpy as np
from ase import Atoms
from ase.io import read
from spglib import find_primitive, get_symmetry, get_symmetry_dataset

try:
    import matplotlib.pyplot as plt
    from ase.build import make_supercell
    from mpl_toolkits.mplot3d import Axes3D

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    plt = None
    make_supercell = None


def parse_input(filename):
    """Parse structure from file using ASE."""
    try:
        structure = read(filename)
        return structure
    except Exception as e:
        print(f"Error reading structure: {e}")
        sys.exit(1)


def denoise_structure(structure):
    """Simple denoising: center and symmetrize positions (placeholder)."""
    # Center structure
    structure.center()
    # Optionally, more advanced denoising can be added here
    return structure


def find_primitive_cell(structure):
    """Find primitive cell using spglib."""
    lattice = structure.get_cell()
    positions = structure.get_scaled_positions()
    numbers = structure.get_atomic_numbers()
    cell = (lattice, positions, numbers)
    primitive = find_primitive(cell)
    if primitive is None:
        return structure
    prim_lattice, prim_positions, prim_numbers = primitive
    return Atoms(
        numbers=prim_numbers,
        cell=prim_lattice,
        scaled_positions=prim_positions,
        pbc=True,
    )


def identify_point_group(structure):
    """Identify point group using spglib."""
    lattice = structure.get_cell()
    positions = structure.get_scaled_positions()
    numbers = structure.get_atomic_numbers()
    cell = (lattice, positions, numbers)
    dataset = get_symmetry_dataset(cell)
    return dataset.pointgroup if dataset else None


def find_space_group_operators(structure, tolerance):
    """Find space group operators using spglib."""
    lattice = structure.get_cell()
    positions = structure.get_scaled_positions()
    numbers = structure.get_atomic_numbers()
    cell = (lattice, positions, numbers)
    symmetry = get_symmetry(cell, symprec=tolerance)
    return symmetry


def match_to_standard_space_group(structure, tolerance):
    """Match to standard space group using spglib."""
    lattice = structure.get_cell()
    positions = structure.get_scaled_positions()
    numbers = structure.get_atomic_numbers()
    cell = (lattice, positions, numbers)
    dataset = get_symmetry_dataset(cell, symprec=tolerance)
    return dataset


def assign_wyckoff_positions(structure, dataset):
    """Assign Wyckoff positions from spglib dataset."""
    wyckoffs = dataset.get("wyckoffs", [])
    equivalent_atoms = dataset.get("equivalent_atoms", [])
    return wyckoffs, equivalent_atoms


def print_text_output(dataset, wyckoffs, equivalent_atoms):
    print("Identified Space Group:")
    print(f"  Number: {dataset['number']}")
    print(f"  Symbol: {dataset['international']}")
    print("Standardized Lattice (Angstrom):")
    print(np.array2string(dataset["std_lattice"], precision=4))
    print("Wyckoff Positions:")
    for i, (w, eq) in enumerate(zip(wyckoffs, equivalent_atoms)):
        print(f"  Atom {i}: Wyckoff {w}, Equivalent atom index: {eq}")


def render_3D_visualization(structure, dataset, symmetry):
    """Visualize the crystal structure using interactive matplotlib 3D plot."""
    if not HAS_MATPLOTLIB or plt is None:
        print("Matplotlib not available. Please install with: pip install matplotlib")
        return

    print("Opening 3D visualization of the crystal structure...")
    print("Structure information:")
    print(f"  Formula: {structure.get_chemical_formula()}")
    print(f"  Number of atoms: {len(structure)}")
    print(f"  Space group: {dataset['international']} (#{dataset['number']})")

    # Create a supercell for better visualization if the structure is small
    if len(structure) < 20 and make_supercell is not None:
        # Create a 2x2x2 supercell for better visualization
        supercell_matrix = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
        structure_vis = make_supercell(structure, supercell_matrix)
        print(
            f"  Showing 2x2x2 supercell with {len(structure_vis)} atoms for better visualization"
        )
    else:
        structure_vis = structure

    try:
        # Create the 3D plot
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection="3d")

        # Get atomic positions and symbols
        positions = structure_vis.get_positions()
        symbols = structure_vis.get_chemical_symbols()

        # Define colors for different elements
        element_colors = {
            "H": "white",
            "He": "cyan",
            "Li": "violet",
            "Be": "green",
            "B": "brown",
            "C": "black",
            "N": "blue",
            "O": "red",
            "F": "green",
            "Ne": "cyan",
            "Na": "violet",
            "Mg": "green",
            "Al": "gray",
            "Si": "blue",
            "P": "orange",
            "S": "yellow",
            "Cl": "green",
            "Ar": "cyan",
            "K": "violet",
            "Ca": "green",
            "Sc": "gray",
            "Ti": "gray",
            "V": "gray",
            "Cr": "gray",
            "Mn": "gray",
            "Fe": "orange",
            "Co": "gray",
            "Ni": "gray",
            "Cu": "brown",
            "Zn": "gray",
            "Sr": "green",
            "Ba": "green",
            "default": "purple",
        }

        # Define sizes for different elements (scaled for visualization)
        element_sizes = {
            "H": 30,
            "He": 30,
            "Li": 100,
            "Be": 60,
            "B": 80,
            "C": 70,
            "N": 65,
            "O": 60,
            "F": 50,
            "Ne": 40,
            "Na": 150,
            "Mg": 120,
            "Al": 110,
            "Si": 100,
            "P": 95,
            "S": 90,
            "Cl": 85,
            "Ar": 80,
            "K": 180,
            "Ca": 160,
            "Sc": 140,
            "Ti": 130,
            "V": 125,
            "Cr": 120,
            "Mn": 115,
            "Fe": 110,
            "Co": 105,
            "Ni": 100,
            "Cu": 110,
            "Zn": 120,
            "Sr": 180,
            "Ba": 200,
            "default": 100,
        }

        # Plot atoms
        plotted_elements = set()
        for i, (pos, symbol) in enumerate(zip(positions, symbols)):
            color = element_colors.get(symbol, element_colors["default"])
            atom_size = element_sizes.get(symbol, element_sizes["default"])
            label = symbol if symbol not in plotted_elements else ""
            if symbol not in plotted_elements:
                plotted_elements.add(symbol)
            ax.scatter(
                pos[0],
                pos[1],
                pos[2],
                c=color,
                s=atom_size,
                alpha=0.8,
                edgecolors="black",
                linewidth=0.5,
                label=label,
            )

        # Draw unit cell
        if structure_vis.cell is not None and not np.allclose(structure_vis.cell, 0):
            cell = structure_vis.cell

            # Define the 8 corners of the unit cell
            corners = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0],  # bottom face
                    [0, 0, 1],
                    [1, 0, 1],
                    [1, 1, 1],
                    [0, 1, 1],  # top face
                ]
            )

            # Transform corners to Cartesian coordinates
            corners_cart = corners @ cell

            # Define the 12 edges of the unit cell
            edges = [
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0),  # bottom face
                (4, 5),
                (5, 6),
                (6, 7),
                (7, 4),  # top face
                (0, 4),
                (1, 5),
                (2, 6),
                (3, 7),  # vertical edges
            ]

            # Draw edges
            for edge in edges:
                start, end = corners_cart[edge[0]], corners_cart[edge[1]]
                ax.plot(
                    [start[0], end[0]],
                    [start[1], end[1]],
                    [start[2], end[2]],
                    "k-",
                    alpha=0.3,
                    linewidth=1,
                )

        # Set labels and title
        ax.set_xlabel("X (Å)")
        ax.set_ylabel("Y (Å)")
        ax.set_zlabel("Z (Å)")
        ax.set_title(
            f'{structure_vis.get_chemical_formula()}\nSpace Group: {dataset["international"]} (#{dataset["number"]})',
            fontsize=14,
            fontweight="bold",
        )

        # Add legend for unique elements
        if plotted_elements:
            ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98))

        # Set equal aspect ratio
        max_range = (
            np.array(
                [
                    positions[:, 0].max() - positions[:, 0].min(),
                    positions[:, 1].max() - positions[:, 1].min(),
                    positions[:, 2].max() - positions[:, 2].min(),
                ]
            ).max()
            / 2.0
        )
        mid_x = (positions[:, 0].max() + positions[:, 0].min()) * 0.5
        mid_y = (positions[:, 1].max() + positions[:, 1].min()) * 0.5
        mid_z = (positions[:, 2].max() + positions[:, 2].min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        # Add some text information
        info_text = f"Atoms: {len(structure_vis)}\nFormula: {structure_vis.get_chemical_formula()}\nSpace Group: {dataset['international']}"
        ax.text2D(
            0.02,
            0.02,
            info_text,
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7),
        )

        # Show the plot
        plt.tight_layout()
        print("Interactive 3D plot opened. You can:")
        print("  - Rotate: Click and drag")
        print("  - Zoom: Mouse wheel or right-click drag")
        print("  - Pan: Shift + click and drag")
        print("  - Close the window when done viewing")

        plt.show()

    except Exception as e:
        print(f"Failed to create 3D visualization: {e}")
        print("Make sure matplotlib is properly installed with 3D support")

    return structure_vis


def findsym(input_file, tolerance=1e-3, visualize=False):
    structure = parse_input(input_file)
    structure = denoise_structure(structure)
    primitive_cell = find_primitive_cell(structure)
    point_group = identify_point_group(primitive_cell)
    symmetry = find_space_group_operators(primitive_cell, tolerance)
    dataset = match_to_standard_space_group(primitive_cell, tolerance)
    wyckoffs, equivalent_atoms = assign_wyckoff_positions(primitive_cell, dataset)
    print_text_output(dataset, wyckoffs, equivalent_atoms)
    if visualize:
        render_3D_visualization(primitive_cell, dataset, symmetry)
    return {
        "number": dataset.number if dataset else None,
        "point group": point_group,
        "symmetry": symmetry,
        "wyckoff sites": wyckoffs,
        "equivalent atoms": equivalent_atoms,
    }
