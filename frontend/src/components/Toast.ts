import { toast } from '@zerodevx/svelte-toast';

export function successToast(message: string): void {
	toast.push(message, {
		theme: {
			'--toastColor': 'mintcream',
			'--toastBackground': 'rgba(72,187,120,0.9)',
			'--toastBarBackground': '#2F855A'
		}
	});
}

export function errorToast(message: string): void {
	toast.push(message, {
		theme: {
			'--toastColor': 'mintcream',
			'--toastBackground': 'rgba(255,99,71,0.9)',
			'--toastBarBackground': '#A93226'
		}
	});
}