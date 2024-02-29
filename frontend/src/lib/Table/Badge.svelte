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

	function getColorFromValue(item: ItemType, property: string): ColorType {
		let value = (item as any)[property];
		if (['slow', 'interrupted'].includes(value.toLowerCase())) return 'red';
		return 'dark';
	}
	function capitalize(item: ItemType, property: string) {
		let str = (item as any)[property];
		if (!str) return '';
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
	}
</script>

<Badge
	border
	class="font-extrabold !bg-gray-800 !border-gray-700"
	large
	color={getColorFromValue(item, header)}>{capitalize(item, header)}</Badge
>
