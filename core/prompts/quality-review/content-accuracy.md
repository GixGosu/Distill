# Content Accuracy Review Prompt

Review the dashboard for content accuracy against source data.

---

## Prompt

```
You are reviewing the dashboard for CONTENT ACCURACY.

Read these files:
1. combined-analysis.md (source of truth)
2. dashboard.html (what we're reviewing)
3. Sample files from summaries/ directory

## Verification Criteria

### 1. Sessions Complete
- Count session cards in dashboard
- Count .md files in summaries/
- Must match exactly

### 2. Question Count
- Count questions in dashboard's Question Explorer
- Count questions in combined-analysis.md Master Q&A Index
- Should match (allow small variance for deduplication)

### 3. Topics Complete
- Count topics in dashboard heatmap
- Count unique topics in combined-analysis.md
- Must match

### 4. Tools Listed
- Count tools in dashboard
- Count tools in combined-analysis.md Tools & Resources Compendium
- Must match

### 5. No Fabrication
- Randomly select 3 specific facts from dashboard
- Verify each exists in source files
- All must be traceable

### 6. Summary Accurate
- Check executive summary claims
- Verify numbers match actual data
- Verify key takeaways are supported by content

## Output Format

Return JSON only, no other text:

{
  "dimension": "content_accuracy",
  "criteria": {
    "sessions_complete": {
      "pass": true,
      "dashboard_count": 47,
      "source_count": 47,
      "note": "All sessions present"
    },
    "question_count": {
      "pass": true,
      "dashboard_count": 312,
      "source_count": 315,
      "note": "3 duplicates removed"
    },
    "topics_complete": {
      "pass": true,
      "note": "28 topics match"
    },
    "tools_listed": {
      "pass": false,
      "dashboard_count": 42,
      "source_count": 45,
      "note": "Missing: Tool X, Tool Y, Tool Z"
    },
    "no_fabrication": {
      "pass": true,
      "checked": ["Fact 1", "Fact 2", "Fact 3"],
      "note": "All verified in sources"
    },
    "summary_accurate": {
      "pass": true,
      "note": "Numbers and claims verified"
    }
  },
  "overall_pass": false,
  "issues": [
    "Missing 3 tools from Tools section"
  ],
  "recommendations": [
    "Add missing tools: Tool X, Tool Y, Tool Z"
  ]
}
```
