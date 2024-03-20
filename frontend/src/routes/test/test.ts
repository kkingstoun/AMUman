import { get } from 'svelte/store';
import { accessToken, api } from '$stores/Auth';
import { jobsFilters } from '$stores/Sidebar';

export async function fetchJobs(): Promise<void> {
    type JobQuery = {
        gpu?: number;
        limit?: number;
        node?: number;
        offset?: number;
        priority?: 'HIGH' | 'LOW' | 'NORMAL';
        status?: 'FINISHED' | 'INTERRUPTED' | 'PENDING';
        user?: string;
    };

    let query: JobQuery = {
        limit: 10,
        offset: 0,
        status: "PENDING", // This is correctly typed now
    };

    const params = {
        headers: { Authorization: `Bearer ${get(accessToken)}` },
    };
    let jobs = [];
    await api
        .jobsList(query, params)
        .then((res) => {
            console.log(res);
            let data = res.data.results;
            if (data) {
                jobs = data;
                console.log(jobs);
            }
        })
        .catch((error) => {
            console.error('Error fetching jobs:', error);
        });

};
