<script lang="ts">
	import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
	import { PriorityEnum } from '$api/OpenApi';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';

	let dropdownOpen = false;
	let selectedStatus: string = 'All';
</script>

<Button outline color="dark" size="xs" class="w-full"
	>{selectedStatus}<ChevronDownSolid class="w-3 h-3 ms-2 text-white" /></Button
>
<Dropdown class="w-48 overflow-y-auto py-1 h-48" bind:open={dropdownOpen}>
	<DropdownItem
		class="flex items-center text-base font-semibold gap-2"
		on:click={() => {
			selectedStatus = 'All';
			dropdownOpen = false;
		}}
	>
		All
	</DropdownItem>
	{#each Object.values(PriorityEnum) as status}
		<DropdownItem
			class="flex items-center text-base font-semibold gap-2"
			on:click={() => {
				selectedStatus = status;
				dropdownOpen = false;
			}}
		>
			{status}
		</DropdownItem>
	{/each}
</Dropdown>
