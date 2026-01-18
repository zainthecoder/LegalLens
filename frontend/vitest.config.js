import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
    plugins: [
        svelte({
            hot: !process.env.VITEST
        })
    ],
    test: {
        environment: 'jsdom',
        globals: true,
        include: ['src/**/*.test.js'],
        setupFiles: ['./vitest.setup.js'],
        alias: {
            '$lib': '/src/lib'
        },
        // Force browser conditions for Svelte 5
        server: {
            deps: {
                inline: ['svelte']
            }
        }
    },
    resolve: {
        conditions: ['browser']
    }
});
