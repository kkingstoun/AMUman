import { writable } from 'svelte/store';

export const sidebarIsOpen = writable<boolean | null>(true);

export type JobQuery = {
    gpu?: number;
    node?: number;
    priority?: 'HIGH' | 'LOW' | 'NORMAL';
    status?: 'FINISHED' | 'INTERRUPTED' | 'PENDING';
    user?: string;
    limit: number;
    offset: number;
};
export const jobsFilters = writable<JobQuery>({
    user: undefined,
    status: undefined,
    node: undefined,
    gpu: undefined,
    priority: undefined,
    offset: 0,
    limit: 5,
});

export type NodeQuery = {
    limit?: number;
    offset?: number;
    status?: 'ACTIVE' | 'INACTIVE';
    user?: string;
};
export const nodesFilters = writable<NodeQuery>({
    user: undefined,
    status: undefined,
    limit: undefined,
    offset: undefined,
});

export type GpuQuery = {
    limit?: number;
    offset?: number;
};
export const gpusFilters = writable<GpuQuery>({
    limit: undefined,
    offset: undefined,
});

