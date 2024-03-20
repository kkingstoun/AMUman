import { writable } from 'svelte/store';

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
    id: number;
    message: string;
    color: ToastColor;
};

export const toasts = writable<Toast[]>([]);

export function newToast(message: string, color: ToastColor): void {
    const id = Date.now(); // Using a timestamp as a simple unique ID
    toasts.update((t) => {
        const toast = { message, color, id };
        return [...t, toast];
    });

    setTimeout(() => {
        toasts.update((t) => {
            return t.filter(toast => toast.id !== id); // Remove the toast by ID
        });
    }, 2000);
}