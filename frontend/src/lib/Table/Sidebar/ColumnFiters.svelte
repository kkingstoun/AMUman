<script lang="ts">
	import { headers, shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { formatString } from '$lib/Utils';
	import type { ItemTypeString } from '$stores/Tables';

	export let item_type: ItemTypeString;
	function saveToCache() {
		localStorage.setItem('shownColumns', JSON.stringify($shownColumns));
	}
	onMount(() => {
		const localStorageShownColumns = localStorage.getItem('shownColumns');
		if (localStorageShownColumns) {
			$shownColumns[item_type] = JSON.parse(localStorageShownColumns);
		}
	});
</script>

<Heading tag="h3">Columns</Heading>
{#each $headers[item_type] as column}
	<Checkbox bind:group={$shownColumns['jobs']} on:change={saveToCache} value={column}
		>{formatString(column)}</Checkbox
	>
{/each}
