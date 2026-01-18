import { writable } from 'svelte/store';

export const plan = writable({
    id: '',
    title: '',
    steps: [],
    updatedAt: ''
});
