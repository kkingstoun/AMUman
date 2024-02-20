<script lang="ts">
	import { shownColumns } from '$stores/store';
	import { Dropdown, Checkbox, NavLi } from 'flowbite-svelte';
	import { ChevronDownOutline } from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import type { Job } from '$api/Api';

	function saveToCache() {
		localStorage.setItem('shownColumns', JSON.stringify($shownColumns));
	}
	let allColumns: (keyof Job)[] = [
		'id',
		'path',
		'port',
		'submit_time',
		'start_time',
		'end_time',
		'error_time',
		'priority',
		'estimated_simulation_time',
		'status',
		'gpu_partition',
		'assigned_gpu_id',
		'output',
		'error',
		'flags',
		'node',
		'gpu'
	];
	onMount(() => {
		const savedColumns = localStorage.getItem('shownColumns');
		if (savedColumns) {
			$shownColumns = JSON.parse(savedColumns);
		} else {
			$shownColumns = ['id', 'path', 'status'];
		}
	});
</script>

<NavLi class="cursor-pointer">
	Column filters<ChevronDownOutline class="w-3 h-3 ms-2 text-primary-800 dark:text-white inline" />
</NavLi>

<Dropdown class="w-54 p-3 space-y-3 text-sm">
	{#each allColumns as column}
		<Checkbox bind:group={$shownColumns} on:change={saveToCache} value={column}>{column}</Checkbox>
	{/each}
</Dropdown>
