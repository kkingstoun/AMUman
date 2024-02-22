<script lang="ts">
	import { PriorityEnum } from '$api/Api';
	import { Badge } from 'flowbite-svelte';

	export let priority: PriorityEnum | undefined;
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

	// Define a mapping from job priorityes to Tailwind CSS color classes
	const priorityColorMap: Record<PriorityEnum, ColorType> = {
		[PriorityEnum.LOW]: 'yellow',
		[PriorityEnum.NORMAL]: 'green',
		[PriorityEnum.HIGH]: 'primary'
	};

	function capitalize(str: string | undefined) {
		if (!str) return '';
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
	}

	function getColorByPriority(priority: PriorityEnum | undefined): ColorType {
		if (!priority) return 'primary'; // Default color if priority is not found
		return priorityColorMap[priority];
	}
</script>

<Badge class="font-extrabold" large color={getColorByPriority(priority)}
	>{capitalize(priority)}</Badge
>
