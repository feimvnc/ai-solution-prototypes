# Data Analysis MCP Server

A local [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for data analysis, running on macOS. Built with Python, pandas, and seaborn.

## Features

| Tool | Description |
|------|-------------|
| `load_data` | Load CSV / JSON / Excel / Parquet / TSV files |
| `list_datasets` | Show all datasets loaded in this session |
| `get_summary` | Shape, dtypes, describe(), memory usage, preview |
| `list_columns` | Column names, dtypes, null counts, unique counts |
| `missing_values_report` | Missing value counts and percentages |
| `filter_data` | Filter rows using a pandas query string |
| `aggregate_data` | Group by + aggregate (sum, mean, count, …) |
| `correlation_analysis` | Pearson / Spearman / Kendall correlation matrix |
| `run_query` | Execute arbitrary pandas `.query()` expressions |
| `visualize_data` | Save charts (bar, line, scatter, histogram, box, heatmap, pie) |
| `export_data` | Export processed data to CSV / JSON / Excel / Parquet |

---

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.11+

---

## Installation

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -e .
```

---

## Running the server

The server communicates over **stdio** (standard input/output), which is how MCP clients (e.g. Claude Desktop) launch it.

```bash
# Run directly
data-analysis-mcp

# or
python -m data_analysis_mcp.server
```

---

## Connect to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "data-analysis": {
      "command": "/path/to/mcp-local/.venv/bin/python",
      "args": ["-m", "data_analysis_mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/mcp-local/src"
      }
    }
  }
}
```

```bash
# My local file content
{
    "mcpServers": {
        "data-analysis": {
            "command": "/Users/user/Documents/repo/mcp-local/.venv/bin/python",
            "args": [
                "-m",
                "data_analysis_mcp.server"
            ],
            "env": {
                "PYTHONPATH": "/Users/user/Documents/repo/mcp-local/src"
            }
        }
    }
}

```

Replace `/path/to/mcp-local` with the actual absolute path to this repository.

Then restart Claude Desktop — the data analysis tools will appear automatically.

---

## Connect to Claude Code (CLI)

### 1. Register the server

```bash

# Check claude login 
claude auth login
claude -p "hello"
claude mcp list

claude mcp add data-analysis \
  /Users/user/Documents/repo/mcp-local/.venv/bin/python \
  -e PYTHONPATH=/Users/user/Documents/repo/mcp-local/src \
  -- -m data_analysis_mcp.server
```

To make it available across **all projects** (user-wide):

```bash
claude mcp add --scope user data-analysis \
  /Users/user/Documents/repo/mcp-local/.venv/bin/python \
  -e PYTHONPATH=/Users/user/Documents/repo/mcp-local/src \
  -- -m data_analysis_mcp.server

# grant permission
claude --allowedTools "mcp__data-analysis__*" -p "use data_analysis_mcp.server tool to Load the file ~/Documents/repo/mcp-local/data/sales_sample.csv and give me a summary. Then show me total sales by region as a bar chart."
```

### 2. Verify it's connected

```bash
claude mcp list

```

You should see:
```
data-analysis   /Users/user/Documents/repo/mcp-local/.venv/bin/python   connected
```

If it shows **disconnected**, inspect the error with:
```bash
claude mcp get data-analysis
```

### 3. Approve tool permissions

When Claude Code prompts:
> *"Allow mcp__data-analysis__load_data?"*

Choose **"Always allow"** to approve all 11 tools without being prompted again.

To pre-approve all tools in one go, start Claude Code with:

```bash
claude --allowedTools "mcp__data-analysis__*" -p "use data_analysis_mcp.server tool to Load the file ~/Documents/repo/mcp-local/data/sales_sample.csv and give me a summary. Then show me total sales by region as a bar chart."
```

### Basic commands
```bash
# Check basic
claude auth login
claude -p "hello"

# List mcp tools
claude mcp list

# Add mcp to claude
claude mcp add data-analysis \
  /Users/user/Documents/repo/mcp-local/.venv/bin/python \
  -- -m data_analysis_mcp.server \
  --env PYTHONPATH=/Users/user/Documents/repo/mcp-local/src

# Add --allowedTools 
claude --allowedTools "mcp__data-analysis__*"

# Add --allowedTools 
claude --allowedTools "mcp__data-analysis__*" -p "use data_analysis_mcp.server tool to Load the file ~/Documents/repo/mcp-local/data/sales_sample.csv and give me a summary. Then show me total sales by region as a bar chart."

# may see error is without --allowedTools 
claude -p "use data_analysis_mcp.server tool to Load the file ~/Documents/repo/mcp-local/data/sales_sample.csv and give me a summary.
Then show me total sales by region as a bar chart."

```

### 4. Scope options

| Scope | Flag | Config file |
|-------|------|-------------|
| Current project only | `--scope local` | `.claude/settings.json` |
| All your projects | `--scope user` | `~/.claude/settings.json` |
| Shared with team | `--scope project` | `.claude/settings.json` (commit this) |

### 5. Usage in a Claude Code session

Start a session and use the tools naturally:

```
Load /Users/user/Documents/repo/mcp-local/data/sales_sample.csv
Show me a summary and generate a bar chart of sales by region.
```

Claude Code will call the MCP tools automatically:
- `mcp__data-analysis__load_data`
- `mcp__data-analysis__get_summary`
- `mcp__data-analysis__visualize_data`

---

## Quick Example

Once connected, ask Claude:

```
Load the file ~/Documents/repo/mcp-local/data/sales_sample.csv and give me a summary.
Then show me total sales by region as a bar chart.
```

---

## Project Structure

```
mcp-local/
├── src/
│   └── data_analysis_mcp/
│       ├── server.py          # MCP server + tool registration
│       ├── tools/
│       │   ├── data_loader.py  # Load / export files
│       │   ├── analysis.py     # Stats, filter, query, correlation
│       │   └── visualization.py# Chart generation
│       └── utils/
│           └── helpers.py      # In-memory dataset registry
├── data/                       # Sample datasets
├── output/                     # Generated charts (auto-created)
├── pyproject.toml
└── requirements.txt
```

---

## Sample Data

`data/sales_sample.csv` — 28 rows of daily regional product sales data, ready to explore.
