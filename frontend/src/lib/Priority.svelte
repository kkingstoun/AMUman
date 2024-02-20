<script lang="ts">
	import { PriorityEnum } from '../api/Api';

	export let priority: PriorityEnum | undefined;

	// Define a mapping from job priorityes to Tailwind CSS color classes
	const priorityColorMap: Record<PriorityEnum, string> = {
		[PriorityEnum.LOW]: 'bg-green-200',
		[PriorityEnum.NORMAL]: 'bg-red-500',
		[PriorityEnum.HIGH]: 'bg-yellow-500'
	};

	// Function to get color based on priority
	function getColorBypriority(priority: PriorityEnum | undefined): string {
		if (!priority) return 'bg-gray-200'; // Default color if priority is not found
		return priorityColorMap[priority];
	}

	$: color = getColorBypriority(priority);
</script>

<span class="relative inline-block px-3 py-1 font-semibold leading-tight">
	<span aria-hidden="true" class={`absolute inset-0 ${color} opacity-50 rounded-full`} />
	<span class="relative">{priority}</span>
</span>
