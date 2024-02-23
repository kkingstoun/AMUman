<script lang="ts">
	import Table from '$lib/Table/Table.svelte';
	import TableHeader from './TableHeader.svelte';

	import type { ItemTypeString } from '$stores/Tables';
	import Sidebar from '$lib/Table/Sidebar/Sidebar.svelte';

	export let item_type: ItemTypeString;
</script>

<div class="flex overflow-hidden">
	<Sidebar {item_type} />
	<div class="flex flex-col w-4/5">
		<TableHeader {item_type} />
		<Table {item_type} />
	</div>
</div>
