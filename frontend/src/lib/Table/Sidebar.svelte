<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import type { ItemTypeString } from '$stores/Tables';
	import { AngleLeftOutline, AngleRightOutline } from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import { sidebarIsOpen } from '$stores/Other';
	import { headers, shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { formatString } from '$lib/Utils';

	export let item_type: ItemTypeString;

	onMount(() => {
		$sidebarIsOpen = JSON.parse(localStorage.getItem('sidebarIsOpen') || 'true');
		const localStorageShownColumns = localStorage.getItem('shownColumns');
		if (localStorageShownColumns) {
			$shownColumns = JSON.parse(localStorageShownColumns);
		}
	});

	function onCheck() {
		localStorage.setItem('shownColumns', JSON.stringify($shownColumns));
	}

	function toggleSidebar() {
		$sidebarIsOpen = !$sidebarIsOpen;
		localStorage.setItem('sidebarIsOpen', JSON.stringify($sidebarIsOpen));
	}
</script>

{#if $sidebarIsOpen}
	<Sidebar class="h-full">
		<SidebarWrapper class="!bg-gray-800 !rounded-none h-full">
			<div class="pl-3">
				<Heading tag="h6" class="pb-2">Filter Columns</Heading>
				{#each $headers[item_type] as column}
					<Checkbox
						class="hover:bg-gray-700 ml-4"
						bind:group={$shownColumns[item_type]}
						on:change={onCheck}
						value={column}>{formatString(column)}</Checkbox
					>
				{/each}
			</div>
		</SidebarWrapper>
	</Sidebar>
{/if}

<button class="bg-gray-800 hover:bg-gray-700" on:click={toggleSidebar}>
	{#if $sidebarIsOpen}
		<AngleLeftOutline />
	{:else}
		<AngleRightOutline />
	{/if}
</button>
