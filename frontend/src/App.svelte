<script>
  import Navbar from "./lib/components/Navbar.svelte";
  import SplitView from "./lib/components/SplitView.svelte";
  import ChatInterface from "./lib/components/ChatInterface.svelte";
  import PlanViewer from "./lib/components/PlanViewer.svelte";
</script>

<main
  class="flex flex-col h-screen overflow-hidden bg-background text-foreground font-sans antialiased print:h-auto print:overflow-visible"
>
  <Navbar />
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
</main>
