<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
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
		selectedItems,
		type ItemType,
		isRefreshing,
		refreshLastFetchTimeInterval,
		refreshItemsInterval
	} from '$stores/Tables';
	import Drawer from '$lib/Drawer/Layout.svelte';
	import DeleteItem from './DeleteItem.svelte';
	import DeleteSelectedItems from './DeleteSelectedItems.svelte';
	import RunJob from './RunJob.svelte';
	import { formatValue, formatString, formatDateTime, isJob, getPropertyValue } from '../Utils';
	import type { ItemTypeString } from '$stores/Tables';
	import Badge from '$lib/Table/Badge.svelte';

	export let item_type: ItemTypeString;

	onMount(async () => {
		await fetchItems(item_type);

		const localStorageSortState = localStorage.getItem('sortState');
		if (localStorageSortState) {
			$sortStates = JSON.parse(localStorageSortState);
		}

		sortItems(item_type);
		// This refreshes the jobs every minute
		$refreshItemsInterval = setInterval(() => {
			fetchItems(item_type);
			$isRefreshing = true;
			setTimeout(() => {
				$isRefreshing = false;
			}, 1000);
		}, $refreshInterval); // Refresh every minute
	});

	onDestroy(() => {
		clearInterval($refreshLastFetchTimeInterval);
		clearInterval($refreshItemsInterval);
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
</script>

<Table shadow hoverable={true}>
	<TableHead class="sticky top-0">
		<TableHeadCell class="flex items-center !p-4 space-x-2">
			<Checkbox on:change={(event) => allCheckBoxes(event)} />
			{#if $selectedItems[item_type].length > 0}
				<DeleteSelectedItems {item_type} />
			{/if}
		</TableHeadCell>
		{#each $shownColumns[item_type] as header}
			<TableHeadCell on:click={() => updateSortState(header)}>
				{formatString(header)}
			</TableHeadCell>
		{/each}
		<TableHeadCell>Details</TableHeadCell>
		{#if item_type === 'jobs'}
			<TableHeadCell>Run</TableHeadCell>
		{/if}
		<TableHeadCell>Delete</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each $itemlist[item_type] as item}
			<TableBodyRow>
				<TableBodyCell class="!p-4">
					<Checkbox bind:group={$selectedItems[item_type]} value={item.id} />
				</TableBodyCell>
				{#each $shownColumns[item_type] as header}
					<TableBodyCell class="hover:underline">
						{#if ['gpu_partition', 'priority', 'status', 'connection_status', 'speed'].includes(header)}
							<Badge {header} {item} />
						{:else if ['gpu_partition', 'priority', 'status', 'connection_status', 'speed'].includes(header)}
							{formatValue(item, header)}
						{:else if header.includes('time')}
							{formatDateTime(getPropertyValue(item, header))}
						{:else}
							{getPropertyValue(item, header)}
						{/if}
					</TableBodyCell>
				{/each}
				<TableBodyCell>
					<Drawer {item} {item_type} />
				</TableBodyCell>
				{#if isJob(item)}
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
