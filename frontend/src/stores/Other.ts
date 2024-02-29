import { writable } from 'svelte/store';

export const sidebarIsOpen = writable<boolean | null>(null);

export type ToastColor =
    | 'none'
    | 'red'
    | 'yellow'
    | 'green'
    | 'indigo'
    | 'purple'
    | 'blue'
    | 'primary'
    | 'gray'
    | 'orange'
    | undefined;

type Toast = {
    message: string;
    color: ToastColor;
};

export const toasts = writable<Toast[]>([]);