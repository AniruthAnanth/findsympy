"""
FINDSYM: Crystal Structure Symmetry Detection

A Python package for detecting and analyzing crystal structure symmetries.
"""

import argparse

from ._version import __version__
from .core import findsym

__all__ = ["findsym", "main", "__version__"]


def main():
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        description="FINDSYM: Symmetry detection for crystal structures.",
        epilog="For more information, visit: https://github.com/yourusername/findsym",
    )
    parser.add_argument(
        "input_file", help="Input structure file (CIF, POSCAR, XYZ, etc.)"
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-3,
        help="Symmetry detection tolerance (default: 1e-3)",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Show 3D visualization of crystal structure",
    )
    parser.add_argument("--version", action="version", version=f"FINDSYM {__version__}")

    args = parser.parse_args()

    try:
        result = findsym(args.input_file, args.tolerance, args.visualize)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
