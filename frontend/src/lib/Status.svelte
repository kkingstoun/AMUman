<script lang="ts">
	import { JobStatusEnum } from '../api/Api';
	import { Badge } from 'flowbite-svelte';

	export let status: JobStatusEnum | undefined;
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

	// Define a mapping from job statuses to Tailwind CSS color classes
	const statusColorMap: Record<JobStatusEnum, ColorType> = {
		[JobStatusEnum.WAITING]: 'yellow',
		[JobStatusEnum.PENDING]: 'yellow',
		[JobStatusEnum.RUNNING]: 'green',
		[JobStatusEnum.INTERRUPTED]: 'red',
		[JobStatusEnum.FINISHED]: 'indigo'
	};
	function capitalize(str: string | undefined) {
		if (!str) return '';
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
	}

	function getColorByStatus(status: JobStatusEnum | undefined): ColorType {
		if (!status) return 'primary'; // Default color if status is not found
		return statusColorMap[status];
	}

	$: color = getColorByStatus(status);
</script>

<Badge class="font-extrabold" large color={getColorByStatus(status)}>{capitalize(status)}</Badge>
