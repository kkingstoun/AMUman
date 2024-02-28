import type { ItemType } from '$stores/Tables';
import { toasts, type ToastColor } from '$stores/Other';
import moment from 'moment';
import type { Job, Gpus, Nodes } from '$api/Api';

export function formatString(input: string): string {
    const replacedString = input.replace(/_/g, ' ');
    const capitalizedString = replacedString.charAt(0).toUpperCase() + replacedString.slice(1);

    return capitalizedString;
}

export function formatValue(
    item: ItemType,
    key: string,
    format?: string
): string | number | null | undefined {
    const value = item[key as keyof ItemType];
    if (format === 'datetime') {
        if (!value) return '-';
        return moment(value).fromNow();
    }
    return value;
}

export type ColorType =
    | 'none'
    | 'red'
    | 'yellow'
    | 'green'
    | 'indigo'
    | 'purple'
    | 'pink'
    | 'blue'
    | 'dark'
    | 'primary'
    | undefined;

export function newToast(message: string, color: ToastColor): void {
    toasts.update((t) => {
        const toast = { message, color };
        return [...t, toast];
    });
    // // Remove the toast after 3 seconds
    // setTimeout(() => {
    //     toasts.update((t) => {
    //         return t.slice(1);
    //     });
    // }, 3000);

}

export function formatDate(time: string | undefined): string {
    if (!time) return '-';
    return moment(time).fromNow();
}

export function isJob(item: ItemType): item is Job {
    return 'path' in item;
}
export function isNode(item: ItemType): item is Nodes {
    return 'number_of_gpus' in item;
}
export function isGpu(item: ItemType): item is Gpus {
    return 'speed' in item;
}
export function formatDateTime(dateString?: string | null): string {
    if (!dateString) return '-';
    return (
        moment(dateString).format('YYYY-MM-DD HH:mm:ss') + ' (' + moment(dateString).fromNow() + ')'
    );
};

export function getPropertyValue(item: ItemType, property: string): string | undefined {
    return (item as any)[property];
}