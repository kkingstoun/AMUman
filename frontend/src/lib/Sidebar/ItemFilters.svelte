<script lang="ts">
	import type { ItemTypeString } from '$stores/Tables';
	import { headers, shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { formatString } from '$lib/Utils';

	export let item_type: ItemTypeString;
</script>

<div class="pl-3">
	<Heading tag="h6" class="pb-2 mt-4">Filter {item_type}</Heading>
	{#each $headers[item_type] as column}
		<Checkbox class="hover:bg-gray-700 ml-4" bind:group={$shownColumns[item_type]} value={column}
			>{formatString(column)}</Checkbox
		>
	{/each}
</div>
