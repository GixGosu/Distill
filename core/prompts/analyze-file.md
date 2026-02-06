# Analyze File Prompt

Analyze a single transcript file with format handling and custom extraction.

## Variables
- `{{filename}}` - Name of the file to analyze
- `{{format}}` - File format (vtt, srt, txt, json)
- `{{formatName}}` - Human-readable format name
- `{{fileIndex}}` - Current file number
- `{{totalFiles}}` - Total files being processed
- `{{outputPath}}` - Where to write the summary
- `{{customExtractors}}` - JSON array of custom extractors

---

## Prompt

```
You are analyzing a transcript file. Handle format conversion if needed.

## File Information
- Filename: {{filename}}
- Format: {{formatName}} (.{{format}})
- Processing: File {{fileIndex}} of {{totalFiles}}

## Format-Specific Handling

### If .srt (SubRip):
SubRip format uses numbered sequences:
1
00:00:01,000 --> 00:00:05,000
Text here

Parse the timestamps and text, ignore sequence numbers.

### If .txt (Plain Text):
No timestamps available. Focus on content extraction.

### If .json (Structured):
Look for common structures:
- { "segments": [{ "text": "...", "start": 0, "end": 5 }] } (Whisper)
- { "results": { "transcripts": [...] } } (AWS Transcribe)
- { "transcript": "..." } (Simple format)

### If .vtt (WebVTT):
Standard WebVTT with WEBVTT header and timestamps.

## Your Task
1. Read the transcript file
2. Create output directory if needed
3. Create comprehensive analysis

## Content Type Detection
First, identify the content type:
- Meeting (internal team, client, etc.)
- Lecture/Educational session
- Podcast episode
- Interview (job, media, research)
- Conference talk/presentation
- Customer call (sales, support)
- Focus group/User research
- Webinar
- Other

## Standard Extraction

### Participants & Roles
- Who is speaking (names, roles, or speaker labels)
- Number of distinct speakers
- Primary speaker vs others

### Questions & Discussion Points
- Questions asked by anyone
- Answers or responses given
- Points of clarification requested
- Unresolved questions or deferred items

### Key Content
- Main topics discussed (in order of appearance)
- Key points, decisions, or conclusions
- Important facts, figures, or data mentioned
- Technical terms or jargon used (with context)

### Actionable Items
- Action items or tasks assigned
- Deadlines or commitments mentioned
- Follow-up items needed
- Tools, resources, or references cited

### Notable Moments
- Key insights or revelations
- Points of agreement or disagreement
- Emotional moments or tone shifts
- Surprising information

{{#if customExtractors}}
## Custom Extractors (REQUIRED - Add these sections)

{{#each customExtractors}}
### {{name}}
- Pattern to match: {{pattern}}
- Instructions: {{instructions}}
- Output as a dedicated section in the summary
{{/each}}
{{/if}}

## Output Format
Write to {{outputPath}}:

# [Title/Subject]

**Source**: {{filename}}
**Type**: [Content type]
**Format**: {{formatName}}
**Duration**: ~XX minutes (if determinable)
**Participants**: [List if identifiable]

## Key Questions & Responses
[Extract all Q&A]

## Main Topics Covered
[Topic summaries with key points]

## Action Items & Follow-ups
- [ ] [Action items if any]

## Tools & Resources Mentioned
[List with context]

## Notable Quotes & Insights
[Key quotes and observations]

## Summary
[3-5 sentence overview]

{{#each customExtractors}}
## {{name}}
[Extracted data for {{name}}]

{{/each}}

## Instructions
- Be thorough - capture EVERYTHING of value
- Adapt to the content type
- Note if the format caused any parsing issues
- After writing, output only: "COMPLETE: {{filename}}"
```
