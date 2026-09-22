"""Smoke tests for the NiceGUI GUI layer.

These are skipped automatically if nicegui is not installed (it is an optional
dependency, see requirements-gui.txt).
"""
import importlib

import pytest

pytest.importorskip("nicegui")


def test_gui_imports_without_launching():
    """Importing gui builds the UI but must not start the server."""
    gui = importlib.import_module("gui")
    assert hasattr(gui, "build_ui")
    assert hasattr(gui, "_generate_values")


def test_generate_values_uses_core():
    gui = importlib.import_module("gui")
    # UUID type (18) ignores length/batch/encoding
    out = gui._generate_values(18, 0, False, 'random', 1, False, 'none')
    assert len(out) == 1
    import uuid
    uuid.UUID(out[0])  # raises if not a valid UUID


def test_generate_values_unique_batch():
    gui = importlib.import_module("gui")
    out = gui._generate_values(19, 0, False, 'visa', 5, True, 'none')
    assert len(out) == len(set(out))
    assert all(v.startswith('4') for v in out)
