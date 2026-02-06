# Visual Design Review Prompt

Review the dashboard for visual design and UX quality.

---

## Prompt

```
You are reviewing the dashboard for VISUAL DESIGN & UX.

Read dashboard.html and analyze the CSS and HTML structure.

## Verification Criteria

### 1. Visual Hierarchy
- Are key insights in hero section prominent?
- Large fonts for important numbers?
- Contrasting colors for emphasis?
- Clear section separation?

### 2. Color Consistency
- Is the primary brand color used correctly?
- Is secondary color used for accents/secondary elements?
- Is accent color used sparingly for highlights?
- Consistent throughout all sections?

### 3. Typography
- Header sizes appropriate (2rem+ for h1, scaling down)?
- Body text readable (1rem, line-height 1.5+)?
- Font weights used meaningfully?
- Consistent font family?

### 4. Whitespace
- Padding/margins balanced?
- Not cramped?
- Not too sparse?
- Consistent spacing rhythm?

### 5. Interactive Feedback
- Hover states defined with transitions?
- Focus states visible (accessibility)?
- Cursor changes on interactive elements?
- Click feedback present?

### 6. Mobile Responsive
- Media queries present?
- Flexbox/grid used for layout?
- Touch targets adequate size (44px+)?
- Content readable on small screens?

### 7. Progressive Disclosure
- Accordions/expandables for detailed content?
- "Load More" for long lists?
- Pagination for large datasets?
- Sensible default collapsed states?

### 8. Professional Aesthetic
- Clean, modern design?
- Would pass enterprise/business review?
- No amateurish elements?
- Consistent visual language?

## Output Format

Return JSON only, no other text:

{
  "dimension": "visual_design",
  "criteria": {
    "visual_hierarchy": {
      "pass": true,
      "note": "Hero stats prominent, clear section headers"
    },
    "color_consistency": {
      "pass": true,
      "note": "Brand colors applied correctly"
    },
    "typography": {
      "pass": false,
      "note": "Body line-height is 1.3, should be 1.5+"
    },
    "whitespace": {
      "pass": true,
      "note": "Good spacing rhythm"
    },
    "interactive_feedback": {
      "pass": true,
      "note": "Hover transitions present"
    },
    "mobile_responsive": {
      "pass": true,
      "note": "Media queries at 768px and 480px"
    },
    "progressive_disclosure": {
      "pass": true,
      "note": "Accordions and pagination present"
    },
    "professional_aesthetic": {
      "pass": true,
      "note": "Clean, business-appropriate"
    }
  },
  "pass_count": 7,
  "overall_pass": false,
  "issues": [
    "Line-height too tight for body text"
  ],
  "recommendations": [
    "Increase body line-height to 1.5 or 1.6"
  ]
}

Pass condition: 7+ of 8 criteria must pass.
```
