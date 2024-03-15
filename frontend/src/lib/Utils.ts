import type { ItemType } from '$stores/Tables';
import { toasts, type ToastColor } from '$stores/Other';
import type { Job, Gpu, Node } from '$api/OpenApi';
import { DateTime } from 'luxon';
import { get, type Writable } from 'svelte/store';
import { accessToken, refreshToken } from '$stores/Auth';
import { sidebarIsOpen } from '$stores/Other';
import { shownColumns, sortStates, headers } from '$stores/Tables';
import { type KeyLists } from '$stores/Tables'; // Import the KeyLists type from the appropriate location

export function formatString(input: string): string {
    const replacedString = input.replace(/_/g, ' ');
    const capitalizedString = replacedString.charAt(0).toUpperCase() + replacedString.slice(1);

    return capitalizedString;
}

export function formatValue(
    item: ItemType,
    key: string,
): string | number | null | undefined {
    const value = item[key as keyof ItemType];
    return value;
}

export type ColorType =
    | 'none'
    | 'red'
    | 'yellow'
    | 'green'
    | 'indigo'
    | 'purple'
    | 'pink'
    | 'blue'
    | 'dark'
    | 'primary'
    | undefined;

export function newToast(message: string, color: ToastColor): void {
    const id = Date.now(); // Using a timestamp as a simple unique ID
    toasts.update((t) => {
        const toast = { message, color, id };
        return [...t, toast];
    });

    setTimeout(() => {
        toasts.update((t) => {
            return t.filter(toast => toast.id !== id); // Remove the toast by ID
        });
    }, 2000);
}
export function isJob(item: ItemType): item is Job {
    return 'path' in item;
}
export function isNode(item: ItemType): item is Node {
    return 'number_of_gpus' in item;
}
export function isGpu(item: ItemType): item is Gpu {
    return 'speed' in item;
}
export function formatDateTime(dateString?: string | null): string {
    if (!dateString) return '-';
    dateString = DateTime.fromISO(dateString).setLocale('en-GB').toRelative();
    if (dateString) return dateString;
    else return '-';
};

export function getPropertyValue(item: ItemType, property: string): string | undefined {
    return (item as any)[property];
}

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
}

export function orderShownColumnsLikeHeaders(): void {
    const currentHeaders = get(headers);

    shownColumns.update(currentShownColumns => {
        // Iterate over each key in currentShownColumns and reorder according to currentHeaders
        Object.keys(currentShownColumns).forEach(key => {
            if (currentHeaders[key as keyof KeyLists]) { // Add type assertion to keyof KeyLists
                currentShownColumns[key as keyof KeyLists] = (currentShownColumns[key as keyof KeyLists] as (keyof Node)[] & (keyof Job)[] & (keyof Gpu)[]).sort((a, b) => {
                    // Use the order in currentHeaders[key] to sort currentShownColumns[key]
                    return (currentHeaders[key as keyof KeyLists] as ("id" | "status")[])
                        .indexOf(a as "id" | "status") - (currentHeaders[key as keyof KeyLists] as ("id" | "status")[]).indexOf(b as "id" | "status");
                });
            }
        });

        return currentShownColumns; // Return the newly ordered shownColumns
    });
}