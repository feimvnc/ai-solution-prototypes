"""
analysis.py – Data analysis tools: summary stats, filtering, groupby,
              correlation, missing values, and pandas query execution.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

from data_analysis_mcp.utils.helpers import get_dataset, store_dataset


def _require(dataset_name: str) -> pd.DataFrame | dict:
    """Helper: return the DataFrame or an error dict."""
    df = get_dataset(dataset_name)
    if df is None:
        return {"error": f"Dataset '{dataset_name}' not found. Use load_data first."}
    return df


# ---------------------------------------------------------------------------
# get_summary
# ---------------------------------------------------------------------------


def get_summary(dataset_name: str) -> dict:
    """
    Return a comprehensive statistical summary of a dataset.

    Includes: shape, dtypes, describe() for numeric and categorical columns,
    memory usage, and a preview of the first 5 rows.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    numeric_desc = df.describe(include=[np.number]).round(4).to_dict()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    cat_desc = df[cat_cols].describe().to_dict() if cat_cols else {}

    return {
        "dataset": dataset_name,
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "column_dtypes": df.dtypes.astype(str).to_dict(),
        "numeric_summary": numeric_desc,
        "categorical_summary": cat_desc,
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "preview": df.head(5).to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# list_columns
# ---------------------------------------------------------------------------


def list_columns(dataset_name: str) -> dict:
    """Return column names, data types, and null counts."""
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    return {
        "dataset": dataset_name,
        "columns": [
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isna().sum()),
                "unique_count": int(df[col].nunique()),
            }
            for col in df.columns
        ],
    }


# ---------------------------------------------------------------------------
# missing_values_report
# ---------------------------------------------------------------------------


def missing_values_report(dataset_name: str) -> dict:
    """
    Report missing value counts and percentages per column.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    total = len(df)
    report = []
    for col in df.columns:
        count = int(df[col].isna().sum())
        report.append(
            {
                "column": col,
                "missing_count": count,
                "missing_pct": round(count / total * 100, 2) if total > 0 else 0.0,
            }
        )

    report.sort(key=lambda x: x["missing_count"], reverse=True)
    total_missing = sum(r["missing_count"] for r in report)

    return {
        "dataset": dataset_name,
        "total_rows": total,
        "columns_with_missing": sum(1 for r in report if r["missing_count"] > 0),
        "report": report,
        "total_missing_cells": total_missing,
    }


# ---------------------------------------------------------------------------
# filter_data
# ---------------------------------------------------------------------------


def filter_data(
    dataset_name: str,
    condition: str,
    output_name: str | None = None,
) -> dict:
    """
    Filter a dataset using a pandas query expression.

    Args:
        dataset_name: Source dataset.
        condition:    A pandas query string, e.g. "age > 30 and salary < 100000".
        output_name:  If provided, store the result as a new dataset with this name.

    Returns:
        Summary of the filtered result.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    try:
        filtered = df.query(condition)
    except Exception as exc:
        return {"error": f"Invalid filter condition '{condition}': {exc}"}

    result_name = output_name or f"{dataset_name}_filtered"
    store_dataset(result_name, filtered)

    return {
        "dataset": result_name,
        "condition": condition,
        "original_rows": len(df),
        "filtered_rows": len(filtered),
        "columns": filtered.columns.tolist(),
        "preview": filtered.head(5).to_dict(orient="records"),
        "message": f"Filtered result stored as '{result_name}'.",
    }


# ---------------------------------------------------------------------------
# aggregate_data
# ---------------------------------------------------------------------------


def aggregate_data(
    dataset_name: str,
    group_by: list[str],
    aggregations: dict[str, str | list[str]],
    output_name: str | None = None,
) -> dict:
    """
    Group by one or more columns and apply aggregation functions.

    Args:
        dataset_name:  Source dataset.
        group_by:      List of column names to group by.
        aggregations:  Dict mapping column -> agg function(s),
                       e.g. {"sales": "sum", "age": ["mean", "max"]}.
        output_name:   Optional name to store the aggregated result.

    Returns:
        The aggregated data preview and metadata.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    # Validate group_by columns
    missing_cols = [c for c in group_by if c not in df.columns]
    if missing_cols:
        return {"error": f"Columns not found in dataset: {missing_cols}"}

    try:
        grouped = df.groupby(group_by).agg(aggregations).reset_index()
        # Flatten multi-level column names if needed
        if isinstance(grouped.columns, pd.MultiIndex):
            grouped.columns = [
                "_".join(filter(None, map(str, col))) for col in grouped.columns
            ]
    except Exception as exc:
        return {"error": f"Aggregation failed: {exc}"}

    result_name = output_name or f"{dataset_name}_aggregated"
    store_dataset(result_name, grouped)

    return {
        "dataset": result_name,
        "group_by": group_by,
        "aggregations": aggregations,
        "result_rows": len(grouped),
        "result_columns": grouped.columns.tolist(),
        "preview": grouped.head(10).to_dict(orient="records"),
        "message": f"Aggregated result stored as '{result_name}'.",
    }


# ---------------------------------------------------------------------------
# correlation_analysis
# ---------------------------------------------------------------------------


def correlation_analysis(
    dataset_name: str,
    method: Literal["pearson", "spearman", "kendall"] = "pearson",
    columns: list[str] | None = None,
) -> dict:
    """
    Compute pairwise correlations between numeric columns.

    Args:
        dataset_name: Source dataset.
        method:       'pearson', 'spearman', or 'kendall'.
        columns:      Subset of columns to use. Defaults to all numeric columns.

    Returns:
        Correlation matrix as a dict, plus top 10 strongest pairs.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    numeric_df = df.select_dtypes(include=[np.number])
    if columns:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            return {"error": f"Columns not found: {missing}"}
        numeric_df = df[columns].select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        return {"error": "Need at least 2 numeric columns for correlation analysis."}

    try:
        corr = numeric_df.corr(method=method).round(4)
    except Exception as exc:
        return {"error": f"Correlation computation failed: {exc}"}

    # Find top correlations (exclude diagonal)
    corr_pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            corr_pairs.append(
                {
                    "column_a": cols[i],
                    "column_b": cols[j],
                    "correlation": round(corr.values[i, j].item(), 4),
                }
            )
    corr_pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    return {
        "dataset": dataset_name,
        "method": method,
        "columns_used": cols,
        "correlation_matrix": corr.to_dict(),
        "top_correlations": corr_pairs[:10],
    }


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


def run_query(
    dataset_name: str,
    query: str,
    output_name: str | None = None,
) -> dict:
    """
    Execute a pandas .query() expression on a dataset.

    Args:
        dataset_name: Source dataset.
        query:        Pandas query string, e.g. "price > 100 and category == 'A'".
        output_name:  Optional name to store the result.

    Returns:
        Result rows, count, and preview.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    try:
        result = df.query(query)
    except Exception as exc:
        return {"error": f"Query failed: {exc}"}

    result_name = output_name or f"{dataset_name}_query_result"
    store_dataset(result_name, result)

    return {
        "dataset": result_name,
        "query": query,
        "result_rows": len(result),
        "columns": result.columns.tolist(),
        "preview": result.head(10).to_dict(orient="records"),
        "message": f"Query result stored as '{result_name}'.",
    }
