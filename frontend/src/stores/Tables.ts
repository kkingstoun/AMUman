import { writable } from 'svelte/store';
import type { Nodes, Job, Gpus } from '$api/Api';

export const refreshInterval = writable(60 * 1000);
export const timeSinceLastFetch = writable('Never');
export const lastFetchTime = writable(0);

export type ItemTypeString = "nodes" | "jobs" | "gpus";
export type ItemType = Nodes | Job | Gpus;

interface ItemList {
    nodes: Nodes[];
    jobs: Job[];
    gpus: Gpus[];
}
export const itemlist = writable<ItemList>({
    nodes: [],
    jobs: [],
    gpus: []
});

interface SelectedItems {
    nodes: Array<number | string>;
    jobs: Array<number | string>;
    gpus: Array<number | string>;
}
export const selectedItems = writable<SelectedItems>(
    { nodes: [], jobs: [], gpus: [] }
);

interface SortState {
    column: keyof Nodes;
    direction: 1 | -1; // 1 for ascending, -1 for descending
}
interface SortStates {
    nodes: SortState;
    jobs: SortState;
    gpus: SortState;
}
export const sortStates = writable<SortStates>({
    nodes: { column: 'id', direction: 1 },
    jobs: { column: 'id', direction: 1 },
    gpus: { column: 'id', direction: 1 }
});

interface KeyLists {
    nodes: (keyof Nodes)[];
    jobs: (keyof Job)[];
    gpus: (keyof Gpus)[];
}
export const shownColumns = writable<KeyLists>({
    nodes: [
        'id',
        'name',
        'ip',
        'status'
    ],
    jobs: [
        'id',
        'path',
        'port',
        'submit_time',
        'start_time',
        'end_time',
        'priority',
        'status'
    ],
    gpus: [
        'id',
        'model'
    ]
});

export const headers = writable<KeyLists>({
    nodes: [
        'id',
        'ip',
        'name',
        'number_of_gpus',
        'status',
        'connection_status',
        'last_seen',
    ],
    jobs: [
        'id',
        'path',
        'port',
        'submit_time',
        'start_time',
        'end_time',
        'error_time',
        'priority',
        'gpu_partition',
        'duration',
        'status',
        'error',
        'flags',
        'node',
        'gpu',
    ],
    gpus: [
        'id',
        'speed',
        'status',
        'node',
        'device_id',
        'uuid',
        'model',
        'util',
        'is_running_amumax',
    ]
});

