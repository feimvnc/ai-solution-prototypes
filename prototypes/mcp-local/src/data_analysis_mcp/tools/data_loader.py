"""
data_loader.py – Tools for loading data files into the in-memory registry.

Supported formats: CSV, JSON, Excel (.xlsx/.xls), Parquet
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_analysis_mcp.utils.helpers import dataset_info, list_datasets, store_dataset

# ---------------------------------------------------------------------------
# load_data
# ---------------------------------------------------------------------------


def load_data(file_path: str, dataset_name: str | None = None) -> dict:
    """
    Load a data file (CSV / JSON / Excel / Parquet) into the session registry.

    Args:
        file_path:    Absolute or relative path to the data file.
        dataset_name: Optional name to reference this dataset later.
                      Defaults to the file stem (e.g. 'sales' for 'sales.csv').

    Returns:
        A dict with keys: name, rows, columns, column_names, message.
    """
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        return {"error": f"File not found: {path}"}

    suffix = path.suffix.lower()
    name = dataset_name or path.stem

    try:
        if suffix == ".csv":
            df = pd.read_csv(path)
        elif suffix == ".json":
            df = pd.read_json(path)
        elif suffix in (".xlsx", ".xls"):
            df = pd.read_excel(path, engine="openpyxl")
        elif suffix == ".parquet":
            df = pd.read_parquet(path)
        elif suffix == ".tsv":
            df = pd.read_csv(path, sep="\t")
        else:
            return {
                "error": f"Unsupported file format: '{suffix}'. Supported: csv, tsv, json, xlsx, xls, parquet"
            }
    except Exception as exc:
        return {"error": f"Failed to load file: {exc}"}

    store_dataset(name, df)

    return {
        "message": f"Dataset '{name}' loaded successfully.",
        "name": name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


# ---------------------------------------------------------------------------
# list_datasets
# ---------------------------------------------------------------------------


def list_loaded_datasets() -> dict:
    """
    Return all dataset names currently loaded in the session.

    Returns:
        A dict with key 'datasets' containing a list of dataset metadata.
    """
    names = list_datasets()
    if not names:
        return {
            "datasets": [],
            "message": "No datasets loaded yet. Use load_data first.",
        }
    return {
        "datasets": [dataset_info(n) for n in names],
        "count": len(names),
    }


# ---------------------------------------------------------------------------
# export_data
# ---------------------------------------------------------------------------


def export_data(dataset_name: str, output_path: str, fmt: str = "csv") -> dict:
    """
    Export a loaded dataset to disk.

    Args:
        dataset_name: Name of the dataset to export.
        output_path:  Destination file path.
        fmt:          Format: 'csv', 'json', 'excel', or 'parquet'.

    Returns:
        A dict with 'message' or 'error'.
    """
    from data_analysis_mcp.utils.helpers import get_dataset

    df = get_dataset(dataset_name)
    if df is None:
        return {
            "error": f"Dataset '{dataset_name}' not found. Load it first with load_data."
        }

    out = Path(output_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        if fmt == "csv":
            df.to_csv(out, index=False)
        elif fmt == "json":
            df.to_json(out, orient="records", indent=2)
        elif fmt == "excel":
            df.to_excel(out, index=False, engine="openpyxl")
        elif fmt == "parquet":
            df.to_parquet(out, index=False)
        else:
            return {
                "error": f"Unsupported export format '{fmt}'. Choose: csv, json, excel, parquet"
            }
    except Exception as exc:
        return {"error": f"Export failed: {exc}"}

    return {"message": f"Dataset '{dataset_name}' exported to {out}", "path": str(out)}
