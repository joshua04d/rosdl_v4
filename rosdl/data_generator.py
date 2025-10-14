# rosdl/core/synthetic_data.py
"""
Synthetic Data Generation and Augmentation Module
Part of rosdl.core

Provides:
- Schema-based synthetic dataset generation
- Prompt-based dataset generation
- Augmentation of existing CSV datasets
"""

import os
import random
import string
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')


# ---------------- Helper Generators ---------------- #

def generate_int_column(min_val, max_val, n):
    return np.random.randint(min_val, max_val + 1, size=n)

def generate_float_column(min_val, max_val, n):
    return np.random.uniform(min_val, max_val, size=n).round(2)

def generate_category_column(categories, n):
    return np.random.choice(categories, size=n)

def generate_string_column(str_len, n):
    return [''.join(random.choices(string.ascii_letters + string.digits, k=str_len)) for _ in range(n)]

def generate_realistic_name(n): return [fake.name() for _ in range(n)]
def generate_realistic_city(n): return [fake.city() for _ in range(n)]
def generate_realistic_phone(n): return [fake.phone_number() for _ in range(n)]

def generate_email_from_names(names):
    return [nm.lower().replace(' ', '.').replace("'", '').replace('-', '') + "@example.com" for nm in names]

def generate_pid_column(n, existing_ids=None):
    existing_ids = existing_ids or set()
    start = max(existing_ids) + 1 if existing_ids else 10000
    return list(range(start, start + n))

def generate_date_column(start_date_str, end_date_str, n):
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = (end - start).days
    return [(start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d") for _ in range(n)]


# ---------------- Schema-Based Generation ---------------- #

def generate_from_schema(schema, n_rows, output_path=None):
    """Generate dataset based on user-defined schema."""
    data = {}

    for col in schema:
        cname = col['name'].lower()
        if cname == 'pid':
            data[col['name']] = generate_pid_column(n_rows)
        elif col['type'] == 'int':
            data[col['name']] = generate_int_column(col['min'], col['max'], n_rows)
        elif col['type'] == 'float':
            data[col['name']] = generate_float_column(col['min'], col['max'], n_rows)
        elif col['type'] == 'category':
            data[col['name']] = generate_category_column(col['categories'], n_rows)
        elif col['type'] == 'date':
            data[col['name']] = generate_date_column(col['start'], col['end'], n_rows)
        elif col['type'] == 'string':
            if 'name' in cname:
                data[col['name']] = generate_realistic_name(n_rows)
            elif 'city' in cname:
                data[col['name']] = generate_realistic_city(n_rows)
            elif 'phone' in cname or 'mobile' in cname:
                data[col['name']] = generate_realistic_phone(n_rows)
            elif 'email' in cname:
                pass  # handle later
            else:
                data[col['name']] = generate_string_column(8, n_rows)

    # Handle email field if exists
    name_col = next((c['name'] for c in schema if 'name' in c['name'].lower()), None)
    email_col = next((c['name'] for c in schema if 'email' in c['name'].lower()), None)
    if email_col:
        if name_col and name_col in data:
            data[email_col] = generate_email_from_names(data[name_col])
        else:
            data[email_col] = [fake.email() for _ in range(n_rows)]

    df = pd.DataFrame(data)
    fname = output_path or f"synthetic_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(fname, index=False)
    return fname


# ---------------- Prompt-Based Generation ---------------- #

def generate_from_prompt(prompt, output_path=None):
    """Generate dataset using a text prompt description."""
    parts = prompt.lower().split('columns:')
    if len(parts) != 2:
        raise ValueError("Prompt must contain 'columns:' section.")
    n_rows = int(''.join(filter(str.isdigit, parts[0])))
    col_defs = [x.strip() for x in parts[1].split(',')]

    schema = []
    for c in col_defs:
        tokens = c.split()
        if len(tokens) < 2:
            continue
        name, dtype = tokens[0], tokens[1]
        col = {'name': name, 'type': dtype}

        if dtype in ['int', 'float']:
            min_val, max_val = map(float, tokens[2].split('-'))
            col['min'], col['max'] = (int(min_val), int(max_val)) if dtype == 'int' else (min_val, max_val)
        elif dtype == 'category':
            col['categories'] = [x.strip().upper() for x in tokens[2].split('/')]
        elif dtype == 'date':
            start, end = tokens[2].split(':')
            col['start'], col['end'] = start, end
        schema.append(col)

    return generate_from_schema(schema, n_rows, output_path)

# ---------------- Augmentation ---------------- #

def augment_dataset(path, n_add, output_path=None):
    """Augment an existing dataset by adding synthetic rows."""
    df = pd.read_csv(path)
    existing_pids = set(df['pid'].dropna().astype(int)) if 'pid' in df.columns else set()
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if pd.api.types.is_object_dtype(df[c])]

    new_rows = []
    for _ in range(n_add):
        new = {}
        for col in df.columns:
            if col.lower() == 'pid':
                continue
            if col in numeric_cols:
                val = df[col].mean() + np.random.normal(0, df[col].std() / 5)
                new[col] = round(val, 2)
            elif col in cat_cols:
                choices = df[col].dropna().unique().tolist()
                if choices:
                    new[col] = random.choice(choices)
                else:
                    new[col] = fake.word()
            else:
                # fallback for any other column type
                vals = df[col].dropna().tolist()
                new[col] = random.choice(vals) if vals else ""
        new_rows.append(new)

    df_new = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # regenerate PIDs if present
    if 'pid' in df.columns:
        df_new['pid'] = generate_pid_column(len(df_new), set())

    fname = output_path or f"augmented_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_new.to_csv(fname, index=False)
    return fname
