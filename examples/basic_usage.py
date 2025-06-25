#!/usr/bin/env python3
"""
Basic example of using FINDSYM to analyze crystal structure symmetries.
"""

import os

import findsym


def basic_analysis_example():
    """Basic symmetry analysis example."""
    print("=== Basic FINDSYM Example ===")

    # Check if example structure file exists
    cif_file = "SrTiO3_mp-4651_primitive.cif"
    if not os.path.exists(cif_file):
        print(f"Warning: {cif_file} not found. Please provide a structure file.")
        return

    print(f"Analyzing structure: {cif_file}")

    # Perform symmetry analysis
    result = findsym.findsym(cif_file)

    print("\nResults:")
    print(f"  Space group number: {result.get('number', 'Unknown')}")
    print(f"  Point group: {result.get('point group', 'Unknown')}")
    print(
        f"  Number of symmetry operations: {len(result.get('symmetry', {}).get('rotations', []))}"
    )

    return result


def visualization_example():
    """Example with 3D visualization."""
    print("\n=== Visualization Example ===")

    cif_file = "SrTiO3_mp-4651_primitive.cif"
    if not os.path.exists(cif_file):
        print(f"Warning: {cif_file} not found. Please provide a structure file.")
        return

    print(f"Analyzing structure with visualization: {cif_file}")
    print("Note: This will open an interactive 3D plot window.")

    # Perform analysis with visualization
    result = findsym.findsym(cif_file, tolerance=1e-3, visualize=True)

    return result


def batch_processing_example():
    """Example of processing multiple structures."""
    print("\n=== Batch Processing Example ===")

    import glob

    # Find all CIF files in current directory
    cif_files = glob.glob("*.cif")

    if not cif_files:
        print("No CIF files found in current directory.")
        return

    results = {}

    for cif_file in cif_files:
        print(f"\nProcessing: {cif_file}")
        try:
            result = findsym.findsym(cif_file, tolerance=1e-3, visualize=False)
            results[cif_file] = result
            print(f"  Space group: {result.get('number', 'Unknown')}")
        except Exception as e:
            print(f"  Error: {e}")
            results[cif_file] = None

    return results


if __name__ == "__main__":
    # Run basic example
    basic_analysis_example()

    # Uncomment to run visualization example
    # visualization_example()

    # Uncomment to run batch processing example
    # batch_processing_example()
