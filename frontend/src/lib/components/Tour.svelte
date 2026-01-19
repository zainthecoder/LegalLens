<script>
    import { onMount } from "svelte";

    // Configuration for the tour steps
    const steps = [
        {
            target: null,
            title: "Welcome to LegalLens",
            desc: "Your AI-powered legal project strategist. Let's walk through the workspace.",
            position: "center",
        },
        {
            target: "#tour-input",
            title: "Your Command Center",
            desc: "Type your legal goal here. Be specific—ask for a 'Motion to Dismiss' or a 'Due Diligence Checklist'.",
            position: "top",
        },
        {
            target: "#tour-plan",
            title: "The Strategy Plan (PDF)",
            desc: "This is your living document. As you chat, the AI builds a structured, exportable plan here.",
            position: "left",
        },
        {
            target: "#tour-plan",
            title: "Dynamic Updates",
            desc: "Note: The Chat (Left) is for conversation. The Plan (Right) only updates when specific steps are added or modified. Not every chat message goes here!",
            position: "left",
        },

        {
            target: "#tour-new-strategy",
            title: "Start Fresh",
            desc: "Click here to clear the workspace and begin a new legal strategy.",
            position: "bottom",
        },
        {
            target: "#tour-samples",
            title: "Need Inspiration?",
            desc: "Use legal templates for common tasks like Motion Practice or Family Law.",
            position: "bottom",
        },
    ];

    let currentStepIndex = 0;
    let isActive = false;
    let targetRect = null;

    $: currentStep = steps[currentStepIndex];

    const TOOLTIP_HEIGHT = 200; // approximate height
    const TOOLTIP_MARGIN = 20;

    function getTopPosition(step, rect) {
        if (!step.target || !rect) return "50%";

        let top;

        switch (step.position) {
            case "bottom":
                top = rect.bottom + TOOLTIP_MARGIN;
                break;
            case "top":
                top = rect.top - TOOLTIP_HEIGHT - TOOLTIP_MARGIN;
                break;
            default:
                top = rect.top + rect.height / 2 - TOOLTIP_HEIGHT / 2;
        }

        // Clamp to viewport bounds
        const maxTop = window.innerHeight - TOOLTIP_HEIGHT - TOOLTIP_MARGIN;
        return `${Math.max(TOOLTIP_MARGIN, Math.min(top, maxTop))}px`;
    }

    onMount(() => {
        const hasSeenTour = localStorage.getItem("legallens-tour-completed");
        if (!hasSeenTour) {
            setTimeout(() => {
                isActive = true;
                updatePosition();
            }, 1000); // Small delay to ensure UI loads
        }

        window.addEventListener("resize", updatePosition);
        return () => window.removeEventListener("resize", updatePosition);
    });

    function updatePosition() {
        if (!isActive || !currentStep.target) {
            targetRect = null;
            return;
        }
        const el = document.querySelector(currentStep.target);
        if (el) {
            targetRect = el.getBoundingClientRect();
        }
    }

    function next() {
        if (currentStepIndex < steps.length - 1) {
            currentStepIndex++;
            // Wait for DOM update or just next tick
            setTimeout(updatePosition, 0);
        } else {
            finish();
        }
    }

    function finish() {
        isActive = false;
        localStorage.setItem("legallens-tour-completed", "true");
    }
</script>

{#if isActive}
    <!-- Backdrop -->
    <div
        class="fixed inset-0 z-[100] bg-black/50 transition-opacity duration-300"
    >
        <!-- Spotlight Hole (Optional sophisticated impl omitted for simplicity, focusing on Tooltip) -->
        <!-- We will just position the tooltip relative to the target if it exists, or center if not -->

        <!-- Tooltip Card -->
        <div
            class="absolute bg-card text-card-foreground p-6 rounded-xl shadow-2xl border border-primary/20 w-80 max-w-[90vw] transition-all duration-300"
            style:top={getTopPosition(currentStep, targetRect)}
            style:left={currentStep.target && targetRect
                ? currentStep.position === "right"
                    ? `${targetRect.right + 20}px`
                    : currentStep.position === "left"
                      ? `${targetRect.left - 340}px`
                      : `${targetRect.left + targetRect.width / 2 - 160}px`
                : "50%"}
            style:transform={currentStep.target
                ? "none"
                : "translate(-50%, -50%)"}
        >
            <div class="flex justify-between items-start mb-4">
                <h3 class="font-playfair text-xl font-semibold text-primary">
                    {currentStep.title}
                </h3>
                <button
                    on:click={finish}
                    class="text-muted-foreground hover:text-foreground text-xs"
                    >Skip</button
                >
            </div>

            <p class="text-sm text-muted-foreground mb-6 leading-relaxed">
                {currentStep.desc}
            </p>

            <div class="flex items-center justify-between">
                <div class="flex gap-1">
                    {#each steps as _, i}
                        <div
                            class="h-1.5 w-1.5 rounded-full transition-colors {i ===
                            currentStepIndex
                                ? 'bg-primary'
                                : 'bg-muted'}"
                        ></div>
                    {/each}
                </div>

                <button
                    on:click={next}
                    class="bg-primary text-primary-foreground px-4 py-1.5 rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                    {currentStepIndex === steps.length - 1
                        ? "Get Started"
                        : "Next"}
                </button>
            </div>

            <!-- Arrow (Simplified) -->
            {#if currentStep.target}
                <div
                    class="absolute w-4 h-4 bg-card border-l border-t border-primary/20 transform rotate-45"
                    style:top={currentStep.position === "bottom"
                        ? "-8px"
                        : "auto"}
                    style:bottom={currentStep.position === "top"
                        ? "-8px"
                        : "auto"}
                    style:left={currentStep.position === "left"
                        ? "auto"
                        : "50%"}
                    style:right={currentStep.position === "left"
                        ? "-8px"
                        : "auto"}
                ></div>
            {/if}
        </div>
    </div>
{/if}
