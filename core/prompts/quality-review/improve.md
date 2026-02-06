# Improvement Agent Prompt

Fix issues identified by quality reviewers.

## Variables
- `{{iteration}}` - Current iteration number
- `{{maxIterations}}` - Maximum iterations allowed
- `{{totalIssues}}` - Total number of issues found
- `{{issues}}` - Array of issue descriptions
- `{{recommendations}}` - Array of recommendations
- `{{contentPass}}` - Whether content review passed
- `{{visualPass}}` - Whether visual review passed
- `{{technicalPass}}` - Whether technical review passed

---

## Prompt

```
You are improving the dashboard based on review feedback.

## Review Results (Iteration {{iteration}} of {{maxIterations}})

### Issues Found ({{totalIssues}} total):
{{#each issues}}
{{@index}}. {{this}}
{{/each}}

### Recommendations:
{{#each recommendations}}
{{@index}}. {{this}}
{{/each}}

### Review Status:
- Content Accuracy: {{#if contentPass}}PASS{{else}}FAIL{{/if}}
- Visual Design: {{#if visualPass}}PASS{{else}}FAIL{{/if}}
- Technical Quality: {{#if technicalPass}}PASS{{else}}FAIL{{/if}}

## Your Task
1. Read dashboard.html
2. Fix ALL issues identified above
3. Write the improved version

## Priority Order
1. **Technical issues** (must all pass - these break functionality)
2. **Content accuracy issues** (must all pass - incorrect data is unacceptable)
3. **Visual design issues** (fix as many as possible)

## Rules
- Do NOT remove working functionality
- Preserve ALL existing data and content
- Make targeted fixes for identified issues
- Ensure the file remains a valid, complete HTML document
- Test your changes mentally before writing

## Common Fixes

### For missing functions:
- Define the function before it's called
- Ensure proper scope

### For broken search:
- Connect input event listener
- Implement filter logic
- Update display after filtering

### For missing data:
- Read from combined-analysis.md
- Add missing items to appropriate section

### For styling issues:
- Check CSS property syntax
- Verify color values are valid hex
- Ensure media queries are properly closed

## Output
Write the improved dashboard.html
After fixing, output: "IMPROVEMENTS COMPLETE: Fixed X issues"
```
