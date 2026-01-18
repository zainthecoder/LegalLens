<script>
  import { createEventDispatcher } from 'svelte';
  
  export let type = 'button';
  export let disabled = false;
  export let variant = 'default'; // default, outline, ghost, premium
  export let className = '';

  const dispatch = createEventDispatcher();

  const baseClass = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2";

  const variants = {
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
    ghost: "hover:bg-accent hover:text-accent-foreground",
    premium: "bg-primary text-primary-foreground border border-primary/20 shadow-sm hover:bg-primary/90 hover:shadow-md transition-all duration-300"
  };

  $: classes = `${baseClass} ${variants[variant] || variants.default} ${className}`;
</script>

<button {type} {disabled} class={classes} on:click>
  <slot />
</button>
