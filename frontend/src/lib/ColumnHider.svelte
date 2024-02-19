<script lang="ts">
	import { shownColumns, allColumns } from '../store';
	import { Dropdown, Checkbox, Button } from 'flowbite-svelte';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	function saveToCache() {
		localStorage.setItem('shownColumns', JSON.stringify($shownColumns));
	}
	onMount(() => {
		const savedColumns = localStorage.getItem('shownColumns');
		if (savedColumns) {
			$shownColumns = JSON.parse(savedColumns);
		}
	});
</script>

<Button class="font-extrabold">
	Select Columns<ChevronDownSolid class="w-3 h-3 ms-2 text-white" />
</Button>
<Dropdown class="w-54 p-3 space-y-3 text-sm">
	{#each $allColumns as column}
		<Checkbox bind:group={$shownColumns} on:change={saveToCache} value={column}>{column}</Checkbox>
	{/each}
</Dropdown>
