<script lang="ts">
	import type { ItemTypeString } from '$stores/Tables';
	import { Heading } from 'flowbite-svelte';
	import UserFilter from './Filters/User.svelte';
	import StatusFilter from './Filters/Status.svelte';
	import JobFilterNodes from './Filters/Nodes.svelte';
	export let item_type: ItemTypeString;
	let filters = [UserFilter, StatusFilter, JobFilterNodes];
	let filterNames = ['User', 'Status', 'Node'];
</script>

<div class="pl-3 flex flex-col gap-2">
	<Heading tag="h6" class="pb-2 mt-4">Filter {item_type}</Heading>
	{#each filters as component, index}
		<div class="flex w-full">
			<span class="flex-grow text-right mr-2 w-0">{filterNames[index]}:</span>
			<div class="flex-grow w-12">
				<svelte:component this={component} />
			</div>
		</div>
	{/each}
</div>
