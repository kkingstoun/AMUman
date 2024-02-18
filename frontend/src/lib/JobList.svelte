<script lang="ts">
	import type { Job } from '../Api';
	import { onMount } from 'svelte';
	import { api } from '../store';
	import { errorToast } from './Toast';
	import Status from './Status.svelte';
	import moment from 'moment';
	import Priority from './Priority.svelte';

	let activeJobs: Job[] = [];
	type TableHeader = {
		key: keyof Job;
		label: string;
		format: 'datetime' | '';
	};
	let tableHeaders: TableHeader[] = [
		{ key: 'id', label: 'ID', format: '' },
		{ key: 'path', label: 'Path', format: '' },
		// { key: 'port', label: 'Port', format: '' },
		{ key: 'submit_time', label: 'Submit Time', format: 'datetime' },
		{ key: 'start_time', label: 'Start Time', format: 'datetime' },
		{ key: 'end_time', label: 'End Time', format: 'datetime' },
		{ key: 'error_time', label: 'Error Time', format: 'datetime' },
		{ key: 'priority', label: 'Priority', format: '' },
		// { key: 'estimated_simulation_time', label: 'Estimated Duration', format: '' },
		{ key: 'status', label: 'Status', format: '' },
		{ key: 'output', label: 'Output', format: '' },
		// { key: 'error', label: 'Error', format: '' },
		// { key: 'flags', label: 'Flags', format: '' },
		{ key: 'node', label: 'Node', format: '' }
	];
	interface SortState {
		column: keyof Job;
		direction: 1 | -1; // 1 for ascending, -1 for descending
	}
	let sortState: SortState = {
		column: 'id',
		direction: 1
	};
	onMount(async () => {
		api
			.jobsList()
			.then((res) => {
				activeJobs = res.data;
				sortJobs();
			})
			.catch((err) => {
				console.error(err);
				errorToast('Failed to fetch jobs');
			});
	});
	$: sortState, sortJobs();

	function sortJobs(): void {
		activeJobs.sort((a, b) => {
			const aValue = a[sortState.column];
			const bValue = b[sortState.column];

			if (aValue == null || bValue == null) return 0; // Handle null or undefined values

			if (aValue < bValue) return -1 * sortState.direction;
			if (aValue > bValue) return 1 * sortState.direction;
			return 0;
		});
		activeJobs = activeJobs; // Trigger reactivity
	}

	const formatValue = (job: Job, key: string, format?: string) => {
		const value = job[key as keyof Job];
		if (format === 'datetime') {
			if (!value) return '-';
			return moment(value).fromNow();
		}
		return value;
	};
	function updateSortState(column: keyof Job): void {
		if (sortState.column === column) {
			sortState.direction *= -1; // Toggle direction
		} else {
			sortState.column = column;
			sortState.direction = 1; // Default to ascending for a new column
		}
	}
</script>

<section>
	<div class="mt-8 rounded-2xl" style="background: rgb(146 151 179 / 13%)">
		<div class="container mx-auto">
			<div class="max-w-full overflow-x-auto rounded-lg">
				<table class="w-full leading-normal text-white">
					<thead>
						<tr>
							{#each tableHeaders as { key, label }}
								<th
									class="px-5 py-3 border-b border-gray-200 text-left text-sm uppercase font-normal cursor-pointer"
									on:click={() => updateSortState(key)}
								>
									{label}
									{sortState.column === key ? (sortState.direction === 1 ? ' 🔼' : ' 🔽') : ''}
								</th>
							{/each}
						</tr>
					</thead>
					<tbody>
						{#each activeJobs as job}
							<tr class="hover:bg-gray-700">
								{#each tableHeaders as { key, format }}
									<td class="px-5 py-5 border-b border-gray-200 text-sm">
										<p class="whitespace-no-wrap">
											{#if key === 'status'}
												<Status status={job.status} />
											{:else if key === 'priority'}
												<Priority priority={job.priority} />
											{:else}
												{formatValue(job, key, format)}
											{/if}
										</p>
									</td>
								{/each}
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</section>
