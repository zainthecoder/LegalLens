import '@testing-library/svelte/vitest';

// Mock localStorage for tests
const localStorageMock = {
    store: {},
    getItem: function (key) {
        return this.store[key] || null;
    },
    setItem: function (key, value) {
        this.store[key] = value;
    },
    removeItem: function (key) {
        delete this.store[key];
    },
    clear: function () {
        this.store = {};
    }
};

// Mock localStorage with spies
vi.stubGlobal('localStorage', {
    getItem: vi.fn((key) => localStorageMock.getItem(key)),
    setItem: vi.fn((key, value) => localStorageMock.setItem(key, value)),
    removeItem: vi.fn((key) => localStorageMock.removeItem(key)),
    clear: vi.fn(() => localStorageMock.clear())
});

// Reset mocks between tests
beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
});
