#!/usr/bin/env python3
"""
Distill - Python CLI Runner

Distill conversations into intelligence.

Usage:
    python distill.py ./transcripts --output ./results
    python distill.py ./transcripts --config config.json
    python distill.py ./transcripts --extractors '[{"name": "Action Items", "pattern": "todo|action"}]'
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import anthropic
except ImportError:
    print("Error: anthropic package required. Install with: pip install anthropic")
    sys.exit(1)


# Load prompts from core/prompts/
SCRIPT_DIR = Path(__file__).parent
CORE_DIR = SCRIPT_DIR.parent.parent / "core"
PROMPTS_DIR = CORE_DIR / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_file = PROMPTS_DIR / f"{name}.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_file}")
    
    content = prompt_file.read_text()
    # Extract the prompt from the markdown (between ``` blocks)
    import re
    match = re.search(r'```\n(.*?)```', content, re.DOTALL)
    if match:
        return match.group(1)
    return content


def render_prompt(template: str, variables: dict) -> str:
    """Simple template rendering (replace {{var}} with values)."""
    result = template
    for key, value in variables.items():
        if isinstance(value, list):
            value = json.dumps(value)
        elif isinstance(value, dict):
            value = json.dumps(value)
        elif isinstance(value, bool):
            value = str(value).lower()
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


def list_transcript_files(input_dir: Path) -> list[dict]:
    """List all transcript files in the input directory."""
    files = []
    extensions = ['.vtt', '.srt', '.txt', '.json']
    
    for ext in extensions:
        for filepath in input_dir.glob(f"*{ext}"):
            stat = filepath.stat()
            files.append({
                "filename": filepath.name,
                "filepath": str(filepath),
                "format": ext[1:],  # Remove the dot
                "size_bytes": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    return files


def analyze_file(client: anthropic.Anthropic, file_info: dict, output_dir: Path, 
                 custom_extractors: list, file_index: int, total_files: int) -> dict:
    """Analyze a single transcript file."""
    try:
        filepath = Path(file_info["filepath"])
        content = filepath.read_text()
        
        output_path = output_dir / "summaries" / f"{filepath.stem}.md"
        
        # Build extractor instructions
        extractor_instructions = ""
        if custom_extractors:
            extractor_instructions = "\n\n## Custom Extractors (REQUIRED)\n"
            for i, ext in enumerate(custom_extractors):
                extractor_instructions += f"\n### {i+1}. {ext['name']}\n"
                if ext.get('pattern'):
                    extractor_instructions += f"- Pattern: {ext['pattern']}\n"
                if ext.get('instructions'):
                    extractor_instructions += f"- Instructions: {ext['instructions']}\n"
        
        prompt = f"""Analyze this transcript file and create a comprehensive summary.

## File Information
- Filename: {file_info['filename']}
- Format: {file_info['format']}
- Processing: File {file_index} of {total_files}

## Transcript Content
{content}

## Your Task
Create a comprehensive analysis including:
- Content type (meeting, lecture, podcast, interview, etc.)
- Participants and roles
- Questions and answers
- Key topics with summaries
- Action items and follow-ups
- Tools and resources mentioned
- Notable quotes and insights
- Summary (3-5 sentences)
{extractor_instructions}

Output the analysis in markdown format.
"""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = response.content[0].text
        
        # Save the analysis
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(analysis)
        
        return {
            "success": True,
            "filename": file_info["filename"],
            "output_path": str(output_path)
        }
        
    except Exception as e:
        return {
            "success": False,
            "filename": file_info["filename"],
            "error": str(e)
        }


def synthesize(client: anthropic.Anthropic, output_dir: Path, config: dict) -> str:
    """Synthesize across all analyzed files."""
    summaries_dir = output_dir / "summaries"
    summary_files = list(summaries_dir.glob("*.md"))
    
    # Read all summaries
    summaries_content = ""
    for f in summary_files:
        summaries_content += f"\n\n---\n## {f.stem}\n\n{f.read_text()}"
    
    custom_extractor_sections = ""
    if config.get("customExtractors"):
        custom_extractor_sections = "\n\nAlso aggregate custom extractor data:\n"
        for ext in config["customExtractors"]:
            custom_extractor_sections += f"- {ext['name']}\n"
    
    prompt = f"""Create a comprehensive synthesis of these {len(summary_files)} analyzed transcripts.

