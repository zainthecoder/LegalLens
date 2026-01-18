from openai import OpenAI
import os
from typing import List, Dict, Any
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are LegalLens, an advanced AI legal project assistant designed to help lawyers and legal professionals structure complex legal goals.

Your interface features a split view:
- **Left Pane:** Chat interface for discussion.
- **Right Pane:** A live, structured 'Plan' document.

You have access to a tool called `manage_plan`. You MUST use this tool whenever the user asks to create, modify, or refine the legal strategy.
- When you use the tool, the Right Pane updates immediately.
- Always explain what you are changing in the chat.
- Be precise, professional, and use legal terminology where appropriate.

Rules:
1. Start by asking for a goal if none is provided.
2. Break down goals into actionable steps.
3. Use the `manage_plan` tool to visualize the plan.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "manage_plan",
            "description": "Create or update the legal plan displayed in the right pane.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the legal plan (e.g., 'Motion to Dismiss Strategy')."
                    },
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "Unique ID for the step"},
                                "title": {"type": "string", "description": "Actionable step title"},
                                "description": {"type": "string", "description": "Detailed description"},
                                "status": {"type": "string", "enum": ["pending", "in-progress", "done"]}
                            },
                            "required": ["id", "title", "status"]
                        }
                    }
                },
                "required": ["title", "steps"]
            }
        }
    }
]

async def stream_chat(messages: List[Dict[str, str]]):
    # Add system prompt
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages,
        tools=TOOLS,
        stream=True
    )

    for chunk in response:
        delta = chunk.choices[0].delta
        
        # Check for tool calls
        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                # We yield a special marker for tool calls to handle locally or on frontend
                # For MVP, we might just buffer the tool call arguments and yield correctly
                # But to keep it simple, we'll try to reconstruct the tool call.
                # However, streaming tool calls is tricky. 
                # Let's yield partial JSON or a custom event format.
                if tool_call.function.arguments:
                     yield json.dumps({"type": "tool_chunk", "content": tool_call.function.arguments}) + "\n"
        
        elif delta.content:
            yield json.dumps({"type": "text", "content": delta.content}) + "\n"
