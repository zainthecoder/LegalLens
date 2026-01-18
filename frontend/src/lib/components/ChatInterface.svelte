<script>
  import Button from "../ui/Button.svelte";
  import Input from "../ui/Input.svelte";
  import { plan } from "../stores/plan.js";
  import { auth } from "../stores/auth.js";
  import { get } from "svelte/store";
  import { onMount, onDestroy } from "svelte";

  let messages = [];
  let input = "";
  let isLoading = false;
  let planId = null;

  function handleLoadSession(event) {
    const data = event.detail;
    planId = data.plan._id;
    messages = data.chat_history || [];
    // Scroll to bottom?
  }

  function handleResetSession() {
    planId = null;
    messages = [];
    plan.set({ title: "", steps: [] });
  }

  onMount(() => {
    window.addEventListener("load-session", handleLoadSession);
    window.addEventListener("reset-session", handleResetSession);
  });

  onDestroy(() => {
    if (typeof window !== "undefined") {
      window.removeEventListener("load-session", handleLoadSession);
      window.removeEventListener("reset-session", handleResetSession);
    }
  });

  async function handleSubmit() {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };
    messages = [...messages, userMessage];
    const messageInput = input;
    input = "";
    isLoading = true;

    try {
      const token = get(auth).token;

      const payload = { messages: messages };
      if (planId) {
        payload.plan_id = planId;
      }

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = {
        role: "assistant",
        content: "",
        timestamp: new Date().toISOString(),
      };
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
            if (data.type === "meta") {
              // Capture plan ID from new session
              if (!planId) {
                planId = data.plan_id;
                console.log("Set active plan ID:", planId);
                // Also update URL without reload?
                // navigate(`?plan=${planId}`) // Maybe later
              }
            } else if (data.type === "text") {
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
      // Attempt to update plan if we received tool args
      if (toolArgsBuffer.trim()) {
        try {
          const planData = JSON.parse(toolArgsBuffer);
          console.log("Updating plan with:", planData);

          plan.update((p) => ({
            ...p,
            ...planData,
            updatedAt: new Date().toISOString(),
          }));

          // If no text response, add a placeholder
          if (!assistantMessage.content.trim()) {
            assistantMessage.content =
              "I've updated the strategy plan based on your request.";
            messages = [...messages.slice(0, -1), assistantMessage];
          }
        } catch (e) {
          console.error("Error parsing final tool args:", e);
        }
      } else if (!assistantMessage.content.trim()) {
        // No text and no tool args?
        assistantMessage.content = "(No response received)";
        messages = [...messages.slice(0, -1), assistantMessage];
      }
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