## Project: {config.get('projectName', 'Transcript Analysis')}

## Individual Summaries
{summaries_content}

## Create combined-analysis.md with:
1. Executive Summary (5-7 key takeaways)
2. Question Frequency Analysis (table)
3. Topic Heatmap Data (coverage matrix)
4. Cross-Session Insights
5. Tools & Resources Compendium
6. Investigation Priorities
7. Recommended Review Order
8. Master Q&A Index
9. Session Quick Reference
{custom_extractor_sections}

Output the complete synthesis in markdown format.
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    synthesis = response.content[0].text
    
    # Save synthesis
    output_path = output_dir / "combined-analysis.md"
    output_path.write_text(synthesis)
    
    return synthesis


def generate_json_export(client: anthropic.Anthropic, output_dir: Path, config: dict) -> dict:
    """Generate structured JSON export."""
    analysis_path = output_dir / "combined-analysis.md"
    analysis = analysis_path.read_text()
    
    prompt = f"""Convert this analysis to structured JSON.

## Analysis
{analysis}

## Output JSON structure:
{{
  "metadata": {{"projectName": "{config.get('projectName', 'Analysis')}", "generatedAt": "{datetime.now().isoformat()}"}},
  "summary": {{"totalSessions": N, "totalQuestions": N, "keyTakeaways": [...]}},
  "sessions": [...],
  "questions": [...],
  "topics": [...],
  "tools": [...],
  "heatmap": {{"topics": [...], "sessions": [...], "data": [[...]]}},
  "customExtractors": {{...}}
}}

Output ONLY valid JSON, no other text.
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    json_text = response.content[0].text
    
    # Try to parse and save
    try:
        # Extract JSON from response if wrapped in markdown
        import re
        match = re.search(r'\{[\s\S]*\}', json_text)
        if match:
            json_text = match.group(0)
        
        data = json.loads(json_text)
        output_path = output_dir / "analysis-data.json"
        output_path.write_text(json.dumps(data, indent=2))
        return data
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse JSON output: {e}")
        # Save raw output anyway
        output_path = output_dir / "analysis-data.json"
        output_path.write_text(json_text)
        return {}


def generate_dashboard(client: anthropic.Anthropic, output_dir: Path, config: dict) -> str:
    """Generate HTML dashboard."""
    analysis_path = output_dir / "combined-analysis.md"
    analysis = analysis_path.read_text()
    
    json_path = output_dir / "analysis-data.json"
    json_data = json_path.read_text() if json_path.exists() else "{}"
    
    styling = config.get("styling", {})
    
    prompt = f"""Create an interactive HTML dashboard from this analysis.

## Analysis
{analysis}

## JSON Data
{json_data}

## Branding
- Title: {config.get('dashboardTitle', 'Transcript Analysis Dashboard')}
- Primary Color: {styling.get('primaryColor', '#2563eb')}
- Secondary Color: {styling.get('secondaryColor', '#7c3aed')}
- Accent Color: {styling.get('accentColor', '#f59e0b')}

## Styling Instructions
{styling.get('stylingInstructions', 'Clean, professional design')}

## Requirements
- Single self-contained HTML file
- All CSS/JS inline (except D3.js CDN)
- Mobile responsive
- Dark/light mode toggle
- Search/filter functionality
- Knowledge graph visualization
- Pagination for large lists

