<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import moment from 'moment';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Checkbox
	} from 'flowbite-svelte';

	import type { Job } from '$api/Api';
	import { fetchJobs, sortJobs } from '$api/jobs';
	import { shownColumns, refreshInterval, activeJobs, sortState } from '$stores/store';
	import Status from './Status.svelte';
	import Priority from './Priority.svelte';
	import OutputDrawer from './OutputDrawer.svelte';
	import DeleteJob from './DeleteJob.svelte';
	import RunJob from './RunJob.svelte';

	type TableHeader = {
		key: keyof Job;
		label: string;
		format: 'datetime' | '';
	};

	let tableHeaders: TableHeader[] = [
		{ key: 'id', label: 'ID', format: '' },
		{ key: 'path', label: 'Path', format: '' },
		{ key: 'port', label: 'Port', format: '' },
		{ key: 'submit_time', label: 'Submit Time', format: 'datetime' },
		{ key: 'start_time', label: 'Start Time', format: 'datetime' },
		{ key: 'end_time', label: 'End Time', format: 'datetime' },
		{ key: 'error_time', label: 'Error Time', format: 'datetime' },
		{ key: 'priority', label: 'Priority', format: '' },
		{ key: 'estimated_simulation_time', label: 'Estimated Duration', format: '' },
		{ key: 'status', label: 'Status', format: '' },
		{ key: 'output', label: 'Output', format: '' },
		{ key: 'error', label: 'Error', format: '' },
		{ key: 'flags', label: 'Flags', format: '' },
		{ key: 'node', label: 'Node', format: '' }
	];

	let intervalId: ReturnType<typeof setInterval>;
	onMount(async () => {
		await fetchJobs();
		sortJobs();
		intervalId = setInterval(fetchJobs, $refreshInterval); // Refresh every minute
	});

	onDestroy(() => {
		clearInterval(intervalId); // Clear the interval when the component is destroyed
	});

	function formatValue(job: Job, key: string, format?: string): string | number | null | undefined {
		const value = job[key as keyof Job];
		if (format === 'datetime') {
			if (!value) return '-';
			return moment(value).fromNow();
		}
		return value;
	}
	function updateSortState(column: keyof Job): void {
		if ($sortState.column === column) {
			$sortState.direction *= -1; // Toggle direction
		} else {
			$sortState.column = column;
			$sortState.direction = 1; // Default to ascending for a new column
		}
		sortJobs();
	}
</script>

<Table shadow hoverable={true}>
	<TableHead>
		<TableHeadCell class="!p-4">
			<Checkbox />
		</TableHeadCell>
		{#each tableHeaders as { key, label }}
			{#if $shownColumns.includes(key)}
				<TableHeadCell on:click={() => updateSortState(key)}>
					{label}
				</TableHeadCell>
			{/if}
		{/each}
		<TableHeadCell>Output</TableHeadCell>
		<TableHeadCell>Delete</TableHeadCell>
		<TableHeadCell>Run</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each $activeJobs as job}
			<TableBodyRow>
				<TableBodyCell class="!p-4">
					<Checkbox />
				</TableBodyCell>
				{#each tableHeaders as { key, format }}
					{#if $shownColumns.includes(key)}
						<TableBodyCell class="hover:underline">
							{#if key === 'status'}
								<Status status={job.status} />
							{:else if key === 'priority'}
								<Priority priority={job.priority} />
							{:else}
								{formatValue(job, key, format)}
							{/if}
						</TableBodyCell>
					{/if}
				{/each}
				<TableBodyCell>
					<OutputDrawer {job} />
				</TableBodyCell>
				<TableBodyCell>
					<DeleteJob {job} />
				</TableBodyCell>
				<TableBodyCell>
					<RunJob {job} />
				</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</Table>
