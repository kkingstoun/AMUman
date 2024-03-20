import type { ItemType } from '$stores/Tables';
import type { Job, Gpu, Node } from '$api/OpenApi';
import { DateTime } from 'luxon';
import { get } from 'svelte/store';
import { shownColumns, headers } from '$stores/Tables';
import { type KeyLists } from '$stores/Tables'; // Import the KeyLists type from the appropriate location

export function formatString(input: string): string {
    const replacedString = input.replace(/_/g, ' ');
    const capitalizedString = replacedString.charAt(0).toUpperCase() + replacedString.slice(1);

    return capitalizedString;
}

export function formatValue(
    item: ItemType,
    key: string,
): string | number | null | undefined {
    const value = item[key as keyof ItemType];
    return value;
}


export function isJob(item: ItemType): item is Job {
    return 'path' in item;
}
export function isNode(item: ItemType): item is Node {
    return 'number_of_gpus' in item;
}
export function isGpu(item: ItemType): item is Gpu {
    return 'speed' in item;
}
export function formatDateTime(dateString?: string | null): string {
    if (!dateString) return '-';
    dateString = DateTime.fromISO(dateString).setLocale('en-GB').toRelative();
    if (dateString) return dateString;
    else return '-';
};

export function getPropertyValue(item: ItemType, property: string): string | undefined {
    return (item as any)[property];
}


export function orderShownColumnsLikeHeaders(): void {
    const currentHeaders = get(headers);

    shownColumns.update(currentShownColumns => {
        // Iterate over each key in currentShownColumns and reorder according to currentHeaders
        Object.keys(currentShownColumns).forEach(key => {
            if (currentHeaders[key as keyof KeyLists]) { // Add type assertion to keyof KeyLists
                currentShownColumns[key as keyof KeyLists] = (currentShownColumns[key as keyof KeyLists] as (keyof Node)[] & (keyof Job)[] & (keyof Gpu)[]).sort((a, b) => {
                    // Use the order in currentHeaders[key] to sort currentShownColumns[key]
                    return (currentHeaders[key as keyof KeyLists] as ("id" | "status")[])
                        .indexOf(a as "id" | "status") - (currentHeaders[key as keyof KeyLists] as ("id" | "status")[]).indexOf(b as "id" | "status");
                });
            }
        });

        return currentShownColumns; // Return the newly ordered shownColumns
    });
}