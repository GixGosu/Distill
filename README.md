# VTT Transcript Analyzer for n8n

An AI-powered n8n workflow that analyzes VTT transcript files at scale (100+ files), generates comprehensive summaries, and creates interactive HTML dashboards with visualizations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![n8n](https://img.shields.io/badge/n8n-1.0+-orange.svg)

## Features

- **Batch Processing** - Analyzes hundreds of VTT transcripts in parallel
- **Intelligent Synthesis** - Creates cross-session analysis with topic heatmaps
- **Interactive Dashboard** - Generates a self-contained HTML dashboard with:
  - Question explorer with search & filters
  - Topic coverage heatmap (scrollable for large datasets)
  - Tools & resources gallery with links
  - Session navigator with pagination
  - D3.js knowledge graph visualization
  - Dark/light mode toggle
  - Reading path selector (Quick Scan → Deep Dive)
- **Quality Assurance Loop** - 3-pass review system checking content accuracy, visual design, and technical quality
- **Auto-Improvement** - Automatically fixes issues identified by reviewers

## Architecture

```
┌─────────────────┐
│ VTT Files       │
│ /transcripts/   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────────────┐
│ Main Workflow   │────▶│ Single File Analyzer    │
│ (Orchestrator)  │     │ (Subworkflow, 3x parallel)
└────────┬────────┘     └─────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Hierarchical    │  Batches of 20 files → batch summaries
│ Synthesis Agent │  → combined-analysis.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Visualization   │  → dashboard.html
│ Agent           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Knowledge Graph │  → D3.js force graph
│ Agent           │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Quality Review Loop             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Content  │ │ Visual   │ │Technical │ │
│  │ Reviewer │ │ Reviewer │ │ Reviewer │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       └────────────┼────────────┘       │
│                    ▼                    │
│           ┌──────────────┐              │
│           │ Improvement  │──┐ (max 3    │
│           │ Agent        │  │ iterations)
│           └──────────────┘◀─┘           │
└─────────────────────────────────────────┘
```

## Requirements

- **n8n** v1.0+ (self-hosted or cloud)
- **Claude Bridge** - An HTTP bridge that exposes Claude's computer use capabilities
- **Docker** (recommended for claude-bridge)

## Quick Start

### 1. Set Up Claude Bridge

The workflow communicates with Claude via an HTTP bridge service. You'll need to set this up first:

```bash
# Example using a Docker-based claude-bridge
docker run -d \
  --name claude-bridge \
  -p 3456:3456 \
  -v /path/to/transcripts:/transcripts \
  -e ANTHROPIC_API_KEY=your-key-here \
  your-claude-bridge-image
```

> **Note:** Claude Bridge is a separate component that wraps Claude's API with computer use capabilities. See [Claude Bridge Setup](#claude-bridge-setup) for details.

### 2. Import Workflows

1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Import both workflows:
   - `workflows/vtt-analyzer-main.json` (main orchestrator)
   - `workflows/vtt-analyzer-single-file.json` (subworkflow)

### 3. Configure the Subworkflow

1. Open **VTT Analyzer - SCALED V2**
2. Find the node **"Analyze Files (Max 3 Parallel)"**
3. Click it and select **VTT Single File Analyzer** from the workflow dropdown

### 4. Adjust Endpoints (if needed)

If your claude-bridge runs on a different URL than `http://claude-bridge:3456/claude`, update all HTTP Request nodes.

### 5. Add Your Transcripts

Place your `.vtt` files in the configured transcripts directory (default: `/transcripts/`).

### 6. Run!

Click **Execute Workflow** on the main workflow. For large datasets, expect:
- ~2-5 min per file analysis
- ~30-60 min for synthesis (100+ files)
- ~15-30 min for dashboard generation
- ~15-30 min for quality review loop

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_BRIDGE_URL` | Claude Bridge endpoint | `http://claude-bridge:3456/claude` |
| `TRANSCRIPTS_DIR` | Path to VTT files | `/transcripts` |

### Workflow Settings

| Setting | Location | Description |
|---------|----------|-------------|
| `maxConcurrency` | Single File Analyzer | Parallel file processing (default: 3) |
| `maxIterations` | Init Quality Loop | Quality review iterations (default: 3) |
| `timeout` | HTTP Request nodes | API timeout in ms |

## Output Files

After execution, find these in your transcripts directory:

```
/transcripts/
├── summaries/           # Individual file analyses
│   ├── file1.md
│   ├── file2.md
│   └── ...
├── batch-summaries/     # Intermediate batch summaries
│   ├── batch-01.md
│   └── ...
├── combined-analysis.md # Master synthesis document
└── dashboard.html       # Interactive visualization
```

## Claude Bridge Setup

The workflow expects a Claude Bridge service that:

1. Accepts POST requests to `/claude`
2. Body format:
   ```json
   {
     "prompt": "Your instruction here",
     "maxTurns": 15,
     "workingDir": "/transcripts"
   }
   ```
3. Returns:
   ```json
   {
     "result": "Claude's response/output"
   }
   ```
4. Has filesystem access to the transcripts directory
5. Can execute bash commands (for file operations)

### Options for Claude Bridge:

1. **claude-computer-use-demo** - Anthropic's reference implementation
2. **Custom implementation** - Wrap Claude's API with tool use
3. **OpenClaw's claude-bridge** - If using OpenClaw

## Customization

### Changing Analysis Prompts

Each agent has its prompt defined in the `jsonBody` parameter of its HTTP Request node. Edit these to customize:

- What information to extract from transcripts
- How to format the output
- Dashboard sections and styling
- Quality review criteria

### Adjusting for Different Content Types

While designed for lecture transcripts, this workflow can analyze any VTT content:

- Meeting recordings
- Podcast transcripts
- Interview transcripts
- Webinar recordings

Adjust the prompts in the Single File Analyzer and Synthesis Agent to match your content type.

## Troubleshooting

### "No JSON array found in response"
The List Files agent failed to parse VTT filenames. Check:
- Files exist in `/transcripts/`
- Files have `.vtt` extension
- Claude Bridge can access the directory

### Timeout Errors
Large datasets may exceed default timeouts. Increase timeout values in HTTP Request nodes:
- Synthesis Agent: 3600000 (1 hour)
- Visualization Agent: 3600000 (1 hour)
- Questions Completion: 3600000 (1 hour)

### Quality Loop Never Passes
If the quality loop hits max iterations without passing:
1. Check `quality-report.md` for specific failures
2. Some visual criteria may be subjective
3. Consider reducing Visual Design pass threshold from 7/8 to 6/8

## License

MIT License - See [LICENSE](LICENSE)

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Credits

Built with:
- [n8n](https://n8n.io) - Workflow automation
- [Claude](https://anthropic.com) - AI analysis
- [D3.js](https://d3js.org) - Knowledge graph visualization

---

*Created by [@brineshrimp](https://github.com/brineshrimp) / BrineShrimp Games*
