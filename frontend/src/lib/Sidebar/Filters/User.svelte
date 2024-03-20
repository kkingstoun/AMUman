<script lang="ts">
	import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
	import { getRequestParams } from '$api/Auth';
	import { api } from '$stores/Auth';
	import { newToast } from '$stores/Toast';
	import { fetchJobs } from '$api/Table';
	import { jobsFilters } from '$stores/Sidebar';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';

	let users: string[] = [];
	let loading = false; // Loading state
	let dropdownOpen = false;

	async function getUserNames() {
		loading = true; // Set loading to true
		const params = getRequestParams();

		if (params !== null) {
			await api
				.usersList({}, params)
				.then((res) => {
					let data = res.data.results;
					if (data) {
						users = [];
						data.forEach((user) => {
							users.push(user.auth.username);
						});
					}
				})
				.catch((res) => {
					for (let field in res.error) {
						newToast(`Failed to fetch users: ${res.error[field]}`, 'red');
					}
				})
				.then(() => {
					loading = false; // Set loading to false
				});
		}
	}
</script>

<Button outline color="dark" size="xs" on:click={getUserNames} class="w-full">
	{$jobsFilters.user || 'All'}<ChevronDownSolid class="w-3 h-3 ms-2 text-white dark:text-white" />
</Button>

<Dropdown class="overflow-y-auto py-1 h-48" bind:open={dropdownOpen}>
	{#if !loading}
		<DropdownItem
			class="flex items-center text-base font-semibold gap-2"
			on:click={() => {
				$jobsFilters.user = undefined;
				dropdownOpen = false;
				fetchJobs();
			}}
		>
			All
		</DropdownItem>
		{#each users as user}
			<DropdownItem
				class="flex items-center text-base font-semibold gap-2"
				on:click={() => {
					$jobsFilters.user = user;
					dropdownOpen = false;
					fetchJobs();
				}}
			>
				{user}
			</DropdownItem>
		{/each}
	{/if}
</Dropdown>
