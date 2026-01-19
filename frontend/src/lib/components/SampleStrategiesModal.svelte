<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let isOpen = false;

    const strategies = [
        {
            title: "Motion Practice",
            prompt: "Help me plan a Motion to Dismiss for Lack of Jurisdiction in NY Supreme Court.",
            icon: "⚖️",
        },
        {
            title: "Corporate Due Diligence",
            prompt: "Create a checklist for a Series A Investment Due Diligence review.",
            icon: "🏢",
        },
        {
            title: "Family Law",
            prompt: "Plan a Child Custody Modification petition in California Superior Court.",
            icon: "👨‍👩‍👧",
        },
    ];

    function useStrategy(prompt) {
        // Dispatch event to parent to handle the prompt injection
        dispatch("useStrategy", prompt);
        isOpen = false;
    }
</script>

{#if isOpen}
    <!-- Backdrop -->
    <div
        class="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200"
        on:click={() => (isOpen = false)}
    >
        <!-- Modal Content -->
        <div
            class="bg-card w-full max-w-2xl rounded-xl border border-border shadow-2xl overflow-hidden transform transition-all animate-in zoom-in-95 duration-200"
            on:click|stopPropagation
        >
            <!-- Header -->
            <div
                class="px-6 py-4 border-b border-border flex items-center justify-between bg-muted/30"
            >
                <div>
                    <h2
                        class="font-playfair text-xl font-semibold text-foreground"
                    >
                        Sample Strategies
                    </h2>
                    <p class="text-sm text-muted-foreground mt-1">
                        Select a template to jumpstart your planning.
                    </p>
                </div>
                <button
                    on:click={() => (isOpen = false)}
                    class="text-muted-foreground hover:text-foreground p-1 rounded-md hover:bg-muted transition-colors"
                >
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
                        ><line x1="18" x2="6" y1="6" y2="18" /><line
                            x1="6"
                            x2="18"
                            y1="6"
                            y2="18"
                        /></svg
                    >
                </button>
            </div>

            <!-- Grid of Strategies -->
            <div class="p-6 grid gap-4 sm:grid-cols-1 md:grid-cols-3">
                {#each strategies as s}
                    <button
                        on:click={() => useStrategy(s.prompt)}
                        class="flex flex-col text-left h-full p-4 rounded-lg border border-border bg-background hover:bg-primary/5 hover:border-primary/30 transition-all group"
                    >
                        <div
                            class="text-2xl mb-3 group-hover:scale-110 transition-transform duration-200"
                        >
                            {s.icon}
                        </div>
                        <h3
                            class="font-semibold text-foreground mb-2 group-hover:text-primary transition-colors"
                        >
                            {s.title}
                        </h3>
                        <p
                            class="text-xs text-muted-foreground leading-relaxed mb-4 flex-grow italic"
                        >
                            "{s.prompt}"
                        </p>
                        <div
                            class="text-xs font-medium text-primary opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1"
                        >
                            Use Template
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="12"
                                height="12"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                ><path d="M5 12h14" /><path
                                    d="m12 5 7 7-7 7"
                                /></svg
                            >
                        </div>
                    </button>
                {/each}
            </div>

            <!-- Footer -->
            <div
                class="px-6 py-3 bg-muted/30 border-t border-border text-center"
            >
                <p class="text-xs text-muted-foreground">
                    Tip: You can always customize these strategies later in the
                    chat.
                </p>
            </div>
        </div>
    </div>
{/if}
