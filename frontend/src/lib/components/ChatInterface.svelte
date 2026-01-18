<script>
  import Button from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import { plan } from "../stores/plan.js";
  import { auth } from "../stores/auth.js";
  import { get } from "svelte/store";

  let messages = [];
  let input = "";
  let isLoading = false;

  async function handleSubmit() {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user", content: input };
    messages = [...messages, userMessage];
    const messageInput = input;
    input = "";
    isLoading = true;

    try {
      const token = get(auth).token;
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ messages: messages }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = { role: "assistant", content: "" };
      let toolArgsBuffer = "";

      // Speculatively add assistant message to UI
      messages = [...messages, assistantMessage];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            if (data.type === "text") {
              // Update the last message content
              assistantMessage.content += data.content;
              messages = [...messages.slice(0, -1), assistantMessage];
            } else if (data.type === "tool_chunk") {
              // Accumulate tool arguments
              toolArgsBuffer += data.content;
            }
          } catch (e) {
            console.error("Error parsing stream", e);
          }
        }
      }

      // Attempt to update plan if we received tool args
      if (toolArgsBuffer.trim()) {
        try {
          const planData = JSON.parse(toolArgsBuffer);
          console.log("Updating plan with:", planData);
          plan.set(planData);

          // Optional: Add a system message saying plan was updated
          // messages = [...messages, { role: 'system', content: 'Plan updated.' }];
        } catch (e) {
          console.error("Error parsing final tool args:", e);
          console.error("Buffer was:", toolArgsBuffer);
        }
      }

      // Re-fetch plan if tool was called?
      // Or in this MVP, let's assume the LLM includes the plan in the text or
      // we handle tool execution on client?
      // The architecture plan said "Backend calls tool".
      // But my backend implementation `stream_chat` yields tool chunks.
      // Let's update backend to execute tool
      // OR implement parsing here.
      // Parsing streaming tool calls in custom code is hard.
      // Let's stick to text chat for Step 1 verification,
      // THEN fixing tool execution if needed.
    } catch (error) {
      console.error("Error:", error);
      messages = [
        ...messages,
        { role: "system", content: "Error connecting to server." },
      ];
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="flex flex-col h-full bg-muted/10 relative">
  <!-- Header -->
  <div
    class="px-4 py-3 border-b border-border bg-card/50 backdrop-blur flex items-center justify-between sticky top-0 z-10"
  >
    <h2 class="font-semibold text-sm text-foreground truncate max-w-[70%]">
      {$plan?.title || "New Strategy"}
    </h2>
    <span class="text-xs text-muted-foreground">Session Active</span>
  </div>

  <div class="flex-1 p-4 overflow-y-auto space-y-4">
    {#if messages.length === 0}
      <div
        class="bg-card p-4 rounded-lg border border-border max-w-[90%] text-sm shadow-sm"
      >
        <h3 class="font-semibold mb-1 text-primary">LegalLens Assistant</h3>
        <p class="text-muted-foreground">
          Hello! I am your AI Legal Project Assistant. I can help you structure
          complex legal tasks. Try saying: <span
            class="text-foreground font-medium"
            >"Help me plan a Motion for Summary Judgment."</span
          >
        </p>
      </div>
    {/if}

    {#each messages as m}
      <div
        class="flex flex-col max-w-[85%] text-sm mb-4 {m.role === 'user'
          ? 'self-end items-end'
          : 'self-start items-start'}"
      >
        <div
          class="p-3 rounded-lg shadow-sm whitespace-pre-wrap {m.role === 'user'
            ? 'bg-primary text-primary-foreground rounded-tr-none'
            : 'bg-card text-card-foreground border border-border rounded-tl-none'}"
        >
          <div
            class="font-semibold text-xs mb-1 opacity-90 flex justify-between gap-4"
          >
            <span>{m.role === "user" ? "You" : "LegalLens"}</span>
            {#if m.timestamp}
              <span class="font-normal opacity-70 text-[10px]"
                >{new Date(m.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}</span
              >
            {/if}
          </div>
          {m.content}
        </div>
      </div>
    {/each}

    {#if isLoading}
      <div
        class="self-start bg-card text-card-foreground p-3 rounded-lg rounded-tl-none border border-border text-sm flex items-center gap-2"
      >
        <div class="w-2 h-2 bg-primary/50 rounded-full animate-bounce"></div>
        <div
          class="w-2 h-2 bg-primary/50 rounded-full animate-bounce [animation-delay:0.2s]"
        ></div>
        <div
          class="w-2 h-2 bg-primary/50 rounded-full animate-bounce [animation-delay:0.4s]"
        ></div>
      </div>
    {/if}
  </div>

  <div class="p-4 border-t border-border bg-background">
    <form on:submit|preventDefault={handleSubmit} class="flex gap-2">
      <Input
        bind:value={input}
        placeholder="Type your legal goal here..."
        className="flex-1"
        disabled={isLoading}
      />
      <Button type="submit" disabled={isLoading} className="font-semibold"
        >Send</Button
      >
    </form>
  </div>
</div>
