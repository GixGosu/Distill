# Technical Quality Review Prompt

Review the dashboard for technical quality and functionality.

---

## Prompt

```
You are reviewing the dashboard for TECHNICAL QUALITY.

Read dashboard.html and analyze HTML, CSS, and JavaScript.

## Verification Criteria

### 1. Valid HTML
- DOCTYPE present?
- Proper tag nesting?
- All tags closed?
- Required attributes present (alt, etc.)?
- No deprecated elements?

### 2. CSS Loads
- <style> block present?
- Selectors valid?
- No syntax errors?
- Properties correctly formatted?
- Media queries properly structured?

### 3. JS Executes
- <script> block present?
- No syntax errors?
- Functions properly defined?
- Event listeners attached?
- No undefined references?

### 4. Search Works
- Search input element exists?
- Connected to filter function?
- Debouncing implemented?
- Searches across all data (not just visible)?
- Results update dynamically?

### 5. Dark Mode Works
- Toggle button present?
- CSS variables for theme colors?
- localStorage code for persistence?
- All sections respect theme?
- No hardcoded colors breaking dark mode?

### 6. Links Work
- All href values valid?
- Relative paths correct (summaries/*.md)?
- External links have target="_blank"?
- No broken anchor links?

### 7. localStorage Works
- Code to save user preferences?
- Code to restore on load?
- Checkbox states persist?
- Investigation queue persists?
- Dark mode preference persists?

### 8. Print Stylesheet
- @media print rules present?
- Hides interactive elements for print?
- Readable on paper?
- Appropriate page breaks?

## Output Format

Return JSON only, no other text:

{
  "dimension": "technical_quality",
  "criteria": {
    "valid_html": {
      "pass": true,
      "note": "DOCTYPE present, proper structure"
    },
    "css_loads": {
      "pass": true,
      "note": "2847 lines of valid CSS"
    },
    "js_executes": {
      "pass": false,
      "note": "Uncaught ReferenceError: filterQuestions not defined"
    },
    "search_works": {
      "pass": false,
      "note": "Depends on missing filterQuestions function"
    },
    "dark_mode_works": {
      "pass": true,
      "note": "Toggle, CSS vars, and localStorage all present"
    },
    "links_work": {
      "pass": true,
      "note": "47 internal links verified"
    },
    "localstorage_works": {
      "pass": true,
      "note": "Save/restore for theme, checkboxes, queue"
    },
    "print_stylesheet": {
      "pass": true,
      "note": "@media print rules present"
    }
  },
  "overall_pass": false,
  "issues": [
    "filterQuestions function not defined",
    "Search functionality broken"
  ],
  "recommendations": [
    "Add missing filterQuestions function",
    "Connect search input to filter logic"
  ]
}

Pass condition: ALL 8 criteria must pass. Technical quality must be flawless.
```
