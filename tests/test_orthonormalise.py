#!/usr/bin/env python

"""Tests for `rmcalyse` package."""

import pytest

from click.testing import CliRunner

from rmcalyse import rmcalyse
from rmcalyse import cli
from rmcalyse.general_functions.orthonormalise import orthonormalise

def test_orthonormalise():
    # testing
    cell = [4, 4, 4, 90.0, 60.0, 90.0]
    atom_list = [['Sr', 1, 0.0, 0.0, 0.0], ['Sr', 2, 0.5, 0.5, 0.5]]
    orthonormal_positions = orthonormalise(cell, atom_list)
    orthonormal_positions[1][-1] = round(orthonormal_positions[1][-1],3)
    expected = [['Sr', 1, 0.0, 0.0, 0.0], ['Sr', 2, 3, 2, 1.732]]
    assert expected == orthonormal_positions
 
