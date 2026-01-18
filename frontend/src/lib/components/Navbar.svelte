<script>
  // Icons are trickier in Svelte without a library like lucide-svelte.
  // We can use SVG directly for MVP.
</script>

<nav
  class="flex items-center justify-between px-6 py-3 border-b border-border bg-card print:hidden"
>
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
    <h1 class="font-playfair text-xl font-semibold text-foreground">
      LegalLens
    </h1>
  </div>
  <div class="flex items-center gap-4">
    <div class="text-sm text-muted-foreground hidden md:block">
      Case: <span class="text-foreground font-medium">New Strategy</span>
    </div>
    <div
      class="w-8 h-8 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center text-xs font-serif text-primary"
    >
      JD
    </div>
  </div>
</nav>
