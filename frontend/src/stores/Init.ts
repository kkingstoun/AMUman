import { get, type Writable } from 'svelte/store';
import { accessToken, refreshToken } from '$stores/Auth';
import { sidebarIsOpen } from '$stores/Sidebar';
import { shownColumns, sortStates } from '$stores/Tables';

function getLocalStorageItem<T>(store: Writable<T>, key: string): T {
    const item = localStorage.getItem(key);
    if (item) {
        try {
            return JSON.parse(item) as T;
        } catch (error) {
            console.error(`Error parsing ${key} from localStorage:`, error);
            return get(store); // Fall back to the store's default value
        }
    }
    return get(store); // Return the store's default value if the item is not found
}
function subscribeAndPersist<T>(store: Writable<T>, key: string): void {
    store.subscribe((value) => {
        localStorage.setItem(key, JSON.stringify(value));
    });
}
function InitOneStore<T>(store: Writable<T>, key: string): void {
    store.set(getLocalStorageItem(store, key));
    subscribeAndPersist(store, key);
}
export function initStores(): void {
    InitOneStore(accessToken, 'accessToken');
    InitOneStore(refreshToken, 'refresh');
    InitOneStore(sidebarIsOpen, 'sidebarIsOpen');
    InitOneStore(shownColumns, 'shownColumns');
    InitOneStore(sortStates, 'sortStates');
    console.log('Stores initialized');
    console.log('accessToken:', get(sidebarIsOpen));
}
