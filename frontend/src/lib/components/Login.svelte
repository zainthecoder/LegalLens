<script>
    import { auth } from "../stores/auth.js";
    import Button from "../ui/Button.svelte";
    import Input from "../ui/Input.svelte";

    let email = "";
    let password = "";
    let isRegistering = false;
    let error = "";
    let isLoading = false;

    async function handleSubmit() {
        error = "";
        isLoading = true;
        try {
            if (isRegistering) {
                await auth.register(email, password);
                // Auto login after register
                await auth.login(email, password);
            } else {
                await auth.login(email, password);
            }
        } catch (e) {
            error = e.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div
    class="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 p-4"
>
    <div
        class="bg-card text-card-foreground p-8 rounded-xl shadow-lg border border-border w-full max-w-md space-y-6"
    >
        <div class="text-center space-y-2">
            <div
                class="mx-auto w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary mb-4"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    ><path
                        d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"
                    /><path
                        d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"
                    /><path d="M7 21h10" /><path d="M12 3v18" /><path
                        d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"
                    /></svg
                >
            </div>
            <h1 class="text-2xl font-serif font-bold tracking-tight">
                LegalLens
            </h1>
            <p class="text-muted-foreground text-sm">
                {isRegistering
                    ? "Create your professional account"
                    : "Sign in to access your strategies"}
            </p>
        </div>

        {#if error}
            <div
                class="p-3 rounded-md bg-destructive/10 text-destructive text-sm font-medium animate-in fade-in slide-in-from-top-2"
            >
                {error}
            </div>
        {/if}

        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div class="space-y-2">
                <label for="email" class="text-sm font-medium">Email</label>
                <Input
                    type="email"
                    id="email"
                    bind:value={email}
                    placeholder="attorney@lawfirm.com"
                    required
                    disabled={isLoading}
                />
            </div>

            <div class="space-y-2">
                <label for="password" class="text-sm font-medium"
                    >Password</label
                >
                <Input
                    type="password"
                    id="password"
                    bind:value={password}
                    required
                    disabled={isLoading}
                />
            </div>

            <Button type="submit" class="w-full" disabled={isLoading}>
                {isLoading
                    ? "Loading..."
                    : isRegistering
                      ? "Create Account"
                      : "Sign In"}
            </Button>
        </form>

        <div class="text-center text-sm text-muted-foreground">
            {isRegistering
                ? "Already have an account?"
                : "Don't have an account?"}
            <button
                class="font-medium text-primary hover:underline ml-1"
                on:click={() => {
                    isRegistering = !isRegistering;
                    error = "";
                }}
            >
                {isRegistering ? "Sign In" : "Register"}
            </button>
        </div>
    </div>
</div>
