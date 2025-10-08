# rosdl/core/eda_drift_module.py

import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency

def quick_eda(df: pd.DataFrame):
    """Perform quick EDA on a DataFrame."""
    report = {
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "basic_stats": df.describe(include='all').transpose().round(2).to_dict(),
        "unique_values": {col: df[col].nunique() for col in df.columns}
    }
    return report


def detect_drift(df1: pd.DataFrame, df2: pd.DataFrame):
    """Compare two DataFrames and detect data drift."""
    drift_report = []

    for col in df1.columns:
        if col not in df2.columns:
            continue

        if df1[col].equals(df2[col]):
            drift_report.append((col, "No Change", 1.0))
            continue

        if np.issubdtype(df1[col].dropna().dtype, np.number):
            stat, p_val = ks_2samp(df1[col].dropna(), df2[col].dropna())
            drift_report.append((col, "Numerical", p_val))
        else:
            contingency = pd.crosstab(df1[col].dropna(), df2[col].dropna())
            if contingency.shape[0] > 1 and contingency.shape[1] > 1:
                chi2, p_val, _, _ = chi2_contingency(contingency)
                drift_report.append((col, "Categorical", p_val))
            else:
                drift_report.append((col, "Categorical", 1.0))
    return drift_report
