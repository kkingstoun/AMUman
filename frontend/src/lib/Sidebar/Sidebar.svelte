<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import type { ItemTypeString } from '$stores/Tables';
	import { AngleLeftOutline, AngleRightOutline } from 'flowbite-svelte-icons';
	import { sidebarIsOpen } from '$stores/Sidebar';
	import ItemFilters from './ItemFilters.svelte';
	import ColumnFilters from './ColumnFilters.svelte';

	export let item_type: ItemTypeString;

	function toggleSidebar() {
		$sidebarIsOpen = !$sidebarIsOpen;
	}
</script>

{#if $sidebarIsOpen}
	<Sidebar class="h-full">
		<SidebarWrapper class="!bg-gray-800 !rounded-none h-full">
			<ColumnFilters {item_type} />
			{#if item_type === 'jobs'}
				<ItemFilters {item_type} />
			{/if}
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
