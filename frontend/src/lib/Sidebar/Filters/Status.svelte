<script lang="ts">
	import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
	import { JobStatusEnum } from '$api/OpenApi';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';
	import { jobsFilters } from '$stores/Sidebar';
	import { fetchJobs } from '$api/Table';

	let dropdownOpen = false;
</script>

<Button outline color="dark" size="xs" class="w-full"
	>{$jobsFilters.status || 'All'}<ChevronDownSolid class="w-3 h-3 ms-2 text-white" /></Button
>
<Dropdown class="w-48 overflow-y-auto py-1 h-48" bind:open={dropdownOpen}>
	<DropdownItem
		class="flex items-center text-base font-semibold gap-2"
		on:click={() => {
			$jobsFilters.status = undefined;
			dropdownOpen = false;
			fetchJobs();
		}}
	>
		All
	</DropdownItem>
	{#each Object.values(JobStatusEnum) as status}
		<DropdownItem
			class="flex items-center text-base font-semibold gap-2"
			on:click={() => {
				$jobsFilters.status = status;
				dropdownOpen = false;
				fetchJobs();
			}}
		>
			{status}
		</DropdownItem>
	{/each}
</Dropdown>
