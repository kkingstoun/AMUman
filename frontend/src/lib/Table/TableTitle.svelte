<script lang="ts">
	import { lastFetchTime, refreshLastFetchTimeInterval } from '$stores/Tables';
	import { formatString } from '$lib/Utils';
	import type { ItemTypeString } from '$stores/Tables';
	import { RefreshOutline } from 'flowbite-svelte-icons';
	import { fetchItems } from '$api/Table';
	import { fly } from 'svelte/transition';
	import { isRefreshing } from '$stores/Tables';
	import { onMount } from 'svelte';
	export let item_type: ItemTypeString;

	async function handleRefresh() {
		$isRefreshing = true;
		await fetchItems(item_type);
		setTimeout(() => {
			$isRefreshing = false;
		}, 1000);
	}
	let dateString: string = 'Never';

	function formatDateTime(): void {
		if ($lastFetchTime) {
			let dateStringOrNull = $lastFetchTime.toRelative();
			if (dateStringOrNull) dateString = dateStringOrNull;
			else dateString = '-';
		}
	}
	onMount(() => {
		formatDateTime();
		$refreshLastFetchTimeInterval = setInterval(formatDateTime, 1000 * 1);
	});
</script>

<div class="flex items-center justify-between pb-3 pl-4">
	<h2 class="text-4xl">{formatString(item_type)}</h2>
	{#if !$isRefreshing}
		<div
			class="ml-7 text-gray-500"
			in:fly={{ y: -100, duration: 500 }}
			out:fly={{ y: 100, duration: 500 }}
		>
			Last refresh: {dateString}
		</div>
	{/if}
	<RefreshOutline
		on:click={handleRefresh}
		size="xl"
		class="mr-3 text-gray-500 right {$isRefreshing ? 'animate-spin' : ''}"
	/>
</div>
