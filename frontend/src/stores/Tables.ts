import { writable } from 'svelte/store';
import type { Node, Job, Gpu } from '$api/Api';
import { DateTime } from 'luxon';

export const refreshInterval = writable(30 * 1000);
export const lastFetchTime = writable<DateTime | null>(null);
export const isRefreshing = writable(false);
export const refreshLastFetchTimeInterval = writable<ReturnType<typeof setInterval>>();
export const refreshItemsInterval = writable<ReturnType<typeof setInterval>>();
export type ItemTypeString = "nodes" | "jobs" | "gpus";
export type ItemType = Node | Job | Gpu;

interface ItemList {
    nodes: Node[];
    jobs: Job[];
    gpus: Gpu[];
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
    column: keyof Node;
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
    nodes: (keyof Node)[];
    jobs: (keyof Job)[];
    gpus: (keyof Gpu)[];
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
        'user',
        'submit_time',
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
        'flags',
        'node',
        'gpu',
        'user',
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

