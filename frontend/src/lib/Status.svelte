<script lang="ts">
	import { JobStatusEnum } from '../api/Api';

	export let status: JobStatusEnum | undefined;

	// Define a mapping from job statuses to Tailwind CSS color classes
	const statusColorMap: Record<JobStatusEnum, string> = {
		[JobStatusEnum.WAITING]: 'bg-blue-500',
		[JobStatusEnum.PENDING]: 'bg-blue-500',
		[JobStatusEnum.RUNNING]: 'bg-green-500',
		[JobStatusEnum.INTERRUPTED]: 'bg-red-500',
		[JobStatusEnum.FINISHED]: 'bg-green-700'
	};

	// Function to get color based on status
	function getColorByStatus(status: JobStatusEnum | undefined): string {
		if (!status) return 'bg-gray-200'; // Default color if status is not found
		return statusColorMap[status];
	}

	$: color = getColorByStatus(status);
</script>

<span class="relative inline-block px-3 py-1 font-semibold leading-tight">
	<span aria-hidden="true" class={`absolute inset-0 ${color} opacity-50 rounded-full`} />
	<span class="relative">{status}</span>
</span>
