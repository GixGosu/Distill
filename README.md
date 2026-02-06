# VTT Transcript Analyzer for n8n

A powerful, configurable n8n workflow that analyzes transcript files at scale, generates comprehensive summaries, and creates interactive HTML dashboards with visualizations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![n8n](https://img.shields.io/badge/n8n-1.0+-orange.svg)

## Features

### Core Capabilities
- **Multi-Format Support** - VTT, SRT, TXT, and JSON transcripts
- **Batch Processing** - Handles 100+ files with parallel processing
- **Incremental Mode** - Only process new/changed files
- **Intelligent Synthesis** - Cross-session analysis with topic heatmaps
- **Dual Output** - HTML dashboard and/or JSON data export

### Dashboard Features
- Interactive D3.js knowledge graph
- Question explorer with dynamic filters
- Topic coverage heatmap
- Session navigator with pagination
- Dark/light mode toggle
- Global search
- Mobile responsive

### Configuration Options
- Custom branding (colors, logo, CSS)
- Styling instructions via prompt
- Selectable output sections
- Webhook trigger for automation
- Completion notifications (Slack, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIGGER OPTIONS                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│ Manual Trigger  │ Webhook POST    │ Configuration Form      │
└────────┬────────┴────────┬────────┴────────────┬────────────┘
         └─────────────────┼─────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CONFIGURATION & INITIALIZATION                  │
├─────────────────────────────────────────────────────────────┤
│ • Merge config from all sources                             │
│ • Initialize status tracking                                │
│ • Set branding, output format, processing mode              │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   FILE DISCOVERY                             │
├─────────────────────────────────────────────────────────────┤
│ • List .vtt, .srt, .txt, .json files                        │
│ • Check processing state for incremental mode               │
│ • Filter to only new/changed files                          │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              PARALLEL FILE ANALYSIS                          │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│ │ File 1      │  │ File 2      │  │ File 3      │  ...     │
│ │ (Subflow)   │  │ (Subflow)   │  │ (Subflow)   │          │
│ └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│        │ Error Recovery │                │                  │
│        └────────────────┴────────────────┘                  │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              HIERARCHICAL SYNTHESIS                          │
├─────────────────────────────────────────────────────────────┤
│ • Batch processing (20 files per batch)                     │
│ • Create batch summaries                                    │
│ • Generate combined-analysis.md                             │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT GENERATION                         │
├──────────────────────────┬──────────────────────────────────┤
│   JSON Export            │   HTML Dashboard                 │
│   (if selected)          │   (if selected)                  │
│   → analysis-data.json   │   → dashboard.html               │
│                          │   → + Knowledge Graph            │
└──────────────────────────┴──────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETION                                │
├─────────────────────────────────────────────────────────────┤
│ • Save processing state (for incremental mode)              │
│ • Write final status                                        │
│ • Send notification (if configured)                         │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

- **n8n** v1.0+ (self-hosted or cloud)
- **Claude Bridge** - HTTP service providing Claude computer use capabilities

## Quick Start

### 1. Set Up Credentials

Create an HTTP Header Auth credential in n8n:

1. Go to **Credentials** → **Add Credential**
2. Select **HTTP Header Auth**
3. Name: `Claude Bridge`
4. Name field: `Authorization` (or leave empty if not needed)
5. Value field: Your auth token (or leave empty)
6. In workflow, set the credential and update URLs

Or simply update the default URL in each HTTP Request node.

### 2. Import Workflows

1. Import `workflows/vtt-analyzer-main.json`
2. Import `workflows/vtt-analyzer-single-file.json`
3. Link the subworkflow in "Analyze Files (Max 3 Parallel)" node

### 3. Configure Claude Bridge

See [docs/claude-bridge-setup.md](docs/claude-bridge-setup.md) for detailed setup.

### 4. Run Analysis

**Option A: Configuration Form**
1. Open the workflow
2. Click on "Configuration Form" node
3. Click "Test URL" to open the form
4. Fill in options and submit

**Option B: Webhook**
```bash
curl -X POST http://your-n8n:5678/webhook/analyze-transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Q1 Meetings",
    "outputFormat": "Both HTML and JSON",
    "processingMode": "Incremental (new/changed files only)",
    "primaryColor": "#0066cc",
    "notificationWebhook": "https://hooks.slack.com/..."
  }'
```

**Option C: Manual**
Click "Execute Workflow" with default settings.

## Configuration Options

### Metadata
| Field | Description | Default |
|-------|-------------|---------|
| Project Name | Name for this analysis | "Transcript Analysis" |
| Dashboard Title | Title shown in dashboard | "Transcript Analysis Dashboard" |
| Participants | Comma-separated list | (empty) |
| Tags | Comma-separated list | (empty) |
| Date Range | Date range description | (empty) |

### Styling
| Field | Description | Default |
|-------|-------------|---------|
| Primary Color | Main brand color | #2563eb |
| Secondary Color | Secondary color | #7c3aed |
| Logo URL | URL to logo image | (none) |
| Custom CSS | Additional CSS rules | (none) |
| Styling Instructions | Natural language styling guide | "Clean, professional design" |

### Processing
| Field | Description | Options |
|-------|-------------|---------|
| Output Format | What to generate | HTML Only, JSON Only, Both |
| Processing Mode | How to handle existing files | Full, Incremental |
| Sections to Include | Dashboard sections | all, or comma-separated list |
| Notification Webhook | URL for completion notification | (none) |

### Available Sections
- `summary` - Executive summary and stats
- `questions` - Question explorer
- `topics` - Topic coverage
- `tools` - Tools & resources gallery
- `sessions` - Session navigator
- `graph` - Knowledge graph
- `heatmap` - Topic heatmap

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| WebVTT | .vtt | Standard web subtitles with timestamps |
| SubRip | .srt | Common subtitle format |
| Plain Text | .txt | Raw transcripts (no timestamps) |
| JSON | .json | Whisper, AWS Transcribe, or simple format |

## Output Files

```
/transcripts/
├── .status.json           # Real-time processing status
├── .processing-state.json # State for incremental mode
├── summaries/             # Individual file analyses
│   ├── meeting1.md
│   ├── podcast2.md
│   └── ...
├── batch-summaries/       # Intermediate batch summaries
├── combined-analysis.md   # Master synthesis document
├── analysis-data.json     # Structured JSON export (if selected)
└── dashboard.html         # Interactive dashboard (if selected)
```

## Status Tracking

Monitor progress via `/transcripts/.status.json`:

```json
{
  "status": "processing",
  "phase": "individual_analysis",
  "runId": "run-1706789123456",
  "progress": {
    "filesDiscovered": 47,
    "filesProcessed": 23,
    "filesFailed": 1,
    "filesSkipped": 12,
    "currentFile": "meeting-2024-01-15.vtt"
  },
  "errors": [
    { "file": "corrupted.vtt", "error": "Invalid VTT format" }
  ],
  "lastUpdated": "2024-02-01T10:30:00Z"
}
```

## Error Handling

The workflow continues processing even if individual files fail:

- Failed files are logged in status.json
- Error details included in final output
- Partial results still generate dashboard
- Failed files can be retried on next run (incremental mode)

## Incremental Processing

In incremental mode, files are tracked by a hash of:
- Filename
- File size
- Modification time

Only files that have changed since the last run are reprocessed. This dramatically speeds up subsequent runs.

## API/JSON Output

When JSON output is enabled, `analysis-data.json` contains:

```json
{
  "metadata": {
    "projectName": "...",
    "generatedAt": "...",
    "runId": "...",
    "participants": [],
    "tags": []
  },
  "summary": {
    "totalSessions": 47,
    "totalQuestions": 312,
    "totalTopics": 28,
    "totalTools": 45,
    "keyTakeaways": ["..."]
  },
  "sessions": [...],
  "questions": [...],
  "topics": [...],
  "tools": [...],
  "heatmap": {
    "topics": [...],
    "sessions": [...],
    "data": [[...]]
  }
}
```

## Custom Styling

### Via Styling Instructions

Use natural language to describe your preferences:

```
"Make it minimalist with lots of whitespace. 
Use a dark theme by default. 
Cards should have subtle shadows and rounded corners.
Headers should use a serif font for elegance."
```

### Via Custom CSS

Add specific CSS overrides:

```css
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
```

## Webhook Integration

### Triggering via Webhook

```bash
curl -X POST https://your-n8n/webhook/analyze-transcripts \
  -H "Content-Type: application/json" \
  -d @config.json
```

### Completion Notifications

Supports any webhook-compatible service:
- Slack (incoming webhooks)
- Discord (webhooks)
- Microsoft Teams (connectors)
- Custom endpoints

Notification payload:
```json
{
  "text": "✅ Transcript Analysis Complete\n\nProject: Q1 Meetings\nRun ID: run-123456\n\nOutputs:\n• dashboard: /transcripts/dashboard.html\n• jsonData: /transcripts/analysis-data.json"
}
```

## Troubleshooting

### File Not Found Errors
- Verify transcripts are in `/transcripts/` directory
- Check file permissions
- Ensure Claude Bridge has volume mount access

### Timeout Errors
Increase timeouts in HTTP Request nodes:
- Synthesis Agent: 3600000 (1 hour)
- HTML Generation: 3600000 (1 hour)
- Single file: 600000 (10 minutes)

### Incremental Mode Not Working
- Delete `.processing-state.json` to force full reprocess
- Check that files have different modification times

### Dashboard Styling Issues
- Verify CSS syntax in Custom CSS field
- Check that colors are valid hex codes
- Use browser dev tools to debug

## License

MIT License - See [LICENSE](LICENSE)

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## Credits

Built with:
- [n8n](https://n8n.io) - Workflow automation
- [Claude](https://anthropic.com) - AI analysis
- [D3.js](https://d3js.org) - Knowledge graph visualization

---

*Created by [@brineshrimp](https://github.com/brineshrimp) / BrineShrimp Games*
