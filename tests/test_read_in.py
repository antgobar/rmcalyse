#!/usr/bin/env python

"""Tests for `rmcalyse` package."""

import pytest

from click.testing import CliRunner

from rmcalyse import rmcalyse
from rmcalyse import cli
from rmcalyse.general_functions.read_rmc6f import read_in

def test_rmc6f_file_reader():
    # really simple (probably too simplistic!) pytest
    (cell, atoms) = read_in('tests/SrTiO3_00Nb.rmc6f')
    expected = [19.66995, 19.66995, 19.66995, 90.0, 90.0, 90.0]
    assert all(a == pytest.approx(b) for a,b in zip(cell, expected))
    assert len(atoms) == 625
