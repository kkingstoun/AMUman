<script lang="ts">
	import { lastFetchTime, timeSinceLastFetch } from '$stores/Tables';
	import { formatString } from '$lib/Utils';
	import type { ItemTypeString } from '$stores/Tables';
	import { RefreshOutline } from 'flowbite-svelte-icons';
	import { fetchItems } from '$api/Table';
	import moment from 'moment';

	export let item_type: ItemTypeString;
</script>

<h2 class="text-4xl">{formatString(item_type)}</h2>
<div class="ml-7 text-gray-500">
	Last refresh: {moment($lastFetchTime).format('HH:mm:ss')} ({$timeSinceLastFetch})
	<div class="flex pb-4 items-center">
		<RefreshOutline
			on:click={() => {
				fetchItems('jobs');
			}}
			class="ml-3 text-gray-500"
		/>
	</div>
</div>
