import { sortStates, itemlist, lastFetchTime, selectedItems, type ItemTypeString, type ItemType, type ItemTypeMap } from '$stores/Tables';
import { api } from '$stores/Auth';
import { get } from 'svelte/store';
import { newToast } from '$lib/Utils';
import { authenticatedApiCall } from './Auth';
import type { Job } from './Api';
import { DateTime } from 'luxon';


export async function fetchItems<T extends ItemTypeString>(itemType: T): Promise<void> {
    // Determine which API call to use based on the itemType
    const apiCall = (api as any)[`${itemType}List`];
    if (!apiCall) {
        newToast(`API call for ${itemType} does not exist.`, "red");
        return;
    }

    await authenticatedApiCall(apiCall).then((res) => {
        itemlist.update(itemList => {
            itemList[itemType] = res.data as ItemTypeMap[T];
            return itemList;
        });
        sortItems(itemType);
        lastFetchTime.set(DateTime.now());
    }).catch((err) => {
        newToast(`Failed to fetch ${itemType}. Err: ${err}`, "red");
    });
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
    await authenticatedApiCall(api.jobsStartCreate, job.id, job).then((res) => {
        newToast(`Started job ${job.id}`, "green");

    }).catch((res) => {
        for (let field in res.error) {
            newToast(`s ${res.error[field]}`, 'red');
        }
    });
}

export async function deleteItem<T extends ItemTypeString>(itemType: T, id: number): Promise<void> {
    // Determine which API call to use based on the itemType
    const apiCall = (api as any)[`${itemType}Destroy`];
    if (!apiCall) {
        newToast(`API call for ${itemType} does not exist.`, "red");
        return;
    }

    await authenticatedApiCall(apiCall, id).then((res) => {
        itemlist.update(list => {
            const updatedList = list[itemType].filter(item => item.id !== id);
            return { ...list, [itemType]: updatedList };
        });
    }).catch((res) => {
        newToast(`Failed to delete ${itemType.slice(0, -1)} ${id}`, "red");
        for (let field in res.error) {
            newToast(`s ${res.error[field]}`, 'red');
        }
    });
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