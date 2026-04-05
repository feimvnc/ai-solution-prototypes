"""
server.py – Main MCP server for local data analysis.

Exposes the following tools via the Model Context Protocol:
  - load_data
  - list_datasets
  - get_summary
  - list_columns
  - missing_values_report
  - filter_data
  - aggregate_data
  - correlation_analysis
  - run_query
  - visualize_data
  - export_data

Run with:
    python -m data_analysis_mcp.server
or via the installed script:
    data-analysis-mcp
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from data_analysis_mcp.tools.analysis import (
    aggregate_data,
    correlation_analysis,
    filter_data,
    get_summary,
    list_columns,
    missing_values_report,
    run_query,
)
from data_analysis_mcp.tools.data_loader import (
    export_data,
    list_loaded_datasets,
    load_data,
)
from data_analysis_mcp.tools.visualization import visualize_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
logger = logging.getLogger("data-analysis-mcp")

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

app = Server("data-analysis-mcp")

# ---------------------------------------------------------------------------
# Tool definitions (schema exposed to the AI client)
# ---------------------------------------------------------------------------

TOOLS: list[types.Tool] = [
    types.Tool(
        name="load_data",
        description=(
            "Load a data file (CSV, JSON, Excel, Parquet, TSV) from the local filesystem "
            "into the session. The dataset is stored under 'dataset_name' for later use."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the data file.",
                },
                "dataset_name": {
                    "type": "string",
                    "description": "Optional name for the dataset (defaults to the file stem).",
                },
            },
            "required": ["file_path"],
        },
    ),
    types.Tool(
        name="list_datasets",
        description="List all datasets currently loaded in this session.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    types.Tool(
        name="get_summary",
        description=(
            "Return comprehensive statistics for a loaded dataset: shape, column types, "
            "numeric describe(), categorical describe(), memory usage, and a 5-row preview."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {
                    "type": "string",
                    "description": "Name of the loaded dataset.",
                },
            },
            "required": ["dataset_name"],
        },
    ),
    types.Tool(
        name="list_columns",
        description="List all columns in a dataset with their dtype, null count, and unique count.",
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
            },
            "required": ["dataset_name"],
        },
    ),
    types.Tool(
        name="missing_values_report",
        description="Report the count and percentage of missing values per column in a dataset.",
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
            },
            "required": ["dataset_name"],
        },
    ),
    types.Tool(
        name="filter_data",
        description=(
            "Filter rows using a pandas query expression (e.g. 'age > 30 and salary < 80000'). "
            "The result is stored as a new dataset."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "condition": {
                    "type": "string",
                    "description": "Pandas query string (e.g. \"price > 100 and category == 'A'\").",
                },
                "output_name": {
                    "type": "string",
                    "description": "Name for the filtered dataset. Optional.",
                },
            },
            "required": ["dataset_name", "condition"],
        },
    ),
    types.Tool(
        name="aggregate_data",
        description=(
            "Group a dataset by one or more columns and apply aggregation functions "
            "(sum, mean, count, min, max, etc.). Result is stored as a new dataset."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "group_by": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Columns to group by.",
                },
                "aggregations": {
                    "type": "object",
                    "description": 'Map of column -> agg function(s), e.g. {"sales": "sum", "age": ["mean","max"]}.',
                },
                "output_name": {
                    "type": "string",
                    "description": "Optional name for the result.",
                },
            },
            "required": ["dataset_name", "group_by", "aggregations"],
        },
    ),
    types.Tool(
        name="correlation_analysis",
        description="Compute a pairwise correlation matrix for numeric columns in a dataset.",
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "method": {
                    "type": "string",
                    "enum": ["pearson", "spearman", "kendall"],
                    "description": "Correlation method. Default: 'pearson'.",
                },
                "columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Subset of columns to include. Optional.",
                },
            },
            "required": ["dataset_name"],
        },
    ),
    types.Tool(
        name="run_query",
        description=(
            "Execute a pandas .query() expression on a dataset and return matching rows. "
            "Result is stored as a new dataset."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "query": {
                    "type": "string",
                    "description": "Pandas query string.",
                },
                "output_name": {
                    "type": "string",
                    "description": "Optional name for the result.",
                },
            },
            "required": ["dataset_name", "query"],
        },
    ),
    types.Tool(
        name="visualize_data",
        description=(
            "Generate and save a chart (bar, line, scatter, histogram, box, heatmap, pie) "
            "from a loaded dataset. Returns the path to the saved PNG file."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "chart_type": {
                    "type": "string",
                    "enum": [
                        "bar",
                        "line",
                        "scatter",
                        "histogram",
                        "box",
                        "heatmap",
                        "pie",
                    ],
                },
                "x": {"type": "string", "description": "Column for the X axis."},
                "y": {"type": "string", "description": "Column for the Y axis."},
                "hue": {"type": "string", "description": "Column for colour grouping."},
                "title": {"type": "string", "description": "Chart title."},
                "output_filename": {
                    "type": "string",
                    "description": "Output PNG filename.",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Directory to save the chart.",
                },
                "bins": {
                    "type": "integer",
                    "description": "Number of bins for histogram. Default: 30.",
                },
                "top_n": {
                    "type": "integer",
                    "description": "Limit to top N values for bar/pie charts.",
                },
            },
            "required": ["dataset_name", "chart_type"],
        },
    ),
    types.Tool(
        name="export_data",
        description="Export a loaded dataset to disk in CSV, JSON, Excel, or Parquet format.",
        inputSchema={
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"},
                "output_path": {
                    "type": "string",
                    "description": "Destination file path.",
                },
                "fmt": {
                    "type": "string",
                    "enum": ["csv", "json", "excel", "parquet"],
                    "description": "Export format. Default: 'csv'.",
                },
            },
            "required": ["dataset_name", "output_path"],
        },
    ),
]

# ---------------------------------------------------------------------------
# Handler: list tools
# ---------------------------------------------------------------------------


@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return TOOLS


# ---------------------------------------------------------------------------
# Handler: call tool
# ---------------------------------------------------------------------------


@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    logger.info("Tool called: %s  args=%s", name, arguments)

    result: Any = None

    try:
        if name == "load_data":
            result = load_data(
                file_path=arguments["file_path"],
                dataset_name=arguments.get("dataset_name"),
            )
        elif name == "list_datasets":
            result = list_loaded_datasets()

        elif name == "get_summary":
            result = get_summary(arguments["dataset_name"])

        elif name == "list_columns":
            result = list_columns(arguments["dataset_name"])

        elif name == "missing_values_report":
            result = missing_values_report(arguments["dataset_name"])

        elif name == "filter_data":
            result = filter_data(
                dataset_name=arguments["dataset_name"],
                condition=arguments["condition"],
                output_name=arguments.get("output_name"),
            )
        elif name == "aggregate_data":
            result = aggregate_data(
                dataset_name=arguments["dataset_name"],
                group_by=arguments["group_by"],
                aggregations=arguments["aggregations"],
                output_name=arguments.get("output_name"),
            )
        elif name == "correlation_analysis":
            result = correlation_analysis(
                dataset_name=arguments["dataset_name"],
                method=arguments.get("method", "pearson"),
                columns=arguments.get("columns"),
            )
        elif name == "run_query":
            result = run_query(
                dataset_name=arguments["dataset_name"],
                query=arguments["query"],
                output_name=arguments.get("output_name"),
            )
        elif name == "visualize_data":
            result = visualize_data(
                dataset_name=arguments["dataset_name"],
                chart_type=arguments["chart_type"],
                x=arguments.get("x"),
                y=arguments.get("y"),
                hue=arguments.get("hue"),
                title=arguments.get("title"),
                output_filename=arguments.get("output_filename"),
                output_dir=arguments.get("output_dir"),
                bins=arguments.get("bins", 30),
                top_n=arguments.get("top_n"),
            )
        elif name == "export_data":
            result = export_data(
                dataset_name=arguments["dataset_name"],
                output_path=arguments["output_path"],
                fmt=arguments.get("fmt", "csv"),
            )
        else:
            result = {"error": f"Unknown tool: '{name}'"}

    except Exception as exc:
        logger.exception("Unhandled error in tool '%s'", name)
        result = {"error": f"Internal server error: {exc}"}

    return [
        types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))
    ]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def _run() -> None:
    logger.info("Starting Data Analysis MCP server (stdio transport)…")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
