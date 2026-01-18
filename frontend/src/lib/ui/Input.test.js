/**
 * Component tests for Input
 */
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import Input from './Input.svelte';

describe('Input component', () => {
    describe('rendering', () => {
        it('renders with default props', () => {
            render(Input);
            const input = document.querySelector('input');
            expect(input).toBeTruthy();
            expect(input.type).toBe('text');
        });

        it('renders with placeholder', () => {
            render(Input, { props: { placeholder: 'Enter your email' } });
            const input = document.querySelector('input');
            expect(input.placeholder).toBe('Enter your email');
        });

        it('renders with email type', () => {
            render(Input, { props: { type: 'email' } });
            const input = document.querySelector('input');
            expect(input.type).toBe('email');
        });

        it('renders with password type', () => {
            render(Input, { props: { type: 'password' } });
            const input = document.querySelector('input');
            expect(input.type).toBe('password');
        });

        it('applies base styling classes', () => {
            render(Input);
            const input = document.querySelector('input');
            expect(input.className).toContain('rounded-md');
            expect(input.className).toContain('border');
        });

        it('applies custom className', () => {
            render(Input, { props: { className: 'custom-input' } });
            const input = document.querySelector('input');
            expect(input.className).toContain('custom-input');
        });
    });

    describe('disabled state', () => {
        it('is not disabled by default', () => {
            render(Input);
            const input = document.querySelector('input');
            expect(input.disabled).toBe(false);
        });

        it('can be disabled', () => {
            render(Input, { props: { disabled: true } });
            const input = document.querySelector('input');
            expect(input.disabled).toBe(true);
        });

        it('has disabled styles when disabled', () => {
            render(Input, { props: { disabled: true } });
            const input = document.querySelector('input');
            expect(input.className).toContain('disabled:cursor-not-allowed');
            expect(input.className).toContain('disabled:opacity-50');
        });
    });

    describe('value handling', () => {
        it('displays initial value', () => {
            render(Input, { props: { value: 'initial value' } });
            const input = document.querySelector('input');
            expect(input.value).toBe('initial value');
        });

        it('updates value on input', async () => {
            const { component } = render(Input, { props: { value: '' } });
            const input = document.querySelector('input');

            await fireEvent.input(input, { target: { value: 'new value' } });

            // The input's value should be updated
            expect(input.value).toBe('new value');
        });
    });

    describe('events', () => {
        it('fires input event', async () => {
            render(Input);
            const input = document.querySelector('input');

            let inputFired = false;
            input.addEventListener('input', () => { inputFired = true; });

            await fireEvent.input(input, { target: { value: 'test' } });
            expect(inputFired).toBe(true);
        });

        it('fires change event', async () => {
            render(Input);
            const input = document.querySelector('input');

            let changeFired = false;
            input.addEventListener('change', () => { changeFired = true; });

            await fireEvent.change(input, { target: { value: 'test' } });
            expect(changeFired).toBe(true);
        });
    });
});
