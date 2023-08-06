#!/usr/bin/env python

"""Tests for `mp3_combine_and_split` package."""

import pytest

from click.testing import CliRunner

from slugify import slugify
from mp3_combine_and_split import cli


def test_safe_filename():
    """Sample pytest test function with the pytest fixture as an argument."""
    sample_filename = "Roald Dahl/Stephen Mangan/Tamsin Greig-Revolting Rhymes & Dirty Beasts-1"
    safe_sample_filename = slugify(sample_filename)
    assert safe_sample_filename == "roald-dahl-stephen-mangan-tamsin-greig-revolting-rhymes-dirty-beasts-1"


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output
