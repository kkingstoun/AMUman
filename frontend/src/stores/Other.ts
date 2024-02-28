import { writable } from 'svelte/store';

export const sidebarIsOpen = writable<boolean | null>(null);