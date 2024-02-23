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

	import { fetchItems, sortItems } from '$api/Table';
	import {
		shownColumns,
		refreshInterval,
		itemlist,
		sortStates,
		lastFetchTime,
		selectedItems,
		timeSinceLastFetch,
		headers,
		type ItemType
	} from '$stores/Tables';
	import Status from './Status.svelte';
	import Priority from './Priority.svelte';
	import OutputDrawer from './OutputDrawer.svelte';
	import DeleteItem from './DeleteItem.svelte';
	import DeleteSelectedItems from './DeleteSelectedItems.svelte';
	import RunJob from './RunJob.svelte';
	import { formatValue } from '../Utils';
	import type { ItemTypeString } from '$stores/Tables';
	import type { Job } from '$api/Api';

	export let item_type: ItemTypeString;

	let refreshLastFetchTimeInterval: ReturnType<typeof setInterval>;
	function refreshTimeSinceLastFetch() {
		$timeSinceLastFetch = moment($lastFetchTime).fromNow();
	}

	let refreshJobsInterval: ReturnType<typeof setInterval>;
	onMount(async () => {
		await fetchItems(item_type);
		// This only refreshes the text that shows the time since last fetch
		refreshTimeSinceLastFetch();
		refreshLastFetchTimeInterval = setInterval(refreshTimeSinceLastFetch, 1000 * 60);

		const localStorageSortState = localStorage.getItem('sortState');
		if (localStorageSortState) {
			$sortStates[item_type] = JSON.parse(localStorageSortState);
		}

		sortItems(item_type);
		// This refreshes the jobs every minute
		refreshJobsInterval = setInterval(() => {
			fetchItems(item_type);
		}, $refreshInterval); // Refresh every minute
	});

	onDestroy(() => {
		clearInterval(refreshLastFetchTimeInterval);
		clearInterval(refreshJobsInterval);
	});

	function updateSortState(column: string): void {
		if ($sortStates[item_type].column === column) {
			$sortStates[item_type].direction *= -1; // Toggle direction
		} else {
			$sortStates[item_type].column = column as keyof ItemType;
			$sortStates[item_type].direction = 1; // Default to ascending for a new column
		}
		localStorage.setItem('sortState', JSON.stringify($sortStates));
		sortItems(item_type);
	}

	function allCheckBoxes(event: Event): void {
		if (event.target instanceof HTMLInputElement) {
			if (event.target.checked) {
				$selectedItems[item_type] = $itemlist[item_type].map((job) => job.id);
			} else {
				$selectedItems[item_type] = [];
			}
		}
	}
	function columnIsShown(header: string): boolean {
		return $shownColumns[item_type].includes(header as keyof ItemType);
	}
	function isJob(item: any): item is Job {
		return item_type === 'jobs' && 'priority' in item;
	}
</script>

<Table shadow hoverable={true}>
	<TableHead>
		<TableHeadCell class="flex items-center !p-4 space-x-2">
			<Checkbox on:change={(event) => allCheckBoxes(event)} />
			{#if $selectedItems[item_type].length > 0}
				<DeleteSelectedItems {item_type} />
			{/if}
		</TableHeadCell>
		{#each $headers[item_type] as header}
			{#if columnIsShown(header)}
				<TableHeadCell on:click={() => updateSortState(header)}>
					{header}
				</TableHeadCell>
			{/if}
		{/each}
		{#if item_type === 'jobs'}
			<TableHeadCell>Output</TableHeadCell>
			<TableHeadCell>Delete</TableHeadCell>
		{/if}
		<TableHeadCell>Run</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each $itemlist[item_type] as item}
			<TableBodyRow>
				<TableBodyCell class="!p-4">
					<Checkbox bind:group={$selectedItems[item_type]} value={item.id} />
				</TableBodyCell>
				{#each $headers[item_type] as header}
					{#if columnIsShown(header)}
						<TableBodyCell class="hover:underline">
							{#if isJob(item) && header === 'status'}
								<Status status={item.status} />
							{:else if isJob(item) && header === 'priority'}
								<Priority priority={item.priority} />
							{:else}
								{formatValue(item, header)}
							{/if}
						</TableBodyCell>
					{/if}
				{/each}
				{#if isJob(item)}
					<TableBodyCell>
						<OutputDrawer job={item} />
					</TableBodyCell>
					<TableBodyCell>
						<RunJob job={item} />
					</TableBodyCell>
				{/if}
				<TableBodyCell>
					<DeleteItem {item} {item_type} />
				</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</Table>
