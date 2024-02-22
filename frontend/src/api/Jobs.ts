import { api, sortState, activeJobs, lastFetchTime, selectedJobs } from '$stores/store';
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
        // errorToast('Failed to fetch jobs');
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

export async function deleteJob(jobId: number) {
    try {
        await api.jobsDestroy(jobId);
    } catch (err) {
        console.error(err);
        errorToast(`Failed to delete job ${jobId}`);
    }
    // Update the activeJobs store by removing the deleted job
    activeJobs.update(jobs => jobs.filter(job => job.id !== jobId));

}

export async function deleteSelectedJobs() {
    for (const job of get(activeJobs)) {
        if (job.id && get(selectedJobs).includes(job.id)) {
            deleteJob(job.id);
            // remove the job from the selectedJobs store
            selectedJobs.update(jobs => jobs.filter(id => id !== job.id));
        }
    }
}