import { writable } from 'svelte/store';

function createAuthStore() {
    const { subscribe, set, update } = writable({
        isAuthenticated: false,
        user: null,
        token: null,
        isLoading: true
    });

    return {
        subscribe,
        init: async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    // Validate token with backend
                    const res = await fetch('http://localhost:8000/api/auth/me', {
                        headers: { Authorization: `Bearer ${token}` }
                    });

                    if (res.ok) {
                        const user = await res.json();
                        set({ isAuthenticated: true, user, token, isLoading: false });
                    } else {
                        // Token invalid/expired
                        localStorage.removeItem('token');
                        set({ isAuthenticated: false, user: null, token: null, isLoading: false });
                    }
                } catch (e) {
                    console.error("Auth init error", e);
                    set({ isAuthenticated: false, user: null, token: null, isLoading: false });
                }
            } else {
                set({ isAuthenticated: false, user: null, token: null, isLoading: false });
            }
        },
        login: async (email, password) => {
            const formData = new FormData();
            formData.append('username', email); // OAuth2PasswordRequestForm expects username
            formData.append('password', password);

            const res = await fetch('http://localhost:8000/api/auth/token', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Login failed');
            }

            const data = await res.json(); // { access_token, token_type }
            const token = data.access_token;
            localStorage.setItem('token', token);

            // Get User Details
            const userRes = await fetch('http://localhost:8000/api/auth/me', {
                headers: { Authorization: `Bearer ${token}` }
            });
            const user = await userRes.json();

            set({ isAuthenticated: true, user, token, isLoading: false });
        },
        register: async (email, password) => {
            const res = await fetch('http://localhost:8000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Registration failed');
            }
            // After register, you can auto-login or ask user to login
            return await res.json();
        },
        logout: () => {
            localStorage.removeItem('token');
            set({ isAuthenticated: false, user: null, token: null, isLoading: false });
        }
    };
}

export const auth = createAuthStore();
