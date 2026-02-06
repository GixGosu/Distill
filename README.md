# VTT Transcript Analyzer for n8n

A powerful, fully-configurable n8n workflow that analyzes transcript files at scale, generates comprehensive summaries, and creates interactive HTML dashboards.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![n8n](https://img.shields.io/badge/n8n-1.0+-orange.svg)

## Features

### Input
- **Multi-Format**: VTT, SRT, TXT, JSON transcripts
- **Source Integrations**: Local files, Zoom, Google Drive, Otter.ai, S3
- **Incremental Processing**: Only process new/changed files

### Processing
- **Parallel Analysis**: Process multiple files simultaneously
- **Custom Extractors**: Define your own extraction patterns
- **Quality Review Loop**: 3-pass automated quality assurance
- **Error Recovery**: Continue processing on individual file failures

### Output
- **Dual Format**: HTML dashboard and/or JSON data
- **Custom Branding**: Colors, logo, CSS, styling instructions
- **Export Destinations**: Google Drive, Notion, S3, Email, Airtable

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         TRIGGERS                                      │
│   Manual  │  Webhook POST  │  Configuration Form                     │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    SOURCE INTEGRATION                                 │
│  Local Files │ Zoom API │ Google Drive │ Otter.ai │ AWS S3          │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   FILE ANALYSIS (Parallel)                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                                │
│  │ File 1  │ │ File 2  │ │ File 3  │ ...  (with custom extractors) │
│  └─────────┘ └─────────┘ └─────────┘                                │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   SYNTHESIS & OUTPUT                                  │
│  Hierarchical Synthesis → JSON Export → HTML Dashboard               │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   QUALITY REVIEW LOOP (Optional)                     │
│  Content Review → Visual Review → Technical Review → Improve         │
│                        (up to 3 iterations)                          │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   EXPORT DESTINATIONS                                 │
│  Google Drive │ Notion │ S3 │ Email │ Airtable                      │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
                    Notification (Slack, etc.)
```

## Quick Start

### 1. Import Workflows
- `workflows/vtt-analyzer-main.json`
- `workflows/vtt-analyzer-single-file.json`

### 2. Link Subworkflow
In main workflow, configure "Analyze Files (Parallel)" to point to the single file analyzer.

### 3. Set Up Claude Bridge
See [docs/claude-bridge-setup.md](docs/claude-bridge-setup.md)

### 4. Run
Open Configuration Form, fill options, submit.

## Configuration Reference

### Metadata
| Field | Description |
|-------|-------------|
| Project Name | Name for this analysis run |
| Dashboard Title | Title shown in dashboard |
| Participants | Comma-separated participant names |
| Tags | Comma-separated tags |
| Date Range | Date range description |

### Styling
| Field | Description |
|-------|-------------|
| Primary Color | Main brand color (hex) |
| Secondary Color | Secondary color (hex) |
| Logo URL | URL to logo image |
| Custom CSS | Additional CSS rules |
| Styling Instructions | Natural language styling guide |

### Processing
| Field | Options |
|-------|---------|
| Output Format | HTML Only, JSON Only, Both |
| Processing Mode | Full, Incremental |
| Sections to Include | all, or: questions,topics,tools,sessions,graph,heatmap |

### Quality Review
| Field | Description |
|-------|-------------|
| Enable Quality Review | Yes (recommended) / No (faster) |
| Max Iterations | Number of improvement cycles (default: 3) |

### Source Integration
| Source | Config Required |
|--------|-----------------|
| Local files | None (default) |
| Zoom Cloud | API credentials |
| Google Drive | Folder ID, API key |
| Otter.ai | Webhook receives data |
| AWS S3 | Bucket, prefix, credentials |

```json
// Example source config
{
  "folderId": "abc123",
  "apiKey": "your-api-key"
}
```

### Export Destinations
| Destination | Config Required |
|-------------|-----------------|
| local | None (default) |
| gdrive | Folder ID |
| notion | Database ID, API key |
| s3 | Bucket, prefix |
| email | To address |
| airtable | Base ID, table names |

```json
// Example export config
{
  "gdrive": { "folderId": "abc123" },
  "email": { "to": "team@example.com" },
  "s3": { "bucket": "my-bucket", "prefix": "analyses/" }
}
```

### Custom Extractors

Define your own extraction patterns that work **in addition to** standard extraction:

```json
[
  {
    "name": "Action Items",
    "pattern": "action item|todo|assigned to|will do",
    "instructions": "Extract all action items with owner and deadline if mentioned"
  },
  {
    "name": "Decisions Made",
    "pattern": "decided|agreed|confirmed|approved",
    "instructions": "Extract all decisions with context and who made them"
  },
  {
    "name": "Risk Flags",
    "pattern": "risk|concern|blocker|issue|problem",
    "instructions": "Extract anything flagged as a risk or concern"
  },
  {
    "name": "Budget References",
    "pattern": "\\$|dollar|budget|cost|spend",
    "instructions": "Extract all budget and cost references with amounts"
  }
]
```

Custom extractors:
- Create dedicated sections in each file summary
- Are aggregated in the combined analysis
- Appear as separate sections in the dashboard
- Are included in JSON export under `customExtractors`

## Quality Review Loop

When enabled, the dashboard undergoes automated review:

### Pass 1: Content Accuracy
- Session count matches
- Questions complete
- Topics complete
- Tools listed
- No fabricated data
- Summary accurate

### Pass 2: Visual Design
- Visual hierarchy
- Color consistency
- Typography
- Whitespace
- Interactive feedback
- Mobile responsive
- Progressive disclosure
- Professional aesthetic

### Pass 3: Technical Quality
- Valid HTML
- CSS loads
- JS executes
- Search works
- Dark mode works
- Links work
- localStorage works
- Print stylesheet

After each review, the Improvement Agent fixes identified issues. Loop continues until all pass or max iterations reached.

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| WebVTT | .vtt | Standard web subtitles |
| SubRip | .srt | Common subtitle format |
| Plain Text | .txt | Raw transcripts |
| JSON | .json | Whisper, AWS Transcribe, etc. |

## Output Files

```
/transcripts/
├── .status.json              # Real-time processing status
├── .processing-state.json    # State for incremental mode
├── summaries/                # Individual file analyses
├── batch-summaries/          # Intermediate batch summaries
├── combined-analysis.md      # Master synthesis
├── analysis-data.json        # Structured JSON (if enabled)
└── dashboard.html            # Interactive dashboard (if enabled)
```

## Webhook API

```bash
POST /webhook/analyze-transcripts
Content-Type: application/json

{
  "projectName": "Q1 Meetings",
  "outputFormat": "Both HTML and JSON",
  "processingMode": "Incremental (new/changed only)",
  "primaryColor": "#0066cc",
  "enableQualityReview": "Yes (recommended)",
  "exportDestinations": "gdrive,email",
  "exportConfig": {
    "gdrive": { "folderId": "..." },
    "email": { "to": "team@example.com" }
  },
  "customExtractors": [
    { "name": "Action Items", "pattern": "action|todo", "instructions": "..." }
  ],
  "notificationWebhook": "https://hooks.slack.com/..."
}
```

## Error Handling

- Individual file failures don't stop the pipeline
- Errors logged in `.status.json`
- Failed files listed in final output
- Can be retried on next incremental run

## Performance Tips

1. **Use Incremental Mode** for subsequent runs
2. **Disable Quality Review** for faster processing during development
3. **Limit Sections** to only what you need
4. **Increase Timeouts** for large datasets (100+ files)

## License

MIT License - See [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Created by [@brineshrimp](https://github.com/brineshrimp) / BrineShrimp Games*
