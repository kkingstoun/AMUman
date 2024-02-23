<script lang="ts">
	import { JobStatusEnum, NodesStatusEnum, GpusStatusEnum } from '$api/Api';
	import { Badge } from 'flowbite-svelte';

	export let status: JobStatusEnum | NodesStatusEnum | GpusStatusEnum | undefined;
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

	const jobsStatusColorMap: Record<JobStatusEnum, ColorType> = {
		[JobStatusEnum.WAITING]: 'yellow',
		[JobStatusEnum.PENDING]: 'yellow',
		[JobStatusEnum.RUNNING]: 'green',
		[JobStatusEnum.INTERRUPTED]: 'red',
		[JobStatusEnum.FINISHED]: 'indigo'
	};
	const nodesStatusColorMap: Record<NodesStatusEnum, ColorType> = {
		[NodesStatusEnum.WAITING]: 'yellow',
		[NodesStatusEnum.RUNNING]: 'green',
		[NodesStatusEnum.RESERVED]: 'indigo',
		[NodesStatusEnum.UNAVAILABLE]: 'red'
	};
	const gpusStatusColorMap: Record<GpusStatusEnum, ColorType> = {
		[GpusStatusEnum.Waiting]: 'yellow',
		[GpusStatusEnum.Running]: 'green',
		[GpusStatusEnum.Reserved]: 'indigo',
		[GpusStatusEnum.Unavailable]: 'red'
	};

	function capitalize(str: string | undefined) {
		if (!str) return '';
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
	}

	function getColorByStatus(
		status: JobStatusEnum | NodesStatusEnum | GpusStatusEnum | undefined
	): ColorType {
		if (!status) return 'primary'; // Default color if status is not found
		if (status in jobsStatusColorMap) return jobsStatusColorMap[status as JobStatusEnum];
		if (status in nodesStatusColorMap) return nodesStatusColorMap[status as NodesStatusEnum];
		if (status in gpusStatusColorMap) return gpusStatusColorMap[status as GpusStatusEnum];
		// return statusColorMap[status];
	}
</script>

<Badge class="font-extrabold" large color={getColorByStatus(status)}>{capitalize(status)}</Badge>
