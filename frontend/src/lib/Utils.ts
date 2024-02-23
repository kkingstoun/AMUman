import type { ItemType } from '$stores/Tables';
import moment from 'moment';

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