<script>
  import { onMount } from "svelte";
  import { auth } from "./lib/stores/auth.js";
  import Navbar from "./lib/components/Navbar.svelte";
  import SplitView from "./lib/components/SplitView.svelte";
  import ChatInterface from "./lib/components/ChatInterface.svelte";
  import PlanViewer from "./lib/components/PlanViewer.svelte";
  import Login from "./lib/components/Login.svelte";
  import HistorySidebar from "./lib/components/HistorySidebar.svelte";

  let isSidebarOpen = false;

  onMount(() => {
    auth.init();
  });
</script>

<main
  class="flex flex-col h-screen overflow-hidden bg-background text-foreground font-sans antialiased print:h-auto print:overflow-visible"
>
  {#if $auth.isLoading}
    <div class="flex items-center justify-center h-full">
      <div
        class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
      ></div>
    </div>
  {:else if !$auth.isAuthenticated}
    <div class="h-full w-full">
      <Login />
    </div>
  {:else}
    <HistorySidebar bind:isOpen={isSidebarOpen} />
    <Navbar on:toggleSidebar={() => (isSidebarOpen = !isSidebarOpen)} />
    <div class="flex-1 overflow-hidden">
      <SplitView>
        <div slot="left" class="h-full">
          <ChatInterface />
        </div>
        <div slot="right" class="h-full">
          <PlanViewer />
        </div>
      </SplitView>
    </div>
  {/if}
</main>
