import { writable } from 'svelte/store';
import { plan } from './plan';

function createAuthStore() {
    const { subscribe, set, update } = writable({
        isAuthenticated: false,
        user: null,
        token: null,
        loading: true
    });

    return {
        subscribe,
        login: async (email, password) => {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            try {
                const res = await fetch('http://localhost:8000/api/auth/token', {
                    method: 'POST',
                    body: formData
                });

                if (!res.ok) throw new Error('Login failed');

                const data = await res.json();
                const token = data.access_token;

                // Get User Details
                const userRes = await fetch('http://localhost:8000/api/auth/me', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const user = await userRes.json();

                // Save to local storage
                localStorage.setItem('token', token);

                set({ isAuthenticated: true, user, token, loading: false });
                return true;
            } catch (e) {
                console.error(e);
                return false;
            }
        },
        logout: () => {
            localStorage.removeItem('token');
            plan.set({ id: '', title: '', steps: [], updatedAt: '' });
            set({ isAuthenticated: false, user: null, token: null, loading: false });
        },
        register: async (email, password) => {
            try {
                const res = await fetch('http://localhost:8000/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (!res.ok) {
                    const errorData = await res.json();
                    throw new Error(errorData.detail || 'Registration failed');
                }
                return true;
            } catch (e) {
                console.error(e);
                throw e;
            }
        },
        init: async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const userRes = await fetch('http://localhost:8000/api/auth/me', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (userRes.ok) {
                        const user = await userRes.json();
                        set({ isAuthenticated: true, user, token, loading: false });
                        return;
                    }
                } catch (e) {
                    console.error(e);
                }
            }
            set({ isAuthenticated: false, user: null, token: null, loading: false });
        }
    };
}

export const auth = createAuthStore();
