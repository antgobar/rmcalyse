#!/usr/bin/env python

"""Tests for `rmcalyse` package."""

import pytest

from click.testing import CliRunner

from rmcalyse import rmcalyse
from rmcalyse import cli
from rmcalyse.general_functions.supercell_class import SuperCell

def test_SuperCell():
    # testing
    file_path = 'tests/STO_2.rmc6f'
    expected_cell_parameters = [8, 8, 8, 90.0, 90.0, 90.0]
    expected_density = [0.078125]

    rmc_data = SuperCell(file_path)
    rmc_data.get_data()

    cell_parameters = rmc_data.cell_parameters
    density =  rmc_data.density

    assert expected_cell_parameters == cell_parameters
    assert expected_density == density
 
