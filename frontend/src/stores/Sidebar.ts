import { writable } from 'svelte/store';

export const sidebarIsOpen = writable<boolean | null>(null);

interface ItemFilters {
    user: string;
    status: string;
    node: string;
}
export const itemFilters = writable<ItemFilters>({
    user: 'All',
    status: 'All',
    node: 'All',
});