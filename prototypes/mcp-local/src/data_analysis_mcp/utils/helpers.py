"""
Shared in-memory state for datasets loaded during the MCP session.
All tools operate on this registry.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

# Global registry: dataset_name -> DataFrame
_datasets: dict[str, pd.DataFrame] = {}


def store_dataset(name: str, df: pd.DataFrame) -> None:
    """Store a DataFrame under the given name."""
    _datasets[name] = df


def get_dataset(name: str) -> Optional[pd.DataFrame]:
    """Retrieve a DataFrame by name, or None if not found."""
    return _datasets.get(name)


def list_datasets() -> list[str]:
    """Return all currently loaded dataset names."""
    return list(_datasets.keys())


def remove_dataset(name: str) -> bool:
    """Remove a dataset from the registry. Returns True if it existed."""
    if name in _datasets:
        del _datasets[name]
        return True
    return False


def dataset_info(name: str) -> Optional[dict]:
    """Return a quick metadata dict for a dataset."""
    df = get_dataset(name)
    if df is None:
        return None
    return {
        "name": name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
    }
