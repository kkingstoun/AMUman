<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import ColumnFiters from './ColumnFiters.svelte';
	import type { ItemTypeString } from '$stores/Tables';
	import { AngleLeftOutline, AngleRightOutline } from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import { sidebarIsOpen } from '$stores/Other';

	export let item_type: ItemTypeString;

	onMount(() => {
		$sidebarIsOpen = JSON.parse(localStorage.getItem('sidebarIsOpen') || 'true');
	});
	function onClick() {
		$sidebarIsOpen = !$sidebarIsOpen;
		localStorage.setItem('sidebarIsOpen', JSON.stringify($sidebarIsOpen));
	}
</script>

{#if $sidebarIsOpen}
	<Sidebar class="h-full">
		<SidebarWrapper class="!bg-gray-800 !rounded-none h-full">
			<ColumnFiters {item_type} />
		</SidebarWrapper>
	</Sidebar>
{/if}

<button class="bg-gray-800 hover:bg-gray-600" on:click={onClick}>
	{#if $sidebarIsOpen}
		<AngleLeftOutline />
	{:else}
		<AngleRightOutline />
	{/if}
</button>
