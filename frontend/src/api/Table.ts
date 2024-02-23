import { sortStates, itemlist, lastFetchTime, selectedItems } from '$stores/Tables';
import { api } from '$stores/Auth';
import { get } from 'svelte/store';
import { errorToast } from '$lib/Toast';
import { getRequestParams } from './Auth';

export async function fetchItems(item_type: 'jobs' | 'nodes' | 'gpus') {
    try {
        let response: any;
        if (item_type === 'jobs') {
            response = await api.jobsList(getRequestParams());
        } else if (item_type === 'nodes') {
            response = await api.nodesList(getRequestParams());
        } else if (item_type === 'gpus') {
            response = await api.gpusList(getRequestParams());
        } else {
            throw new Error('Invalid item type');
        }

        itemlist.update(current => {
            // Update the specific part of the store based on item_type
            current[item_type] = response.data;
            return current;
        });

        sortItems(item_type); // Assuming this function exists and is correctly implemented
        lastFetchTime.set(Date.now());
    } catch (err) {
        console.error(err);
        errorToast(`Failed to fetch ${item_type}`);
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

export async function deleteItem(item_type: 'jobs' | 'nodes' | 'gpus', id: number) {
    try {
        // Dynamically call the correct API method based on item_type
        if (item_type === 'jobs') {
            await api.jobsDestroy(id, getRequestParams());
        } else if (item_type === 'nodes') {
            await api.nodesDestroy(id, getRequestParams()); // Assuming similar API exists
        } else if (item_type === 'gpus') {
            await api.gpusDestroy(id, getRequestParams()); // Assuming similar API exists
        }

        // Update the store by removing the deleted item
        itemlist.update(list => {
            const updatedList = list[item_type].filter(item => item.id !== id);
            return { ...list, [item_type]: updatedList };
        });
    } catch (err) {
        console.error(err);
        errorToast(`Failed to delete ${item_type.slice(0, -1)} ${id}`); // Adjust the message dynamically
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

    // Since deleteItem updates itemlist internally, no need to update itemlist here
}