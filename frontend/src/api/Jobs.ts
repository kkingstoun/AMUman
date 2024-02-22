import { api, sortState, activeJobs, lastFetchTime } from '$stores/store';
import { get } from 'svelte/store';
import type { Job } from './Api';
import { errorToast } from '$lib/Toast';

export async function fetchJobs() {
    try {
        const res = await api.jobsList();
        // Use the set method to update the store value
        activeJobs.set(res.data);
        sortJobs();
        // Update the lastFetchTime store with the current timestamp
        lastFetchTime.set(Date.now());
    } catch (err) {
        console.error(err);
        errorToast('Failed to fetch jobs');
    }
}


export function sortJobs(): void {
    activeJobs.update(jobs => {
        const currentSortState = get(sortState);

        // Use slice to create a copy for immutability
        return jobs.slice().sort((a: Job, b: Job) => {
            const aValue = a[currentSortState.column];
            const bValue = b[currentSortState.column];

            // Handle null or undefined values
            if (aValue == null || bValue == null) return 0;

            return (aValue < bValue ? -1 : 1) * currentSortState.direction;
        });
    });
}
