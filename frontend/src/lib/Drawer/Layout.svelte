<script lang="ts">
	import { Drawer, Button, Heading } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { FileLinesOutline } from 'flowbite-svelte-icons';
	import type { ItemType, ItemTypeString } from '$stores/Tables';
	import { headers } from '$stores/Tables';
	import { formatDateTime, formatValue, getPropertyValue, isJob } from '$lib/Utils';
	import Badge from '$lib/Table/Badge.svelte';
	import Output from './Output.svelte';
	import DatePicker from '$lib/Drawer/DatePicker.svelte';
	export let item: ItemType;
	export let item_type: ItemTypeString;
	let drawerHidden = true;
	let transitionParams = {
		x: -320,
		duration: 60,
		easing: sineIn
	};
</script>

<Button outline color="dark" size="xs" on:click={() => (drawerHidden = false)}
	><FileLinesOutline /></Button
>

<Drawer
	transitionType="fly"
	{transitionParams}
	bind:hidden={drawerHidden}
	id="sidebar1"
	class="w-3/5"
>
	<div class="flex items-center">
		<div class="p-4">
			<DatePicker />
			<Heading tag="h5" class="mb-4" customSize="text-3xl font-extrabold"
				>{item_type} details</Heading
			>

			<div class="space-y-2">
				{#each $headers[item_type] as header}
					<p class="text-sm">
						<strong class="inline-block w-48">{header}:</strong>
						{#if ['gpu_partition', 'priority', 'status', 'connection_status', 'speed'].includes(header)}
							<Badge {header} {item} />
						{:else if ['gpu_partition', 'priority', 'status', 'connection_status', 'speed'].includes(header)}
							{formatValue(item, header)}
						{:else if header.includes('time')}
							{formatDateTime(getPropertyValue(item, header))}
						{:else if header === 'duration'}
							{getPropertyValue(item, header)} Hours
						{:else}
							{getPropertyValue(item, header)}
						{/if}
					</p>
				{/each}
				{#if isJob(item)}
					<Output job={item} />
				{/if}
			</div>
		</div>
	</div>
</Drawer>
