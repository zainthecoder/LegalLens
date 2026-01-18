/**
 * Unit tests for auth store
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { get } from 'svelte/store';

// Mock fetch globally
global.fetch = vi.fn();

// We need to reset and reimport the store for each test to get fresh state
describe('auth store', () => {
    let auth;

    beforeEach(async () => {
        vi.resetModules();
        vi.clearAllMocks();
        localStorage.getItem.mockReturnValue(null);

        // Dynamically import to get fresh store instance
        const module = await import('./auth.js');
        auth = module.auth;
    });

    describe('initial state', () => {
        it('has correct default values', () => {
            const state = get(auth);
            expect(state.isAuthenticated).toBe(false);
            expect(state.user).toBe(null);
            expect(state.token).toBe(null);
            expect(state.loading).toBe(true);
        });
    });

    describe('login', () => {
        it('sets authenticated state on successful login', async () => {
            const mockToken = 'test-token-123';
            const mockUser = { email: 'test@example.com', id: '1' };

            global.fetch
                .mockResolvedValueOnce({
                    ok: true,
                    json: () => Promise.resolve({ access_token: mockToken })
                })
                .mockResolvedValueOnce({
                    ok: true,
                    json: () => Promise.resolve(mockUser)
                });

            const result = await auth.login('test@example.com', 'password123');

            expect(result).toBe(true);
            const state = get(auth);
            expect(state.isAuthenticated).toBe(true);
            expect(state.token).toBe(mockToken);
            expect(state.user).toEqual(mockUser);
            expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
        });

        it('returns false on login failure', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: false,
                json: () => Promise.resolve({ detail: 'Invalid credentials' })
            });

            const result = await auth.login('test@example.com', 'wrongpassword');

            expect(result).toBe(false);
            const state = get(auth);
            expect(state.isAuthenticated).toBe(false);
        });

        it('handles network errors gracefully', async () => {
            global.fetch.mockRejectedValueOnce(new Error('Network error'));

            const result = await auth.login('test@example.com', 'password');

            expect(result).toBe(false);
        });
    });

    describe('logout', () => {
        it('clears authentication state', async () => {
            // First login
            global.fetch
                .mockResolvedValueOnce({
                    ok: true,
                    json: () => Promise.resolve({ access_token: 'token' })
                })
                .mockResolvedValueOnce({
                    ok: true,
                    json: () => Promise.resolve({ email: 'test@example.com' })
                });

            await auth.login('test@example.com', 'password');

            // Then logout
            auth.logout();

            const state = get(auth);
            expect(state.isAuthenticated).toBe(false);
            expect(state.user).toBe(null);
            expect(state.token).toBe(null);
            expect(localStorage.removeItem).toHaveBeenCalledWith('token');
        });
    });

    describe('register', () => {
        it('returns true on successful registration', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ id: '1', email: 'new@example.com' })
            });

            const result = await auth.register('new@example.com', 'password123');

            expect(result).toBe(true);
            expect(global.fetch).toHaveBeenCalledWith(
                'http://localhost:8000/api/auth/register',
                expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: 'new@example.com', password: 'password123' })
                })
            );
        });

        it('throws error on registration failure', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: false,
                json: () => Promise.resolve({ detail: 'Email already registered' })
            });

            await expect(auth.register('existing@example.com', 'password'))
                .rejects.toThrow('Email already registered');
        });
    });

    describe('init', () => {
        it('restores session from valid token', async () => {
            const mockUser = { email: 'test@example.com', id: '1' };
            localStorage.getItem.mockReturnValue('saved-token');

            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve(mockUser)
            });

            await auth.init();

            const state = get(auth);
            expect(state.isAuthenticated).toBe(true);
            expect(state.token).toBe('saved-token');
            expect(state.user).toEqual(mockUser);
            expect(state.loading).toBe(false);
        });

        it('clears state when token is invalid', async () => {
            localStorage.getItem.mockReturnValue('invalid-token');

            global.fetch.mockResolvedValueOnce({
                ok: false,
                json: () => Promise.resolve({ detail: 'Invalid token' })
            });

            await auth.init();

            const state = get(auth);
            expect(state.isAuthenticated).toBe(false);
            expect(state.loading).toBe(false);
        });

        it('sets loading false when no token exists', async () => {
            localStorage.getItem.mockReturnValue(null);

            await auth.init();

            const state = get(auth);
            expect(state.isAuthenticated).toBe(false);
            expect(state.loading).toBe(false);
        });
    });
});
