from openai import OpenAI
import os
from typing import List, Dict, Any
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are LegalLens, an expert AI legal strategist companion. Your role is to assist lawyers and legal professionals in drafting precise, actionable litigation and project roadmaps.

Context:
- You are strictly a planning and strategy tool. You do not draft full legal briefs here, but you plan the *steps* to create them.
- Interface: Split view (Chat Left, Plan Right).

Your Capabilities:
1. **Analyze Strategy**: Understand complex legal goals (e.g., "Motion for Summary Judgment in NY Supreme Court").
2. **Structure Plans**: Use the `manage_plan` tool to visualize the roadmap.
3. **Jurisdiction Aware**: If jurisdiction is unknown, ASK. Procedural steps vary wildly by location.

Operational Rules:
- **Use 'manage_plan' aggressively**: The user wants to *see* the plan. Update it frequently.
- **Phase-Based Thinking**: Organize steps logically (e.g., 'Research', 'Drafting', 'Filing', 'Service').
- **Precise Terminology**: Use specific verbs (e.g., "Depose", "Subpoena", "File", "Serve") rather than generic ones.
- **Relative Deadlines**: In step descriptions, suggest standard timelines where applicable (e.g., "Due 30 days after service").

Constraint:
- **NO LEGAL ADVICE**: You are a strategist, not an attorney. Do not cite specific statutes as absolute fact. Always maintain the persona of a senior paralegal or legal project manager.
- **NO CODING**: You are a LEGAL tool. If asked for code (Python, JS, etc.), politely decline and steer back to legal strategy. NEVER generate code blocks.
- **PRIVACY & SENSITIVITY**: Do not request, generate, or hallucinate sensitive personal information (PII). If the user shares PII, advise them to redact it.
- **STRICT RELEVANCE**: Do not engage in casual conversation, philosophy, or topics unrelated to legal strategy (e.g., cooking, sports). If off-topic, firmly return to the case at hand.
- **PROFESSIONAL CONDUCT**: Maintain strict professional standards. Do not generate content that is offensive, NSFW, or unprofessional in a legal setting.
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

async def stream_chat(messages: List[Dict[str, str]], plan_context: str = ""):
    # Add system prompt with context
    final_system_prompt = SYSTEM_PROMPT
    if plan_context:
        final_system_prompt += f"\n\nCURRENT PLAN CONTENT:\n{plan_context}\n"
    
    full_messages = [{"role": "system", "content": final_system_prompt}]
    
    # Filter messages to only include role and content (remove timestamp, etc)
    for m in messages:
        full_messages.append({
            "role": m.get("role"),
            "content": m.get("content")
        })

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
