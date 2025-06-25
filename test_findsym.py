import pytest
import os
import sys
from unittest.mock import patch
import numpy as np

# Add the parent directory to sys.path to import findsym
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from findsym import findsym
from findsym.core import (
    parse_input,
    find_primitive_cell,
    identify_point_group,
    match_to_standard_space_group,
)


class TestFindsym:
    """Test suite for FINDSYM package."""

    def test_import(self):
        """Test that the package imports correctly."""
        import findsym

        assert hasattr(findsym, "findsym")
        assert hasattr(findsym, "main")
        assert hasattr(findsym, "__version__")

    def test_version(self):
        """Test that version is accessible."""
        from findsym import __version__

        assert __version__ == "0.1.1"

    @pytest.mark.skipif(
        not os.path.exists("SrTiO3_mp-4651_primitive.cif"),
        reason="Test CIF file not found",
    )
    def test_parse_input_cif(self):
        """Test parsing CIF files."""
        if os.path.exists("SrTiO3_mp-4651_primitive.cif"):
            structure = parse_input("SrTiO3_mp-4651_primitive.cif")
            assert structure is not None
            assert len(structure) > 0

    def test_core_functions_exist(self):
        """Test that core functions are available."""
        from findsym.core import (
            parse_input,
            denoise_structure,
            find_primitive_cell,
            identify_point_group,
            find_space_group_operators,
            match_to_standard_space_group,
            assign_wyckoff_positions,
            print_text_output,
        )

        # Just check they exist
        assert callable(parse_input)
        assert callable(denoise_structure)
        assert callable(find_primitive_cell)
        assert callable(identify_point_group)
        assert callable(find_space_group_operators)
        assert callable(match_to_standard_space_group)
        assert callable(assign_wyckoff_positions)
        assert callable(print_text_output)

    def test_main_function_help(self):
        """Test that main function shows help when needed."""
        with patch("sys.argv", ["findsym", "--help"]):
            with pytest.raises(SystemExit):
                from findsym import main

                main()

    def test_main_function_version(self):
        """Test that main function shows version."""
        with patch("sys.argv", ["findsym", "--version"]):
            with pytest.raises(SystemExit):
                from findsym import main

                main()


if __name__ == "__main__":
    pytest.main([__file__])
