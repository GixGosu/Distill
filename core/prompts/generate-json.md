# Generate JSON Prompt

Create a structured JSON export of the analysis.

## Variables
- `{{projectName}}` - Project name
- `{{runId}}` - Unique run identifier
- `{{participants}}` - Array of participants
- `{{tags}}` - Array of tags
- `{{dateRange}}` - Date range description
- `{{customExtractors}}` - Array of custom extractor definitions

---

## Prompt

```
Create a structured JSON export of the analysis.

Read combined-analysis.md and create analysis-data.json with this structure:

{
  "metadata": {
    "projectName": "{{projectName}}",
    "generatedAt": "[current ISO timestamp]",
    "runId": "{{runId}}",
    "participants": {{participants}},
    "tags": {{tags}},
    "dateRange": "{{dateRange}}"
  },
  
  "summary": {
    "totalSessions": [count],
    "totalQuestions": [count],
    "totalTopics": [count],
    "totalTools": [count],
    "keyTakeaways": [
      "Takeaway 1",
      "Takeaway 2",
      ...
    ]
  },
  
  "sessions": [
    {
      "id": "session-1",
      "filename": "original-file.vtt",
      "summaryFile": "summaries/original-file.md",
      "title": "Session Title",
      "type": "meeting|lecture|podcast|interview|etc",
      "duration": "XX min",
      "participants": ["Person 1", "Person 2"],
      "summary": "Brief session summary",
      "topics": ["topic1", "topic2"],
      "questionCount": 5,
      "toolCount": 3
    }
  ],
  
  "questions": [
    {
      "id": "q-1",
      "text": "The question that was asked?",
      "answer": "Summary of the answer",
      "category": "auto-detected-category",
      "sessionId": "session-1",
      "sessionTitle": "Session Title",
      "frequency": 1
    }
  ],
  
  "topics": [
    {
      "id": "topic-1",
      "name": "Topic Name",
      "sessions": ["session-1", "session-2"],
      "sessionCount": 2,
      "coverage": 0.75,
      "description": "Brief topic description"
    }
  ],
  
  "tools": [
    {
      "id": "tool-1",
      "name": "Tool Name",
      "type": "software|website|book|framework|service",
      "url": "https://...",
      "sessions": ["session-1"],
      "sessionCount": 1,
      "context": "How/why the tool was mentioned"
    }
  ],
  
  "heatmap": {
    "topics": ["topic1", "topic2", ...],
    "sessions": ["session-1", "session-2", ...],
    "data": [
      [1, 0, 1, ...],  // topic1 coverage
      [1, 1, 0, ...],  // topic2 coverage
      ...
    ]
  },
  
  "crossSessionInsights": {
    "commonThemes": ["Theme 1", "Theme 2"],
    "uniqueContributions": [
      {"session": "session-1", "contribution": "Unique concept"}
    ],
    "knowledgeGaps": ["Gap 1", "Gap 2"]
  },
  
  "investigationPriorities": [
    {
      "topic": "Topic to investigate",
      "reason": "Why it's important",
      "priority": "high|medium|low"
    }
  ],
  
  "recommendedOrder": [
    {
      "order": 1,
      "sessionId": "session-5",
      "reason": "Good starting point because..."
    }
  ]
  
  {{#if customExtractors}}
  ,
  "customExtractors": {
    {{#each customExtractors}}
    "{{toLowerCase (replace name ' ' '_')}}": [
      {
        "text": "Extracted item",
        "sessionId": "session-1",
        "context": "Additional context"
      }
    ]{{#unless @last}},{{/unless}}
    {{/each}}
  }
  {{/if}}
}

Extract ALL data from combined-analysis.md. Do not truncate or sample.

Output: "JSON_EXPORT_COMPLETE"
```
