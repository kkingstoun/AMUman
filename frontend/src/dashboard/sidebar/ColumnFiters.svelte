<script lang="ts">
	import { shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import type { Job } from '$api/Api';
	import { formatString } from '$lib/Utils';

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
		'output',
		'error',
		'flags',
		'node',
		'gpu'
	];

	onMount(() => {
		const savedColumns = localStorage.getItem('shownColumns');
		if (savedColumns) {
			$shownColumns['jobs'] = JSON.parse(savedColumns);
		} else {
			$shownColumns['jobs'] = ['id', 'path', 'status'];
		}
	});
</script>

<Heading tag="h3">Columns</Heading>
{#each allColumns as column}
	<Checkbox bind:group={$shownColumns['jobs']} on:change={saveToCache} value={column}
		>{formatString(column)}</Checkbox
	>
{/each}
