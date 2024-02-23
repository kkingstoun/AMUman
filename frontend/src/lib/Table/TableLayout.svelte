<script lang="ts">
	import TableContent from './TableContent.svelte';
	import TableTitle from './TableTitle.svelte';
	import Sidebar from './Sidebar.svelte';

	import type { ItemTypeString } from '$stores/Tables';
	export let item_type: ItemTypeString;
</script>

<div class="flex overflow-hidden pb-3 pr-3">
	<div class="flex h-auto pr-3">
		<Sidebar {item_type} />
	</div>

	<div class="flex flex-col w-full pt-3 overflow-auto">
		<TableTitle {item_type} />
		<TableContent {item_type} />
	</div>
</div>
