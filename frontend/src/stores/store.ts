import { writable } from 'svelte/store';
import { Api } from '$api/Api';
import type { Job } from '$api/Api';

export const isAuthenticated = writable<boolean>(true);

export const activePage = writable<string>('Running');

export const api = new Api<string>({ baseUrl: 'http://localhost:8000' }).api;
export const refreshInterval = writable(60 * 1000);
export const timeSinceLastFetch = writable('');
export const lastFetchTime = writable(0);
export const activeJobs = writable<Job[]>([]);
export const selectedJobs = writable<Array<number | string>>([]);

export const shownColumns = writable<(keyof Job)[]>([
	'id',
	'path',
	'port',
	'submit_time',
	'start_time',
	'end_time',
	'error_time',
	'priority',
	'estimated_simulation_time',
	'status'
]);

interface SortState {
	column: keyof Job;
	direction: 1 | -1; // 1 for ascending, -1 for descending
}
export const sortState = writable<SortState>({
	column: 'id',
	direction: 1
});