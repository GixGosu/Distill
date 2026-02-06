# Generate Dashboard Prompt

Create an interactive HTML dashboard from the analysis.

## Variables
- `{{dashboardTitle}}` - Title for the dashboard
- `{{primaryColor}}` - Primary brand color (hex)
- `{{secondaryColor}}` - Secondary brand color (hex)
- `{{accentColor}}` - Accent color (hex)
- `{{logoUrl}}` - URL to logo image (optional)
- `{{customCss}}` - Additional CSS rules (optional)
- `{{stylingInstructions}}` - Natural language styling guide
- `{{sections}}` - Array of sections to include
- `{{customExtractors}}` - Array of custom extractor definitions

---

## Prompt

```
You are creating an interactive HTML dashboard from analyzed transcript data.

## Branding
- Dashboard Title: {{dashboardTitle}}
- Primary Color: {{primaryColor}}
- Secondary Color: {{secondaryColor}}
- Accent Color: {{accentColor}}
- Logo URL: {{logoUrl}}

## Custom Styling Instructions
{{stylingInstructions}}

## Custom CSS to Include
{{customCss}}

## Sections to Include
{{sections}}

## Your Task
Read the combined-analysis.md (and analysis-data.json if it exists) and create an engaging HTML dashboard.

## Design Requirements
- Apply the branding colors throughout
- If logo URL provided, display it in the header
- Include the custom CSS in a <style> block
- Follow the custom styling instructions
- Only include the sections specified above

## Technical Requirements
- Single self-contained HTML file
- All CSS/JS inline (except D3.js CDN for knowledge graph)
- Mobile responsive with media queries
- Dark/light mode toggle (localStorage)
- Print stylesheet
- Pagination for large lists (20 per page)
- Search/filter functionality
- Debounced search (300ms)
- Smooth transitions and hover effects
- Accessible (keyboard navigation, ARIA labels)

## Required Components

### Hero Section
- Project title and stats
- Total sessions, questions, topics, tools
- 5-7 key takeaway cards
- Reading mode selector (Quick Scan / Key Points / Full Review)

### Question Explorer
- Searchable accordion/list
- Dynamic category filters (auto-detected from content)
- Frequency badges
- Lazy loading (show 30, "Load More" for rest)
- Source session attribution

### Topic Heatmap
- CSS Grid matrix: topic × session
- Fixed topic labels on left (sticky column)
- Horizontally scrollable sessions
- Binary colors: {{primaryColor}} (covered) / #e5e7eb (not)
- Hover tooltips with details
- Coverage percentage per topic

### Tools & Resources Gallery
- Card grid with category tabs
- Auto-detected categories
- Clickable links (official URL or Google search)
- Session count badges
- Context/description

### Session Navigator
- Paginated cards (20 per page)
- Pagination controls with page numbers
- Session type badge
- Brief description
- "View Summary" and "View Original" buttons
- Search/filter

### Knowledge Graph
- D3.js v7 force-directed graph
- Node types: topic ({{primaryColor}}), tool ({{secondaryColor}}), session ({{accentColor}})
- Node size by connection count
- Filter controls (slider for node count, type checkboxes)
- Draggable nodes
- Click to highlight connections
- Hover tooltips
- Zoom and pan
- Respect dark mode

### Investigation Queue
- Checklist with localStorage persistence
- Priority indicators
- Clear completed option

### Global Search
- Searches all sections
- Highlights matches
- Shows section where found

{{#if customExtractors}}
### Custom Extractor Sections

{{#each customExtractors}}
#### {{name}}
- Display as collapsible list or table
- Include session attribution
- Searchable
- Sortable if applicable
{{/each}}
{{/if}}

## Color Palette
- Primary: {{primaryColor}}
- Secondary: {{secondaryColor}}
- Accent: {{accentColor}}
- Dark mode background: #0f172a
- Dark mode text: #e2e8f0

## Output
Write to dashboard.html
Output: "DASHBOARD_COMPLETE"
```