Output the complete HTML file.
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=32000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    html = response.content[0].text
    
    # Extract HTML if wrapped in markdown
    import re
    match = re.search(r'<!DOCTYPE.*</html>', html, re.DOTALL | re.IGNORECASE)
    if match:
        html = match.group(0)
    
    output_path = output_dir / "dashboard.html"
    output_path.write_text(html)
    
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Distill - Transform conversations into intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python distill.py ./transcripts
  python distill.py ./transcripts --output ./results
  python distill.py ./transcripts --format both
  python distill.py ./transcripts --extractors '[{"name": "Action Items", "pattern": "todo"}]'
        """
    )
    
    parser.add_argument("input_dir", type=Path, help="Directory containing transcript files")
    parser.add_argument("--output", "-o", type=Path, default=Path("./distill-output"),
                        help="Output directory (default: ./distill-output)")
    parser.add_argument("--config", "-c", type=Path, help="Path to config JSON file")
    parser.add_argument("--format", "-f", choices=["html", "json", "both"], default="both",
                        help="Output format (default: both)")
    parser.add_argument("--extractors", "-e", type=str,
                        help="Custom extractors as JSON array")
    parser.add_argument("--project-name", "-n", type=str, default="Transcript Analysis",
                        help="Project name")
    parser.add_argument("--parallel", "-p", type=int, default=3,
                        help="Number of parallel file processors (default: 3)")
    parser.add_argument("--skip-dashboard", action="store_true",
                        help="Skip dashboard generation")
    
    args = parser.parse_args()
    
    # Load config
    config = {}
    if args.config and args.config.exists():
        config = json.loads(args.config.read_text())
    
    # Override with CLI args
    config["projectName"] = args.project_name
    config["outputFormat"] = args.format
    
    if args.extractors:
        config["customExtractors"] = json.loads(args.extractors)
    
    # Validate input
    if not args.input_dir.exists():
        print(f"Error: Input directory not found: {args.input_dir}")
        sys.exit(1)
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Initialize client
    client = anthropic.Anthropic()
    
    # List files
    print(f"Scanning {args.input_dir} for transcript files...")
    files = list_transcript_files(args.input_dir)
    print(f"Found {len(files)} transcript files")
    
    if not files:
        print("No transcript files found. Supported formats: .vtt, .srt, .txt, .json")
        sys.exit(1)
    
    # Analyze files
    print(f"\nAnalyzing files (parallelism: {args.parallel})...")
    results = []
    
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = {
            executor.submit(
                analyze_file, client, f, args.output,
                config.get("customExtractors", []),
                i + 1, len(files)
            ): f for i, f in enumerate(files)
        }
        
        for future in as_completed(futures):
            result = future.result()
            status = "✓" if result["success"] else "✗"
            print(f"  {status} {result['filename']}")
            results.append(result)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\nAnalysis complete: {len(successful)} succeeded, {len(failed)} failed")
    
    if not successful:
        print("No files were successfully analyzed.")
        sys.exit(1)
    
    # Synthesize
    print("\nSynthesizing across all sessions...")
    synthesize(client, args.output, config)
    print(f"  ✓ combined-analysis.md")
    
    # Generate outputs
    if args.format in ["json", "both"]:
        print("\nGenerating JSON export...")
        generate_json_export(client, args.output, config)
        print(f"  ✓ analysis-data.json")
    
    if args.format in ["html", "both"] and not args.skip_dashboard:
        print("\nGenerating dashboard...")
        generate_dashboard(client, args.output, config)
        print(f"  ✓ dashboard.html")
    
    # Summary
    print(f"\n{'='*50}")
    print("Distillation complete!")
    print(f"{'='*50}")
    print(f"Output directory: {args.output}")
    print(f"Files processed: {len(successful)}/{len(files)}")
    print(f"\nGenerated files:")
    print(f"  - {args.output}/summaries/*.md (individual analyses)")
    print(f"  - {args.output}/combined-analysis.md")
    if args.format in ["json", "both"]:
        print(f"  - {args.output}/analysis-data.json")
    if args.format in ["html", "both"] and not args.skip_dashboard:
        print(f"  - {args.output}/dashboard.html")


if __name__ == "__main__":
    main()
