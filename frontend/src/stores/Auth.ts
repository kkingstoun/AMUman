import { writable } from 'svelte/store';
import { Api, type RequestParams } from '$api/Api';

export const accessToken = writable<string | null>(null);
export const refreshToken = writable<string | null>(null);
export const requestParams = writable<RequestParams>({});
export const api = new Api<string>({ baseUrl: 'http://localhost:8000' }).api;