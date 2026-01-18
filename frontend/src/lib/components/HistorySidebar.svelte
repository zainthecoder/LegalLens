<script>
  import { onMount } from "svelte";
  import { auth } from "../stores/auth";
  import { plan } from "../stores/plan";

  export let isOpen = false;

  let plans = [];
  let loading = false;

  async function loadPlans() {
    if (!$auth.token) return;
    loading = true;
    try {
      const res = await fetch("http://localhost:8000/api/plans", {
        headers: { Authorization: `Bearer ${$auth.token}` },
      });
      if (res.ok) {
        plans = await res.json();
      }
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function selectPlan(planId) {
    if (!$auth.token) return;
    try {
      const res = await fetch(`http://localhost:8000/api/plans/${planId}`, {
        headers: { Authorization: `Bearer ${$auth.token}` },
      });
      if (res.ok) {
        const data = await res.json();
        // Update plan store
        plan.set(data.plan);
        // We also need to reload chat messages.
        // For MVP, we might need a way to tell ChatInterface to reload.
        // Or we can expose a store for 'currentChatHistory'
        // For now, let's dispatch a custom event or use a store if feasible.
        // Actually, simplest is to reload window or use a specific store for "activeSession"
        // Let's reload page with ?planId=... or just update global state.
        // Better: Use a store for 'messages' in chat.
        // We will dispatch an event to window for now to keep it decoupled
        window.dispatchEvent(new CustomEvent("load-session", { detail: data }));
        isOpen = false; // Close sidebar on selection on mobile
      }
    } catch (e) {
      console.error(e);
    }
  }

  // Reload plans when sidebar opens
  $: if (isOpen && $auth.isAuthenticated) {
    loadPlans();
  }
</script>

{#if isOpen}
  <div
    class="fixed inset-y-0 left-0 w-64 bg-card border-r border-border shadow-lg z-50 transform transition-transform duration-200 ease-in-out p-4 flex flex-col"
  >
    <div class="flex items-center justify-between mb-6">
      <h2 class="font-playfair text-lg font-semibold text-foreground">
        My Strategies
      </h2>
      <button
        on:click={() => (isOpen = false)}
        class="text-muted-foreground hover:text-foreground"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          ><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg
        >
      </button>
    </div>

    {#if loading}
      <div class="text-sm text-muted-foreground">Loading...</div>
    {:else if plans.length === 0}
      <div class="text-sm text-muted-foreground">No saved strategies yet.</div>
    {:else}
      <div class="flex-1 overflow-y-auto space-y-2">
        {#each plans as p}
          <button
            on:click={() => selectPlan(p.id || p._id)}
            class="w-full text-left p-3 rounded-lg hover:bg-muted transition-colors border border-transparent hover:border-border group"
          >
            <div
              class="font-medium text-sm text-foreground group-hover:text-primary truncate"
            >
              {p.title}
            </div>
            <div class="text-xs text-muted-foreground">
              {new Date(p.updated_at).toLocaleDateString()}
            </div>
          </button>
        {/each}
      </div>
    {/if}

    <div class="mt-4 pt-4 border-t border-border">
      <div class="text-xs text-muted-foreground text-center">
        LegalLens v0.1
      </div>
    </div>
  </div>

  <!-- Overlay -->
  <div
    class="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
    on:click={() => (isOpen = false)}
  ></div>
{/if}
