import { writable } from 'svelte/store';
import { Api } from '$api/Api';

export const isAuthenticated = writable<boolean>(true);
export const accessToken = writable<string | null>(null);
export const activePage = writable<string>('Running');
export const api = new Api<string>({ baseUrl: 'http://localhost:8000' }).api;