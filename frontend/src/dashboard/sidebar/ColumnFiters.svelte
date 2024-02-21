<script lang="ts">
	import { shownColumns } from '$stores/store';
	import { Checkbox, Heading } from 'flowbite-svelte';
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
	function formatString(input: string): string {
		const replacedString = input.replace(/_/g, ' ');
		const capitalizedString = replacedString.charAt(0).toUpperCase() + replacedString.slice(1);

		return capitalizedString;
	}

	onMount(() => {
		const savedColumns = localStorage.getItem('shownColumns');
		if (savedColumns) {
			$shownColumns = JSON.parse(savedColumns);
		} else {
			$shownColumns = ['id', 'path', 'status'];
		}
	});
</script>

<Heading tag="h3">Columns</Heading>
{#each allColumns as column}
	<Checkbox bind:group={$shownColumns} on:change={saveToCache} value={column}
		>{formatString(column)}</Checkbox
	>
{/each}
