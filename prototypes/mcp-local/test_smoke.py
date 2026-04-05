"""
Quick smoke test for the Data Analysis MCP server tools.
Run: .venv/bin/python test_smoke.py
"""

import sys

sys.path.insert(0, "src")

from data_analysis_mcp.tools.analysis import (
    aggregate_data,
    correlation_analysis,
    filter_data,
    get_summary,
)
from data_analysis_mcp.tools.data_loader import list_loaded_datasets, load_data
from data_analysis_mcp.tools.visualization import visualize_data


def run():
    print("=" * 50)
    print("1. Loading sample data...")
    r = load_data("data/sales_sample.csv")
    assert "error" not in r, r
    print(f"   OK  rows={r['rows']} cols={r['columns']}")

    print("2. Listing datasets...")
    lst = list_loaded_datasets()
    assert lst["count"] == 1
    print(f"   OK  datasets={[d['name'] for d in lst['datasets']]}")

    print("3. Getting summary...")
    s = get_summary("sales_sample")
    assert s["shape"]["rows"] == 28
    print(f"   OK  shape={s['shape']}")

    print("4. Correlation analysis...")
    c = correlation_analysis("sales_sample")
    top = c["top_correlations"][0]
    print(
        f"   OK  top pair: {top['column_a']} <-> {top['column_b']}  r={top['correlation']}"
    )

    print("5. Filter (sales > 2000)...")
    f = filter_data("sales_sample", "sales > 2000")
    assert "error" not in f
    print(f"   OK  filtered_rows={f['filtered_rows']}")

    print("6. Aggregate by region (sum sales)...")
    agg = aggregate_data("sales_sample", ["region"], {"sales": "sum", "units": "sum"})
    assert "error" not in agg
    print(f"   OK  groups={agg['result_rows']}")

    print("7. Generating bar chart...")
    v = visualize_data(
        "sales_sample", "bar", x="region", y="sales", title="Sales by Region"
    )
    assert "error" not in v, v
    print(f"   OK  saved → {v['path']}")

    print("8. Generating heatmap...")
    h = visualize_data("sales_sample", "heatmap", title="Correlation Heatmap")
    assert "error" not in h, h
    print(f"   OK  saved → {h['path']}")

    print("=" * 50)
    print("ALL TESTS PASSED ✓")


if __name__ == "__main__":
    run()
