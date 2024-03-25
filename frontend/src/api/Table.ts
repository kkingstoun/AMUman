import { sortStates, itemlist, lastFetchTime, selectedItems, type ItemTypeString } from '$stores/Tables';
import { api } from '$stores/Auth';
import { get } from 'svelte/store';
import { newToast } from '$stores/Toast';
import { getRequestParams } from './Auth';
import type { Node, Job } from '$api/OpenApi';
import { DateTime } from 'luxon';
import { jobsFilters, nodesFilters, gpusFilters } from '$stores/Sidebar';
import { pagination } from '$stores/Tables';


export async function fetchJobs(): Promise<void> {

    const params = getRequestParams();
    if (params !== null) {
        await api.jobsList(get(jobsFilters), params).then((res) => {
            pagination.set(
                {
                    count: res.data.count,
                }
            )
            let data = res.data.results;
            if (data !== undefined) {
                itemlist.update(itemList => {
                    itemList.jobs = data ?? [];
                    return itemList;
                });
                sortItems('jobs');
                lastFetchTime.set(DateTime.now().setLocale('en-GB'));
            }
        }).catch((res) => {
            for (let field in res.error) {
                newToast(`Failed to fetch jobs: ${res.error[field]}`, 'red');
            }
        });
    }
}
export async function fetchNodes(): Promise<void> {
    const params = getRequestParams();
    if (params !== null) {
        await api.nodesList(get(nodesFilters), params).then((res) => {
            let data = res.data.results;
            if (data !== undefined) {
                itemlist.update(itemList => {
                    itemList.nodes = data ?? [];
                    return itemList;
                });
                sortItems('nodes');
                lastFetchTime.set(DateTime.now().setLocale('en-GB'));
            }
        }).catch((res) => {
            for (let field in res.error) {
                newToast(`Failed to fetch nodes: ${res.error[field]}`, 'red');
            }
        });
    }
}
export async function fetchGpus(): Promise<void> {
    const params = getRequestParams();
    if (params !== null) {
        await api.gpusList(get(gpusFilters), params).then((res) => {
            let data = res.data.results;
            if (data !== undefined) {
                itemlist.update(itemList => {
                    itemList.gpus = data ?? [];
                    return itemList;
                });
                sortItems('gpus');
                lastFetchTime.set(DateTime.now().setLocale('en-GB'));
            }
        }).catch((res) => {
            for (let field in res.error) {
                newToast(`Failed to fetch gpus: ${res.error[field]}`, 'red');
            }
        });
    }
}

export async function fetchItems<T extends ItemTypeString>(itemType: T): Promise<void> {
    if (itemType === 'jobs') {
        await fetchJobs();
    } else if (itemType === 'nodes') {
        await fetchNodes();
    } else if (itemType === 'gpus') {
        await fetchGpus();
    }
}

export function sortItems(item_type: 'jobs' | 'nodes' | 'gpus'): void {
    itemlist.update(list => {
        // Copy to maintain immutability
        const itemsCopy = [...list[item_type]];

        const currentSortState = get(sortStates)[item_type];
        if (!currentSortState) return list; // Early return if sort state is undefined

        itemsCopy.sort((a, b) => {
            const aValue = (a as any)[currentSortState.column];
            const bValue = (b as any)[currentSortState.column];

            if (aValue == null || bValue == null) return 0;
            if (aValue < bValue) return -1 * currentSortState.direction;
            if (aValue > bValue) return 1 * currentSortState.direction;
            return 0;
        });

        // Update the specific category with sorted items
        return { ...list, [item_type]: itemsCopy };
    });
}

export async function runJob(job: Job) {
    const params = getRequestParams();
    if (params !== null) {
        await api.jobsStartCreate(job.id, job, params).then(() => {
            newToast(`Started job ${job.id}`, "green");

        }).catch((res) => {
            for (let field in res.error) {
                newToast(`Failed to run job: ${res.error[field]}`, 'red');
            }
        });
    }
}
export async function refreshNode(node: Node) {
    const params = getRequestParams();
    if (params !== null) {
        await api.nodesRefreshCreate({ node_id: node.id }, params).then(() => {
            newToast(`Started job ${node.id}`, "green");

        }).catch((res) => {
            for (let field in res.error) {
                newToast(`Failed to run job: ${res.error[field]}`, 'red');
            }
        });
    }
}

export async function deleteItem<T extends ItemTypeString>(itemType: T, id: number): Promise<void> {
    // Determine which API call to use based on the itemType
    const apiCall = (api as any)[`${itemType}Destroy`];
    if (!apiCall) {
        newToast(`API call for ${itemType} does not exist.`, "red");
        return;
    }
    const params = getRequestParams();
    if (params !== null) {
        await apiCall(id, params).then(() => {
            itemlist.update(list => {
                const updatedList = list[itemType].filter(item => item.id !== id);
                return { ...list, [itemType]: updatedList };
            });
        }).catch((res: any) => {
            newToast(`Failed to delete ${itemType.slice(0, -1)} ${id}`, "red");
            for (let field in res.error) {
                newToast(`s ${res.error[field]}`, 'red');
            }
        });
    }
}


export async function deleteSelectedItems(item_type: 'jobs' | 'nodes' | 'gpus') {
    const itemList = get(itemlist)[item_type];
    const selectedItemIds = get(selectedItems)[item_type];

    for (const item of itemList) {
        if (item.id && selectedItemIds.includes(item.id)) {
            await deleteItem(item_type, item.id); // Assuming deleteItem accepts item_type and id

            // Update selectedItems to remove the deleted item's id
            selectedItems.update(current => {
                const updatedSelectedIds = current[item_type].filter(id => id !== item.id);
                return { ...current, [item_type]: updatedSelectedIds };
            });
        }
    }
}
