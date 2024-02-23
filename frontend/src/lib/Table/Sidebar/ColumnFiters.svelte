<script lang="ts">
	import { headers, shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { formatString } from '$lib/Utils';
	import type { ItemTypeString } from '$stores/Tables';

	export let item_type: ItemTypeString;
	onMount(() => {
		const localStorageShownColumns = localStorage.getItem('shownColumns');
		if (localStorageShownColumns) {
			$shownColumns = JSON.parse(localStorageShownColumns);
		}
	});
	function onChange() {
		localStorage.setItem('shownColumns', JSON.stringify($shownColumns));
	}
</script>

<Heading tag="h3">Columns</Heading>
{#each $headers[item_type] as column}
	<Checkbox bind:group={$shownColumns[item_type]} on:change={onChange} value={column}
		>{formatString(column)}</Checkbox
	>
{/each}
