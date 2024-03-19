<script lang="ts">
	import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
	import { authenticatedApiCall } from '$api/Auth';
	import { api } from '$stores/Auth';
	import { newToast } from '$lib/Utils';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';

	let users: string[] = [];
	async function getUsers() {
		await authenticatedApiCall(api.usersList)
			.then((res) => {
				users = [];
				res.data.forEach((user) => {
					users.push(user.auth.username);
				});
			})
			.catch((res) => {
				for (let field in res.error) {
					newToast(res.error[field], 'red');
				}
			});
	}
	let dropdownOpen = false;
	let selectedUser: string = 'All';
</script>

<Button outline color="dark" size="xs" on:click={getUsers} class="w-full"
	>{selectedUser}<ChevronDownSolid class="w-3 h-3 ms-2 text-white dark:text-white" /></Button
>
<Dropdown class="overflow-y-auto py-1 h-48" bind:open={dropdownOpen}>
	<DropdownItem
		class="flex items-center text-base font-semibold gap-2"
		on:click={() => {
			selectedUser = 'All';
			dropdownOpen = false;
		}}
	>
		All
	</DropdownItem>
	{#each users as user}
		<DropdownItem
			class="flex items-center text-base font-semibold gap-2"
			on:click={() => {
				selectedUser = user;
				dropdownOpen = false;
			}}
		>
			{user}
		</DropdownItem>
	{/each}
</Dropdown>
