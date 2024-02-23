<script lang="ts">
	import { Badge } from 'flowbite-svelte';
	import type { ItemType } from '$stores/Tables';

	type ColorType =
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

	export let item: ItemType;
	export let header: string;

	export function getColorFromValue(item: ItemType, property: string): ColorType {
		let value = (item as any)[property];
		if (['slow', 'interrupted'].includes(value.toLowerCase())) return 'red';
		if (['normal', 'low', 'waiting'].includes(value.toLowerCase())) return 'yellow';
		if (['warning', 'paused'].includes(value.toLowerCase())) return 'yellow';
		if (['warning', 'paused'].includes(value.toLowerCase())) return 'yellow';
		return 'green';
	}
	export function capitalize(item: ItemType, property: string) {
		let str = (item as any)[property];
		if (!str) return '';
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
	}
</script>

<Badge class="font-extrabold" large color={getColorFromValue(item, header)}
	>{capitalize(item, header)}</Badge
>
