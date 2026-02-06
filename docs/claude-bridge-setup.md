# Claude Bridge Setup Guide

The Distill workflow requires a "Claude Bridge" - an HTTP service that provides Claude with computer use capabilities (file system access, bash commands).

## What is Claude Bridge?

Claude Bridge is an intermediary service that:

1. Accepts HTTP POST requests with prompts
2. Forwards them to Claude's API with computer use tools enabled
3. Executes tool calls (file read/write, bash commands)
4. Returns Claude's final response

```
┌─────────┐     HTTP POST      ┌──────────────┐     API      ┌─────────┐
│   n8n   │ ─────────────────▶ │ Claude Bridge│ ────────────▶│ Claude  │
│Workflow │ ◀───────────────── │   Service    │ ◀────────────│   API   │
└─────────┘     JSON Response  └──────────────┘              └─────────┘
                                      │
                                      │ Tool Execution
                                      ▼
                               ┌──────────────┐
                               │ File System  │
                               │ /transcripts │
                               └──────────────┘
```

## Option 1: Anthropic Computer Use Demo

Anthropic provides a reference implementation for computer use:

```bash
# Clone the repo
git clone https://github.com/anthropics/anthropic-quickstarts
cd anthropic-quickstarts/computer-use-demo

# Build and run with Docker
docker build -t claude-computer-use .
docker run -d \
  --name claude-bridge \
  -p 3456:8080 \
  -v /path/to/transcripts:/transcripts \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  claude-computer-use
```

You may need to adapt the API endpoint to match the expected format.

## Option 2: Custom Implementation

Create a minimal bridge service that:

### Expected Request Format

```json
POST /claude
Content-Type: application/json

{
  "prompt": "Your instruction for Claude",
  "maxTurns": 15,
  "workingDir": "/transcripts"
}
```

### Expected Response Format

```json
{
  "result": "Claude's final text response after tool execution"
}
```

### Required Capabilities

The bridge must provide Claude with these tools:

1. **File Read** - Read contents of files
2. **File Write** - Create/overwrite files
3. **Bash Execution** - Run shell commands
4. **Directory Listing** - List files in directories

### Example Python Implementation

```python
from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route('/claude', methods=['POST'])
def claude():
    data = request.json
    prompt = data.get('prompt')
    max_turns = data.get('maxTurns', 15)
    working_dir = data.get('workingDir', '/transcripts')
    
    # Create messages with computer use tools
    messages = [{"role": "user", "content": prompt}]
    
    tools = [
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
        },
        {
            "type": "bash_20241022",
            "name": "bash",
        },
        {
            "type": "text_editor_20241022",
            "name": "str_replace_editor",
        }
    ]
    
    final_response = ""
    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        # Handle tool use
        if response.stop_reason == "tool_use":
            # Execute tools and continue conversation
            tool_results = execute_tools(response.content, working_dir)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Extract final text response
            final_response = extract_text(response.content)
            break
    
    return jsonify({"result": final_response})

def execute_tools(content, working_dir):
    # Implement tool execution logic
    # Return tool results in the expected format
    pass

def extract_text(content):
    # Extract text blocks from response
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3456)
```

## Option 3: OpenClaw Integration

If you're running [OpenClaw](https://github.com/openclaw/openclaw), it includes a claude-bridge component:

```bash
# The bridge is available at http://localhost:3456/claude
# when running OpenClaw with computer use enabled
```

## Docker Networking

When running n8n and Claude Bridge in Docker:

```yaml
# docker-compose.yml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    networks:
      - ai-network
    volumes:
      - ./transcripts:/transcripts

  claude-bridge:
    build: ./claude-bridge
    ports:
      - "3456:3456"
    networks:
      - ai-network
    volumes:
      - ./transcripts:/transcripts
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

networks:
  ai-network:
    driver: bridge
```

With this setup, n8n can reach the bridge at `http://claude-bridge:3456/claude`.

## Testing Your Bridge

```bash
# Test the bridge is responding
curl -X POST http://localhost:3456/claude \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "List files in /transcripts and return the count",
    "maxTurns": 5,
    "workingDir": "/transcripts"
  }'
```

Expected response:
```json
{
  "result": "Found 3 files in /transcripts: file1.vtt, file2.vtt, file3.vtt"
}
```

## Troubleshooting

### Bridge Not Responding
- Check the service is running: `docker ps`
- Check logs: `docker logs claude-bridge`
- Verify port mapping: `curl localhost:3456`

### Claude API Errors
- Verify ANTHROPIC_API_KEY is set
- Check API key has computer use access
- Monitor rate limits

### File Access Issues
- Verify volume mounts are correct
- Check file permissions
- Ensure working_dir exists

### Timeout Errors
- Increase timeout in n8n HTTP Request nodes
- Consider breaking large prompts into smaller tasks
- Monitor Claude API latency
