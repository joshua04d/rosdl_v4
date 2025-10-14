"""
Comprehensive functional test for all rosdl modules.
Generates temporary files, runs all functions, and exports report.
"""

import os
import tempfile
import inspect
import pandas as pd
import json
from rosdl import (
    ocr_module,
    pdf_tools,
    metadata_extractor,
    file_converter,
    image_tools,
    text_utils_module as tu,
    eda_drift_module as eda,
    data_generator
)
from PIL import Image

# Temporary directory to store all test files and outputs
TEST_DIR = os.path.join(tempfile.gettempdir(), "rosdl_test_outputs")
os.makedirs(TEST_DIR, exist_ok=True)
REPORT_FILE = os.path.join(TEST_DIR, "rosdl_test_report.csv")

# ------------------ Helper Functions ------------------

def create_sample_image(path=None, format="PNG"):
    path = path or os.path.join(TEST_DIR, f"sample_img.{format.lower()}")
    Image.new("RGB", (100, 100), color="white").save(path, format=format)
    return path

def create_sample_pdf(path=None):
    path = path or os.path.join(TEST_DIR, "sample.pdf")
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError("Install 'fpdf' to generate test PDFs: pip install fpdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Test PDF", 0, 1)
    pdf.output(path)
    return path

def create_sample_csv(path=None):
    path = path or os.path.join(TEST_DIR, "sample.csv")
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df.to_csv(path, index=False)
    return path

def create_sample_xlsx(path=None):
    path = path or os.path.join(TEST_DIR, "sample.xlsx")
    df = pd.DataFrame({"x": [7, 8, 9], "y": [10, 11, 12]})
    df.to_excel(path, index=False)
    return path

def create_sample_schema(path=None):
    schema = {"columns": [{"name": "id", "type": "int"}, {"name": "name", "type": "str"}]}
    path = path or os.path.join(TEST_DIR, "schema.json")
    with open(path, "w") as f:
        json.dump(schema, f)
    return path

# ------------------ Run Module Tests ------------------

def run_module_tests(module, sample_files):
    results = []
    print(f"\n[MODULE] {module.__name__}")
    for name, func in inspect.getmembers(module, inspect.isfunction):
        status = "✅ Success"
        try:
            sig = inspect.signature(func)
            args = []
            for p in sig.parameters.values():
                if "path" in p.name or "file" in p.name or "pdf" in p.name or "input" in p.name:
                    args.append(sample_files.get("pdf") or sample_files.get("image") or sample_files.get("csv"))
                elif "output" in p.name:
                    args.append(os.path.join(TEST_DIR, f"test_output_{name}.txt"))
                elif "rows" in p.name or "n" in p.name:
                    args.append(5)
                elif "schema" in p.name:
                    args.append(sample_files.get("schema"))
                elif "prompt" in p.name:
                    args.append("Generate synthetic data")
                elif "dataset" in p.name:
                    args.append(sample_files.get("csv"))
                else:
                    args.append(None)
            func(*args)
        except Exception as e:
            status = f"❌ Failed: {e}"
        results.append({"module": module.__name__, "function": name, "status": status})
        print(f"{name}: {status}")
    return results

# ------------------ Main Script ------------------

def main():
    # Prepare sample files
    sample_files = {
        "image": create_sample_image(),
        "pdf": create_sample_pdf(),
        "csv": create_sample_csv(),
        "xlsx": create_sample_xlsx(),
        "schema": create_sample_schema()
    }

    # Modules to test
    modules = [
        ocr_module,
        pdf_tools,
        metadata_extractor,
        file_converter,
        image_tools,
        tu,
        eda,
        data_generator
    ]

    all_results = []
    for module in modules:
        res = run_module_tests(module, sample_files)
        all_results.extend(res)

    # Special EDA drift test
    df1 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df2 = pd.DataFrame({"a": [1, 2, 4], "b": [4, 5, 7]})
    try:
        report = eda.quick_eda(df1)
        all_results.append({"module": "eda_drift_module", "function": "quick_eda", "status": "✅ Success"})
        drift = eda.detect_drift(df1, df2)
        all_results.append({"module": "eda_drift_module", "function": "detect_drift", "status": "✅ Success"})
    except Exception as e:
        all_results.append({"module": "eda_drift_module", "function": "EDA functions", "status": f"❌ Failed: {e}"})

    # Export summary report
    df_report = pd.DataFrame(all_results)
    df_report.to_csv(REPORT_FILE, index=False)
    print(f"\n✅ All tests completed. Summary report saved at: {REPORT_FILE}")

if __name__ == "__main__":
    main()
