import { writable } from 'svelte/store';
import { Api, type RequestParams } from '$api/OpenApi';

export const accessToken = writable<string | null>(null);
export const refreshToken = writable<string | null>(null);
export const requestParams = writable<RequestParams>({});
export const api = new Api<string>({ baseUrl: '.' }).api;