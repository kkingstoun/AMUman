import { writable } from 'svelte/store';

export const api = writable<URL>(new URL('./api', window.location.href));