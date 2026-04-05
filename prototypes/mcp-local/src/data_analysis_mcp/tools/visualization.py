"""
visualization.py – Tools for generating and saving charts from loaded datasets.

Supported chart types: bar, line, scatter, histogram, box, heatmap, pie
All charts are saved as PNG files to the output directory.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_analysis_mcp.utils.helpers import get_dataset

# Default output directory (next to project root)
_DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[4] / "output"

# Apply a clean style globally
sns.set_theme(style="whitegrid", palette="muted")


def _resolve_output_path(filename: str, output_dir: str | None) -> Path:
    base = (
        Path(output_dir).expanduser().resolve() if output_dir else _DEFAULT_OUTPUT_DIR
    )
    base.mkdir(parents=True, exist_ok=True)
    return base / filename


def _require(dataset_name: str) -> pd.DataFrame | dict:
    df = get_dataset(dataset_name)
    if df is None:
        return {"error": f"Dataset '{dataset_name}' not found. Use load_data first."}
    return df


# ---------------------------------------------------------------------------
# visualize_data  (unified entry point)
# ---------------------------------------------------------------------------


def visualize_data(
    dataset_name: str,
    chart_type: str,
    x: str | None = None,
    y: str | None = None,
    hue: str | None = None,
    title: str | None = None,
    output_filename: str | None = None,
    output_dir: str | None = None,
    figsize: tuple[int, int] = (10, 6),
    bins: int = 30,
    top_n: int | None = None,
) -> dict:
    """
    Generate and save a chart from a loaded dataset.

    Args:
        dataset_name:     Name of the loaded dataset.
        chart_type:       One of: 'bar', 'line', 'scatter', 'histogram',
                          'box', 'heatmap', 'pie'.
        x:                Column for the X axis (or values for pie/histogram).
        y:                Column for the Y axis.
        hue:              Column used for colour grouping.
        title:            Chart title. Defaults to auto-generated.
        output_filename:  Filename for the saved PNG. Defaults to auto-generated.
        output_dir:       Directory to save the chart. Defaults to ./output.
        figsize:          Figure size as (width, height) in inches.
        bins:             Number of bins for histograms.
        top_n:            For bar/pie, limit to top N categories by value.

    Returns:
        dict with 'path' (saved file path) or 'error'.
    """
    df = _require(dataset_name)
    if isinstance(df, dict):
        return df

    chart_type = chart_type.lower().strip()
    valid_types = {"bar", "line", "scatter", "histogram", "box", "heatmap", "pie"}
    if chart_type not in valid_types:
        return {
            "error": f"Unknown chart_type '{chart_type}'. Choose from: {sorted(valid_types)}"
        }

    auto_title = title or f"{chart_type.capitalize()} – {dataset_name}"
    fname = output_filename or f"{dataset_name}_{chart_type}.png"
    out_path = _resolve_output_path(fname, output_dir)

    fig, ax = plt.subplots(figsize=figsize)

    try:
        if chart_type == "bar":
            _plot_bar(df, ax, x, y, hue, top_n)

        elif chart_type == "line":
            _plot_line(df, ax, x, y, hue)

        elif chart_type == "scatter":
            _plot_scatter(df, ax, x, y, hue)

        elif chart_type == "histogram":
            _plot_histogram(df, ax, x, bins, hue)

        elif chart_type == "box":
            _plot_box(df, ax, x, y, hue)

        elif chart_type == "heatmap":
            plt.close(fig)
            fig = _plot_heatmap(df, figsize)

        elif chart_type == "pie":
            _plot_pie(df, ax, x, y, top_n)

        ax_obj = fig.axes[0] if chart_type == "heatmap" else ax
        ax_obj.set_title(auto_title, fontsize=14, fontweight="bold", pad=12)

        fig.tight_layout()
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    except Exception as exc:
        plt.close(fig)
        return {"error": f"Chart generation failed: {exc}"}

    return {
        "message": "Chart saved successfully.",
        "path": str(out_path),
        "chart_type": chart_type,
        "dataset": dataset_name,
    }


# ---------------------------------------------------------------------------
# Private plot helpers
# ---------------------------------------------------------------------------


def _plot_bar(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    y: str | None,
    hue: str | None,
    top_n: int | None,
) -> None:
    if x is None:
        raise ValueError("'x' column is required for a bar chart.")

    if y is None:
        # Count-based bar chart
        counts = df[x].value_counts()
        if top_n:
            counts = counts.head(top_n)
        sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="muted")
        ax.set_xlabel(x)
        ax.set_ylabel("Count")
    else:
        plot_df = df
        if top_n:
            plot_df = df.nlargest(top_n, y)
        sns.barplot(data=plot_df, x=x, y=y, hue=hue, ax=ax)

    ax.tick_params(axis="x", rotation=45)


def _plot_line(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    y: str | None,
    hue: str | None,
) -> None:
    if x is None or y is None:
        raise ValueError("Both 'x' and 'y' columns are required for a line chart.")
    sns.lineplot(data=df, x=x, y=y, hue=hue, ax=ax, marker="o", markersize=4)


def _plot_scatter(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    y: str | None,
    hue: str | None,
) -> None:
    if x is None or y is None:
        raise ValueError("Both 'x' and 'y' columns are required for a scatter chart.")
    sns.scatterplot(data=df, x=x, y=y, hue=hue, ax=ax, alpha=0.7)


def _plot_histogram(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    bins: int,
    hue: str | None,
) -> None:
    if x is None:
        raise ValueError("'x' column is required for a histogram.")
    sns.histplot(data=df, x=x, bins=bins, hue=hue, kde=True, ax=ax)


def _plot_box(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    y: str | None,
    hue: str | None,
) -> None:
    if y is None:
        raise ValueError("'y' column is required for a box plot.")
    sns.boxplot(data=df, x=x, y=y, hue=hue, ax=ax)
    if x:
        ax.tick_params(axis="x", rotation=45)


def _plot_heatmap(df: pd.DataFrame, figsize: tuple[int, int]) -> plt.Figure:
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        raise ValueError("Need at least 2 numeric columns for a heatmap.")
    corr = numeric_df.corr().round(2)
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=ax,
        linewidths=0.5,
    )
    return fig


def _plot_pie(
    df: pd.DataFrame,
    ax: plt.Axes,
    x: str | None,
    y: str | None,
    top_n: int | None,
) -> None:
    if x is None:
        raise ValueError("'x' column (category) is required for a pie chart.")

    if y is None:
        counts = df[x].value_counts()
    else:
        counts = df.groupby(x)[y].sum().sort_values(ascending=False)

    if top_n:
        counts = counts.head(top_n)

    ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.axis("equal")
