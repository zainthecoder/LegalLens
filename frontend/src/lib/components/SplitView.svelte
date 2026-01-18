<script>
  export let left = null; // Component or snippet
  export let right = null;

  let className = "";
  export { className as class };
</script>

<div
  class="flex flex-col lg:flex-row h-full w-full overflow-hidden bg-background {className}"
>
  <!-- Left Pane: Chat -->
  <div
    class="w-full lg:w-[400px] xl:w-[450px] flex-shrink-0 border-r border-border bg-card/50 backdrop-blur-sm z-10 flex flex-col h-[50vh] lg:h-full print:hidden"
  >
    <slot name="left" />
  </div>

  <!-- Right Pane: Plan -->
  <div
    class="flex-1 flex flex-col h-[50vh] lg:h-full relative overflow-hidden bg-background print:overflow-visible print:h-auto print:block"
  >
    <slot name="right" />
  </div>
</div>
