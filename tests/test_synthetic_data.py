# tests/test_synthetic_data.py
"""
Unit tests for rosdl.core.synthetic_data
Ensures synthetic data generation, augmentation, and prompt parsing all work.
"""

import os
import json
import tempfile
import pandas as pd
from rosdl import data_generator as sd


def test_generate_from_schema():
    """Test schema-based generation and CSV save"""
    schema = [
        {"name": "pid", "type": "int", "min": 1000, "max": 9999},
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int", "min": 18, "max": 60},
        {"name": "salary", "type": "float", "min": 30000, "max": 120000},
        {"name": "city", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "join_date", "type": "date", "start": "2020-01-01", "end": "2024-12-31"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "schema_test.csv")
        output_file = sd.generate_from_schema(schema, 50, out_path)

        # Validate file creation
        assert os.path.exists(output_file), "CSV not created from schema"

        df = pd.read_csv(output_file)
        assert len(df) == 50, "Row count mismatch"
        assert all(col['name'] in df.columns for col in schema), "Column mismatch"


def test_generate_from_prompt():
    """Test text prompt-based generation"""
    prompt = "50 rows, columns: age int 20-50, gender category M/F, salary float 20000-80000, join date 2020-01-01:2023-12-31"
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "prompt_test.csv")
        output_file = sd.generate_from_prompt(prompt, out_path)

        assert os.path.exists(output_file), "CSV not created from prompt"
        df = pd.read_csv(output_file)
        assert len(df) == 50, "Row count mismatch from prompt"
        assert "age" in df.columns and "salary" in df.columns, "Expected columns missing"


def test_augment_dataset():
    """Test dataset augmentation"""
    # Create base dataset
    df = pd.DataFrame({
        "pid": [10001, 10002, 10003],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["Mumbai", "Delhi", "Goa"]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = os.path.join(tmpdir, "base.csv")
        df.to_csv(base_path, index=False)

        output_file = sd.augment_dataset(base_path, n_add=5)
        assert os.path.exists(output_file), "Augmented CSV not created"

        df_aug = pd.read_csv(output_file)
        assert len(df_aug) == 8, "Augmented rows count mismatch"
        assert "pid" in df_aug.columns, "PID column missing after augmentation"


def test_pid_generation_continuity():
    """Ensure new PIDs continue sequence correctly"""
    existing_ids = {10001, 10002, 10003}
    new_ids = sd.generate_pid_column(3, existing_ids)
    assert new_ids == [10004, 10005, 10006], "PID sequence incorrect"


def test_email_generation_from_names():
    """Ensure email generation is consistent and valid"""
    names = ["John Doe", "Jane Smith"]
    emails = sd.generate_email_from_names(names)
    assert all("@" in e and e.endswith("@example.com") for e in emails), "Invalid emails generated"


def test_date_generation_range():
    """Ensure generated dates fall within range"""
    dates = sd.generate_date_column("2023-01-01", "2023-12-31", 100)
    assert all("2023-" in d for d in dates), "Generated dates outside range"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
