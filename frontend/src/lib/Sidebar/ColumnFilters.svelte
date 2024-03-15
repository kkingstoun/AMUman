<script lang="ts">
	import type { ItemTypeString } from '$stores/Tables';
	import { orderShownColumnsLikeHeaders } from '$lib/Utils';
	import { headers, shownColumns } from '$stores/Tables';
	import { Checkbox, Heading } from 'flowbite-svelte';
	import { formatString } from '$lib/Utils';

	export let item_type: ItemTypeString;

	function onCheck() {
		orderShownColumnsLikeHeaders();
	}
</script>

<div class="pl-3">
	<Heading tag="h6" class="pb-2">Columns</Heading>
	{#each $headers[item_type] as column}
		<Checkbox
			class="hover:bg-gray-700 ml-4"
			bind:group={$shownColumns[item_type]}
			on:change={onCheck}
			value={column}>{formatString(column)}</Checkbox
		>
	{/each}
</div>
