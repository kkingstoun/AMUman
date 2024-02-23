import { writable } from 'svelte/store';

export const isAuthenticated = writable<boolean>(true);
export const selectedPage = writable<string>('Running');