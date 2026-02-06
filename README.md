# Transcript Intelligence Dashboard

**Transform any recorded conversation into actionable intelligence.**

An AI-powered n8n workflow that extracts insights from meetings, calls, interviews, and any recorded conversation—then synthesizes them into interactive dashboards and structured data.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![n8n](https://img.shields.io/badge/n8n-1.0+-orange.svg)

## What It Does

1. **Pulls transcripts** directly from Zoom, Google Drive, Otter.ai, S3, or local files
2. **Analyzes each recording** to extract questions, decisions, action items, and insights
3. **Synthesizes across sessions** to find patterns, gaps, and trends
4. **Generates dashboards** with interactive visualizations and knowledge graphs
5. **Exports anywhere** — Google Drive, Notion, Airtable, email, S3

All configurable. All automated. All from a single workflow.

---

## Use Cases

### 🏢 **Meeting Intelligence for Teams**
Analyze weeks of team meetings to surface:
- Recurring blockers and risks
- Decisions made (and by whom)
- Action items that fell through the cracks
- Topics that keep coming up

*"What did we decide about the API migration across all our standups?"*

### 📞 **Sales Call Analysis**
Process recorded sales calls to extract:
- Common objections and responses
- Competitor mentions
- Pricing discussions
- Commitment language and next steps

*"What objections came up most in Q1 demos?"*

### 🎯 **Customer Research Synthesis**
Analyze user interviews and focus groups:
- Pain points by frequency
- Feature requests across segments
- Sentiment patterns
- Quotes for stakeholder presentations

*"What do enterprise customers say about onboarding?"*

### 🎓 **Training & Educational Content**
Process lecture recordings, workshops, webinars:
- Key concepts and definitions
- Q&A index for reference
- Topic coverage heatmap
- Recommended learning paths

*"Create a study guide from this semester's lectures."*

### 🎙️ **Podcast & Content Management**
Analyze podcast episodes for:
- Guest insights and quotable moments
- Topic index across episodes
- Resource/tool mentions
- Cross-episode themes

*"What tools have guests recommended across all episodes?"*

### ⚖️ **Legal & Compliance Review**
Process depositions, hearings, compliance calls:
- Key statements and admissions
- Timeline of events mentioned
- Contradictions across sessions
- Risk flags and red lines

*"Flag all mentions of the contract terms across depositions."*

### 🔬 **Research Interview Analysis**
Synthesize qualitative research:
- Theme extraction across interviews
- Quote attribution
- Coding and categorization
- Gap analysis

*"What themes emerged from the 30 user interviews?"*

### 📊 **Executive Briefing Automation**
Turn meeting recordings into executive summaries:
- Key decisions and rationale
- Risk and blocker summary
- Progress against goals
- Action item status

*"Generate a weekly leadership digest from all department meetings."*

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     SOURCE INTEGRATIONS                          │
│                                                                  │
│   📹 Zoom      📁 Google Drive      🎙️ Otter.ai      ☁️ S3      │
│   Recordings   Shared folders       Live transcripts  Archives   │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT EXTRACTION                        │
│                                                                  │
│   Standard Analysis          Custom Extractors (You Define)     │
│   ├─ Questions & Answers     ├─ "Action Items"                  │
│   ├─ Key Topics              ├─ "Decisions Made"                │
│   ├─ Tools & Resources       ├─ "Risk Flags"                    │
│   ├─ Participants            ├─ "Customer Quotes"               │
│   └─ Notable Insights        └─ "Competitor Mentions"           │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CROSS-SESSION SYNTHESIS                        │
│                                                                  │
│   • Pattern detection across all sessions                       │
│   • Topic frequency and coverage analysis                       │
│   • Question/answer aggregation                                 │
│   • Trend identification                                        │
│   • Gap analysis                                                │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DASHBOARD GENERATION                          │
│                                                                  │
│   📊 Interactive HTML        📋 Structured JSON                  │
│   ├─ Knowledge graph         ├─ All extracted data              │
│   ├─ Topic heatmap           ├─ API-ready format                │
│   ├─ Question explorer       ├─ Import to any tool              │
│   ├─ Session navigator       └─ Programmatic access             │
│   └─ Custom extractor views                                     │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY ASSURANCE                             │
│                                                                  │
│   3-Pass Automated Review:                                      │
│   ✓ Content accuracy         ✓ Visual design                    │
│   ✓ Technical quality        → Auto-fix issues                  │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXPORT DESTINATIONS                           │
│                                                                  │
│   📁 Google Drive    📝 Notion    📊 Airtable                    │
│   ☁️ AWS S3          📧 Email     🔔 Slack/Webhook               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### 🔌 Source Integrations
Pull transcripts automatically from:
- **Zoom Cloud Recordings** — Process meeting recordings directly
- **Google Drive** — Watch folders for new transcripts
- **Otter.ai** — Receive transcripts via webhook
- **AWS S3** — Process archived recordings
- **Local files** — Drop files in a folder

### 🎯 Custom Extractors
Define what matters to YOUR use case:

```json
[
  {
    "name": "Customer Pain Points",
    "pattern": "frustrated|annoying|difficult|hate|problem",
    "instructions": "Extract complaints with context and severity"
  },
  {
    "name": "Competitor Mentions",
    "pattern": "Salesforce|HubSpot|competitor|alternative|switching",
    "instructions": "Note what was said and sentiment"
  },
  {
    "name": "Pricing Discussions",
    "pattern": "price|cost|budget|expensive|discount|deal",
    "instructions": "Extract pricing objections and responses"
  }
]
```

Custom extractors:
- Run **in addition to** standard extraction
- Create dedicated sections in every output
- Are searchable in the dashboard
- Export cleanly to JSON/Airtable

### 📊 Interactive Dashboards
Generated dashboards include:
- **Knowledge Graph** — Visual relationships between topics, tools, and sessions
- **Topic Heatmap** — See what's covered where at a glance
- **Question Explorer** — Searchable Q&A across all sessions
- **Session Navigator** — Paginated session cards with summaries
- **Custom Sections** — Your extractors get their own views

### 🔄 Incremental Processing
- Only process new/changed files
- Resume from failures
- Add to existing analyses
- Track processing state

### ✨ Quality Assurance Loop
Automated 3-pass review ensures professional output:
1. **Content Accuracy** — Data matches sources
2. **Visual Design** — Professional, usable UI
3. **Technical Quality** — Everything works

Issues are auto-fixed. Loop repeats until quality passes.

### 🎨 Full Customization
- Brand colors and logo
- Custom CSS
- Natural language styling instructions
- Select which sections to include

---

## Quick Start

### 1. Import Workflows into n8n
- `workflows/vtt-analyzer-main.json`
- `workflows/vtt-analyzer-single-file.json`

### 2. Configure Claude Bridge
See [docs/claude-bridge-setup.md](docs/claude-bridge-setup.md)

### 3. Run via Configuration Form
Open the form, set your options, submit. That's it.

### 4. Or Trigger via Webhook
```bash
curl -X POST https://your-n8n/webhook/analyze-transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Q1 Sales Calls",
    "sourceIntegration": "Zoom Cloud Recordings",
    "customExtractors": [
      {"name": "Objections", "pattern": "but|however|concern", "instructions": "Extract sales objections"}
    ],
    "exportDestinations": "notion,email"
  }'
```

---

## Supported Input Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| WebVTT | .vtt | Zoom, web players |
| SubRip | .srt | Video editing, YouTube |
| Plain Text | .txt | Otter.ai, manual transcripts |
| JSON | .json | Whisper, AWS Transcribe |

---

## Output Options

### HTML Dashboard
Self-contained, interactive HTML file with:
- D3.js knowledge graph
- Search and filtering
- Dark/light mode
- Mobile responsive
- Print stylesheet

### JSON Data
Structured export for programmatic use:
```json
{
  "metadata": { "projectName": "...", "runId": "..." },
  "summary": { "totalSessions": 47, "keyTakeaways": [...] },
  "sessions": [...],
  "questions": [...],
  "topics": [...],
  "tools": [...],
  "customExtractors": {
    "action_items": [...],
    "decisions": [...],
    "risk_flags": [...]
  }
}
```

---

## Configuration Options

| Category | Options |
|----------|---------|
| **Metadata** | Project name, title, participants, tags, date range |
| **Styling** | Colors, logo URL, custom CSS, styling instructions |
| **Processing** | Output format, incremental mode, sections to include |
| **Quality** | Enable/disable review loop, max iterations |
| **Source** | Integration type, credentials/config |
| **Export** | Destinations (gdrive, notion, s3, email, airtable) |
| **Extractors** | Custom extraction patterns and instructions |
| **Notifications** | Webhook URL for completion alerts |

---

## Example Workflows

### Weekly Team Intelligence
```json
{
  "projectName": "Engineering Weekly",
  "sourceIntegration": "Zoom Cloud Recordings",
  "customExtractors": [
    {"name": "Blockers", "pattern": "blocked|stuck|waiting on"},
    {"name": "Decisions", "pattern": "decided|agreed|let's go with"}
  ],
  "exportDestinations": "notion,slack",
  "processingMode": "Incremental"
}
```

### Quarterly Sales Analysis
```json
{
  "projectName": "Q1 2024 Sales Calls",
  "sourceIntegration": "Google Drive folder",
  "customExtractors": [
    {"name": "Objections", "pattern": "price|budget|competitor"},
    {"name": "Next Steps", "pattern": "follow up|send|schedule|demo"}
  ],
  "exportDestinations": "airtable,gdrive"
}
```

### Research Interview Synthesis
```json
{
  "projectName": "User Research - Onboarding",
  "customExtractors": [
    {"name": "Pain Points", "pattern": "confusing|difficult|frustrated"},
    {"name": "Delight Moments", "pattern": "love|great|easy|amazing"},
    {"name": "Feature Requests", "pattern": "wish|would be nice|should have"}
  ],
  "exportDestinations": "notion"
}
```

---

## Requirements

- **n8n** v1.0+ (self-hosted or cloud)
- **Claude Bridge** — HTTP service for Claude computer use ([setup guide](docs/claude-bridge-setup.md))

---

## License

MIT License — See [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Stop losing insights in recordings. Start building intelligence.**

*Created by [@brineshrimp](https://github.com/brineshrimp) / BrineShrimp Games*
