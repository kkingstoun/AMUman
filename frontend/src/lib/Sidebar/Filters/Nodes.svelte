<script lang="ts">
	import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
	import { getRequestParams } from '$api/Auth';
	import { fetchJobs } from '$api/Table';
	import { api } from '$stores/Auth';
	import { newToast } from '$stores/Toast';
	import { jobsFilters } from '$stores/Sidebar';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';

	let nodes: number[] = [];
	let loading = false; // Loading state
	let dropdownOpen = false;

	async function getNodeNames() {
		loading = true; // Set loading to true
		const params = getRequestParams();

		if (params !== null) {
			await api
				.nodesList({}, params)
				.then((res) => {
					let data = res.data.results;
					if (data) {
						nodes = [];
						data.forEach((node) => {
							nodes.push(node.id);
						});
					}
				})
				.catch((res) => {
					for (let field in res.error) {
						newToast(`Failed to fetch nodes: ${res.error[field]}`, 'red');
					}
				})
				.then(() => {
					loading = false; // Set loading to false
				});
		}
	}
</script>

<Button outline color="dark" size="xs" on:click={getNodeNames} class="w-full">
	{$jobsFilters.node || 'All'}<ChevronDownSolid class="w-3 h-3 ms-2 text-white dark:text-white" />
</Button>

<Dropdown class="overflow-y-auto py-1 h-48" bind:open={dropdownOpen}>
	{#if !loading}
		<DropdownItem
			class="flex items-center text-base font-semibold gap-2"
			on:click={() => {
				$jobsFilters.node = undefined;
				$jobsFilters.offset = 0;
				dropdownOpen = false;
				fetchJobs();
			}}
		>
			All
		</DropdownItem>
		{#each nodes as node}
			<DropdownItem
				class="flex items-center text-base font-semibold gap-2"
				on:click={() => {
					$jobsFilters.node = node;
					dropdownOpen = false;
					$jobsFilters.offset = 0;
					fetchJobs();
				}}
			>
				{node}
			</DropdownItem>
		{/each}
	{/if}
</Dropdown>
