/**
 * Unit tests for plan store
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { plan } from './plan.js';

describe('plan store', () => {
    beforeEach(() => {
        // Reset to default state
        plan.set({
            id: '',
            title: '',
            steps: [],
            updatedAt: ''
        });
    });

    describe('initial state', () => {
        it('has correct default values', () => {
            const state = get(plan);
            expect(state.id).toBe('');
            expect(state.title).toBe('');
            expect(state.steps).toEqual([]);
            expect(state.updatedAt).toBe('');
        });
    });

    describe('set', () => {
        it('updates store with new values', () => {
            const newPlan = {
                id: 'plan-123',
                title: 'Motion for Summary Judgment',
                steps: [
                    { id: '1', title: 'Research case law', status: 'pending' },
                    { id: '2', title: 'Draft motion', status: 'pending' }
                ],
                updatedAt: '2024-01-18T12:00:00Z'
            };

            plan.set(newPlan);

            const state = get(plan);
            expect(state.id).toBe('plan-123');
            expect(state.title).toBe('Motion for Summary Judgment');
            expect(state.steps).toHaveLength(2);
            expect(state.steps[0].title).toBe('Research case law');
        });

        it('can update partial values', () => {
            plan.set({
                id: 'plan-123',
                title: 'Original Title',
                steps: [],
                updatedAt: ''
            });

            // Update with new title
            plan.update(current => ({
                ...current,
                title: 'Updated Title'
            }));

            const state = get(plan);
            expect(state.title).toBe('Updated Title');
            expect(state.id).toBe('plan-123');
        });
    });

    describe('subscribe', () => {
        it('notifies subscribers on changes', () => {
            const values = [];
            const unsubscribe = plan.subscribe(value => {
                values.push(value.title);
            });

            plan.set({ id: '', title: 'First', steps: [], updatedAt: '' });
            plan.set({ id: '', title: 'Second', steps: [], updatedAt: '' });

            expect(values).toContain('First');
            expect(values).toContain('Second');

            unsubscribe();
        });

        it('stops notifying after unsubscribe', () => {
            let updateCount = 0;
            const unsubscribe = plan.subscribe(() => {
                updateCount++;
            });

            // Initial subscription call
            const initialCount = updateCount;

            plan.set({ id: '', title: 'Update 1', steps: [], updatedAt: '' });
            expect(updateCount).toBe(initialCount + 1);

            unsubscribe();

            plan.set({ id: '', title: 'Update 2', steps: [], updatedAt: '' });
            expect(updateCount).toBe(initialCount + 1); // Should not increase
        });
    });
});
