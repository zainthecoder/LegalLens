<script>
  import { createEventDispatcher } from "svelte";
  import { auth } from "../stores/auth";
  import { plan } from "../stores/plan";

  const dispatch = createEventDispatcher();

  function handleLogout() {
    auth.logout();
  }
</script>

<nav
  class="flex items-center justify-between px-6 py-3 border-b border-border bg-card print:hidden"
>
  <div class="flex items-center gap-4">
    <!-- Menu Button -->
    <button
      on:click={() => dispatch("toggleSidebar")}
      class="p-2 -ml-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        ><line x1="4" x2="20" y1="12" y2="12" /><line
          x1="4"
          x2="20"
          y1="6"
          y2="6"
        /><line x1="4" x2="20" y1="18" y2="18" /></svg
      >
    </button>

    <div class="flex items-center gap-2">
      <div class="p-2 bg-primary/10 rounded-md">
        <!-- Scale Icon -->
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="text-primary"
          ><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z" /><path
            d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"
          /><path d="M7 21h10" /><path d="M12 3v18" /><path
            d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"
          /></svg
        >
      </div>
      <h1 class="font-playfair text-xl font-semibold text-foreground mr-6">
        LegalLens
      </h1>

      <!-- New Strategy Button -->
      <button
        on:click={() => {
          window.dispatchEvent(new CustomEvent("reset-session"));
        }}
        class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-primary bg-primary/5 hover:bg-primary/10 border border-primary/20 rounded-full transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          ><path d="M5 12h14" /><path d="M12 5v14" /></svg
        >
        New Strategy
      </button>
    </div>
  </div>

  <div class="flex items-center gap-4">
    <div class="text-sm text-muted-foreground hidden md:block">
      Case: <span class="text-foreground font-medium"
        >{$plan?.title || "New Strategy"}</span
      >
    </div>

    <div class="flex items-center gap-3">
      <div
        class="w-8 h-8 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center text-xs font-serif text-primary"
      >
        {$auth.user?.email?.[0].toUpperCase() || "U"}
      </div>

      <button
        on:click={handleLogout}
        class="text-sm text-muted-foreground hover:text-destructive transition-colors flex items-center gap-1"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          ><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline
            points="16 17 21 12 16 7"
          /><line x1="21" x2="9" y1="12" y2="12" /></svg
        >
        <span class="hidden sm:inline">Logout</span>
      </button>
    </div>
  </div>
</nav>
