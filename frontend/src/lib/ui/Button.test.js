/**
 * Component tests for Button
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/svelte';
import Button from './Button.svelte';

describe('Button component', () => {
    describe('rendering', () => {
        it('renders with default props', () => {
            render(Button, { props: { $$slots: { default: () => 'Click me' } } });
            // Button should be in the document
            const button = document.querySelector('button');
            expect(button).toBeTruthy();
            expect(button.type).toBe('button');
        });

        it('renders with submit type', () => {
            render(Button, { props: { type: 'submit' } });
            const button = document.querySelector('button');
            expect(button.type).toBe('submit');
        });

        it('applies default variant classes', () => {
            render(Button);
            const button = document.querySelector('button');
            expect(button.className).toContain('bg-primary');
        });

        it('applies outline variant classes', () => {
            render(Button, { props: { variant: 'outline' } });
            const button = document.querySelector('button');
            expect(button.className).toContain('border');
            expect(button.className).toContain('bg-background');
        });

        it('applies ghost variant classes', () => {
            render(Button, { props: { variant: 'ghost' } });
            const button = document.querySelector('button');
            expect(button.className).toContain('hover:bg-accent');
        });

        it('applies premium variant classes', () => {
            render(Button, { props: { variant: 'premium' } });
            const button = document.querySelector('button');
            expect(button.className).toContain('shadow');
        });

        it('applies custom className', () => {
            render(Button, { props: { className: 'custom-class' } });
            const button = document.querySelector('button');
            expect(button.className).toContain('custom-class');
        });
    });

    describe('disabled state', () => {
        it('is not disabled by default', () => {
            render(Button);
            const button = document.querySelector('button');
            expect(button.disabled).toBe(false);
        });

        it('can be disabled', () => {
            render(Button, { props: { disabled: true } });
            const button = document.querySelector('button');
            expect(button.disabled).toBe(true);
        });

        it('has disabled styles when disabled', () => {
            render(Button, { props: { disabled: true } });
            const button = document.querySelector('button');
            expect(button.className).toContain('disabled:opacity-50');
        });
    });

    describe('interactions', () => {
        it('handles click events', async () => {
            render(Button);
            const button = document.querySelector('button');

            let clicked = false;
            button.addEventListener('click', () => { clicked = true; });

            await fireEvent.click(button);
            expect(clicked).toBe(true);
        });
    });
});
