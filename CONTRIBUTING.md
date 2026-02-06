# Contributing to VTT Transcript Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributions.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - n8n version
   - Claude Bridge setup details
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the use case
3. Explain the proposed solution
4. Note any alternatives considered

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test with real VTT files
5. Commit with clear messages
6. Push and open a Pull Request

## Development Guidelines

### Workflow Changes

When modifying n8n workflows:

1. **Export as JSON** - Use n8n's export function
2. **Preserve node IDs** - Don't regenerate IDs unnecessarily
3. **Test the full pipeline** - Run with at least 5-10 VTT files
4. **Document prompt changes** - Explain why prompts were modified

### Code Style

For JavaScript in Code nodes:

- Use descriptive variable names
- Add comments for complex logic
- Handle errors gracefully
- Log useful debugging information

### Prompt Engineering

When modifying agent prompts:

- Keep instructions clear and structured
- Use markdown formatting for readability
- Include output format examples
- Specify error handling behavior
- Test with edge cases (empty files, malformed VTT, etc.)

## Testing

### Manual Testing Checklist

- [ ] Single file analysis completes
- [ ] Batch processing works (3+ files)
- [ ] Synthesis generates combined-analysis.md
- [ ] Dashboard renders correctly
- [ ] Knowledge graph displays
- [ ] Dark mode works
- [ ] Search/filters function
- [ ] Quality review loop runs
- [ ] All coverage metrics accurate

### Sample Test Files

Use the examples in `/examples/` for testing:
- `example-lecture.vtt` - Standard lecture format
- `example-qa.vtt` - Heavy Q&A session
- `example-workshop.vtt` - Interactive workshop

## Pull Request Process

1. Update README.md if adding features
2. Add example files if relevant
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback promptly

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Credit others' contributions

## Questions?

Open a discussion or reach out to the maintainers.

---

Thank you for contributing! 🦐
