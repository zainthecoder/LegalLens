<script>
  import { plan } from '../stores/plan.js';
  import Card from '../ui/Card.svelte';
  
  // Subscribe to store
  let currentPlan;
  plan.subscribe(value => {
    currentPlan = value;
  });
</script>

<div class="h-full flex flex-col bg-slate-50 dark:bg-slate-950/50">
  <!-- Toolbar -->
  <div class="h-14 border-b border-border bg-card/50 px-6 flex items-center justify-between flex-shrink-0">
    <h2 class="font-semibold text-lg flex items-center gap-2">
      <span class="text-primary text-xl">📄</span>
      Legal Strategy Plan
    </h2>
    <div class="flex gap-2">
      <button class="text-xs text-muted-foreground hover:text-primary transition-colors">Export PDF</button>
    </div>
  </div>

  <!-- Scrollable Content -->
  <div class="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
    {#if !currentPlan || !currentPlan.title}
      <div class="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50 space-y-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <div class="font-serif text-xl italic">Waiting for Mission</div>
        <p class="text-sm max-w-xs text-center">I am ready to structure your legal strategy. Tell me what you need to achieve.</p>
      </div>
    {:else}
      <!-- Header -->
      <div class="space-y-2">
        <div class="text-xs font-semibold tracking-wider text-primary uppercase">Strategy Document</div>
        <h1 class="text-3xl md:text-4xl font-serif font-bold text-foreground">{currentPlan.title}</h1>
        <div class="text-xs text-muted-foreground flex items-center gap-2">
            <span>Last updated: {new Date(currentPlan.updatedAt).toLocaleTimeString()}</span>
        </div>
      </div>

      <div class="h-px bg-border w-full my-6"></div>

      <!-- Steps -->
      <div class="space-y-4">
        {#each currentPlan.steps as step (step.id)}
          <Card className="p-4 transition-all hover:shadow-md border-l-4 {step.status === 'done' ? 'border-l-primary bg-primary/5' : step.status === 'in-progress' ? 'border-l-blue-500' : 'border-l-transparent'}">
             <div class="flex items-start gap-3">
               <button class="mt-1 w-5 h-5 rounded border border-input flex items-center justify-center {step.status === 'done' ? 'bg-primary border-primary text-primary-foreground' : 'text-transparent hover:border-primary'} transition-colors">
                  {#if step.status === 'done'}✓{/if}
               </button>
               <div class="flex-1 space-y-1">
                 <h3 class="font-medium text-base {step.status === 'done' ? 'line-through text-muted-foreground' : 'text-foreground'}">
                    {step.title}
                 </h3>
                 {#if step.description}
                   <p class="text-sm text-muted-foreground leading-relaxed">
                     {step.description}
                   </p>
                 {/if}
               </div>
               <div class="text-xs px-2 py-1 rounded-full bg-muted text-muted-foreground capitalize">
                 {step.status}
               </div>
             </div>
          </Card>
        {/each}
      </div>
    {/if}
  </div>
</div>
