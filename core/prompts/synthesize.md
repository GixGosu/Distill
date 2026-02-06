# Synthesize Prompt

Create a comprehensive synthesis across all analyzed transcript files.

## Variables
- `{{projectName}}` - Name of the project
- `{{participants}}` - Comma-separated list of participants
- `{{tags}}` - Comma-separated list of tags
- `{{dateRange}}` - Date range description
- `{{successCount}}` - Number of successfully processed files
- `{{skippedCount}}` - Number of skipped files
- `{{failedCount}}` - Number of failed files
- `{{customExtractors}}` - Array of custom extractor definitions

---

## Prompt

```
You are creating a comprehensive synthesis of analyzed transcript files.

## Project Context
- Project Name: {{projectName}}
- Participants: {{participants}}
- Tags: {{tags}}
- Date Range: {{dateRange}}

## Processing Summary
- Files successfully processed: {{successCount}}
- Files skipped (unchanged): {{skippedCount}}
- Files failed: {{failedCount}}

## CRITICAL: Hierarchical Processing Required
Due to potentially large number of files, you MUST use a batch processing approach:

### Step 1: Count and Batch
1. List all .md files in the summaries directory
2. Count the total number of files
3. Divide into batches of 20 files each (alphabetically)

### Step 2: Create Batch Summaries
For each batch, create a batch summary file:
- batch-summaries/batch-01.md (files 1-20)
- batch-summaries/batch-02.md (files 21-40)
- etc.

Each batch summary should contain:
- List of files in that batch
- Key questions from those files
- Tools mentioned
- Main topics covered
- Notable insights

### Step 3: Meta Synthesis
After all batch summaries are created, read ONLY the batch summary files to create the final combined-analysis.md

## Required Sections in combined-analysis.md

### Executive Summary
- Total sessions analyzed
- Overall themes and focus areas
- Key takeaways in 5-7 bullet points

### Question Frequency Analysis
Create a table:
| Question/Topic | Times Asked | Sessions |
|---------------|-------------|----------|
| [question pattern] | [count] | [list] |

Identify:
- Most frequently asked questions (top 10)
- Questions asked in multiple sessions
- Unanswered or recurring questions

### Topic Heatmap Data
Binary coverage matrix (X = covered, - = not covered):

| Topic | Session 1 | Session 2 | Session 3 | ... | Coverage % |
|-------|-----------|-----------|-----------|-----|------------|
| [topic] | X | X | - | ... | 67% |

Include:
- Topics appearing in 3+ sessions (high overlap)
- Topics unique to single sessions

### Cross-Session Insights

#### Common Themes
- Themes reinforced across multiple sessions
- Consistent recommendations
- Shared terminology

#### Unique Contributions
- Concepts only in one session
- Alternative viewpoints
- Specialized deep-dives

#### Knowledge Gaps
- Topics mentioned but not explained
- Prerequisites assumed
- Areas needing research

### Tools & Resources Compendium
| Resource | Type | Sessions | Context |
|----------|------|----------|---------|
| [name] | [tool/site/book/etc] | [list] | [why mentioned] |

### Investigation Priorities
Things warranting further research:
1. [Topic] - [Why investigate]
2. ...

### Recommended Review Order
Recommended order for consuming this content:
1. Start with: [session] - [reason]
2. Then: [session] - [builds on concepts]
3. ...

### Master Q&A Index
All questions across all sessions, organized by topic:

#### [Topic Category]
- Q: [question] → A: [brief answer] (Session X)
- Q: [question] → A: [brief answer] (Session Y)

### Session Quick Reference
For each session, provide a 2-line summary with link reference:
- **[Session Name]** (summaries/filename.md): [One-line description]

{{#if customExtractors}}
### Custom Extractor Aggregations

{{#each customExtractors}}
#### {{name}}
Aggregate all "{{name}}" data from individual summaries into a combined view.
{{/each}}
{{/if}}

## Output
Write the complete synthesis to combined-analysis.md
After completing, output: "SYNTHESIS COMPLETE"
```
