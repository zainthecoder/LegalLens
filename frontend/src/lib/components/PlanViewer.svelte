<script>
  import { plan } from "../stores/plan.js";
  import Card from "../ui/Card.svelte";

  // Subscribe to store
  let currentPlan;
  plan.subscribe((value) => {
    currentPlan = value;
  });

  function handleExport() {
    if (!currentPlan) return;

    // Store original title
    const originalTitle = document.title;

    // Set title to Plan Title (sanitized) for the PDF filename
    if (currentPlan.title) {
      document.title = currentPlan.title;
    }

    // Print
    window.print();

    // Restore original title after a short delay to ensure print dialog caught it
    // Note: window.print() blocks execution in many browsers until dialog closes,
    // but a small timeout is safer for non-blocking implementations.
    setTimeout(() => {
      document.title = originalTitle;
    }, 100);
  }
</script>

<div
  id="tour-plan"
  class="h-full flex flex-col bg-slate-50/50 dark:bg-slate-950/20 print:bg-white"
>
  <!-- Toolbar - Hide on print -->
  <div
    class="h-16 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-8 flex items-center justify-between flex-shrink-0 z-10 print:hidden"
  >
    <h2 class="font-semibold text-lg flex items-center gap-2">
      <span class="text-primary text-xl">📄</span>
      <span
        class="bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent"
        >Strategy Plan</span
      >
    </h2>
    <div class="flex gap-3">
      <button
        on:click={handleExport}
        class="text-xs font-medium px-3 py-1.5 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
      >
        Export PDF
      </button>
    </div>
  </div>

  <!-- Scrollable Content -->
  <div
    class="flex-1 overflow-y-auto p-6 md:p-10 print:overflow-visible print:h-auto print:block"
  >
    <div class="max-w-3xl mx-auto">
      {#if !currentPlan || !currentPlan.title}
        <div
          class="min-h-[60vh] flex flex-col items-center justify-center text-muted-foreground space-y-6"
        >
          <div
            class="w-16 h-16 rounded-2xl bg-muted flex items-center justify-center animate-pulse"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="opacity-50"
              ><path
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              /><polyline points="14 2 14 8 20 8" /><line
                x1="16"
                y1="13"
                x2="8"
                y2="13"
              /><line x1="16" y1="17" x2="8" y2="17" /><polyline
                points="10 9 9 9 8 9"
              /></svg
            >
          </div>
          <div class="text-center space-y-2">
            <div class="font-serif text-2xl text-foreground">
              Awaiting Strategy
            </div>
            <p class="text-sm max-w-[280px] leading-relaxed">
              Describe your legal goal to begin structuring a comprehensive
              action plan.
            </p>
          </div>
        </div>
      {:else}
        <!-- Document Container -->
        <div
          class="bg-card text-card-foreground rounded-xl shadow-sm border border-border/50 p-8 md:p-12 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500"
        >
          <!-- Header Section -->
          <div class="space-y-4 border-b border-border pb-8">
            <div class="flex items-center justify-between">
              <div
                class="text-[10px] font-bold tracking-[0.2em] text-primary uppercase border border-primary/20 px-2 py-0.5 rounded-sm inline-block"
              >
                Legal Strategy
              </div>
            </div>

            <h1
              class="text-3xl md:text-5xl font-serif font-bold text-foreground leading-tight tracking-tight"
            >
              {currentPlan.title}
            </h1>

            <div
              class="flex items-center gap-4 text-xs text-muted-foreground pt-2"
            >
              <span class="flex items-center gap-1.5">
                <svg
                  class="w-3.5 h-3.5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  ><circle cx="12" cy="12" r="10" /><polyline
                    points="12 6 12 12 16 14"
                  /></svg
                >
                Last updated: {new Date(
                  currentPlan.updatedAt || new Date(),
                ).toLocaleTimeString()}
              </span>
              <span class="w-1 h-1 rounded-full bg-border"></span>
              <span>{currentPlan.steps.length} Steps</span>
            </div>
          </div>

          <!-- Steps Section -->
          <div class="space-y-0.5 relative">
            <!-- Connecting Line (Optional approach, removing for cleaner card look, or keeping subtle) -->
            <div
              class="absolute left-[19px] top-6 bottom-6 w-px bg-border/60 -z-10 hidden md:block"
            ></div>

            {#each currentPlan.steps as step, i (step.id)}
              <div class="group relative flex gap-4 md:gap-6 py-4">
                <!-- Checkbox/Number -->
                <button
                  class="mt-1 w-10 h-10 flex-shrink-0 rounded-full border-2 bg-background z-10 flex items-center justify-center transition-all duration-300
                        {step.status === 'done'
                    ? 'border-primary bg-primary text-primary-foreground scale-95'
                    : step.status === 'in-progress'
                      ? 'border-blue-500 text-blue-500 ring-4 ring-blue-500/10'
                      : 'border-muted text-muted-foreground group-hover:border-primary/50'}"
                >
                  {#if step.status === "done"}
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2.5"
                      ><polyline points="20 6 9 17 4 12" /></svg
                    >
                  {:else}
                    <span class="font-mono text-sm font-semibold">{i + 1}</span>
                  {/if}
                </button>

                <!-- Content Card -->
                <div
                  class="flex-1 -mt-1 p-5 rounded-lg border border-transparent transition-all duration-200
                        {step.status === 'in-progress'
                    ? 'bg-blue-50/50 dark:bg-blue-950/10 border-blue-100 dark:border-blue-800'
                    : 'hover:bg-muted/30 hover:border-border/50'}"
                >
                  <div class="flex items-start justify-between gap-4 mb-2">
                    <h3
                      class="text-lg font-semibold tracking-tight {step.status ===
                      'done'
                        ? 'text-muted-foreground line-through decoration-border'
                        : 'text-foreground'}"
                    >
                      {step.title}
                    </h3>
                  </div>

                  {#if step.description}
                    <p
                      class="text-sm text-muted-foreground leading-relaxed {step.status ===
                      'done'
                        ? 'line-through opacity-70'
                        : ''}"
                    >
                      {step.description}
                    </p>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
