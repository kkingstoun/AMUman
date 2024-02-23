<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import ColumnFiters from './ColumnFiters.svelte';
	import type { ItemTypeString } from '$stores/Tables';

	export let item_type: ItemTypeString;
</script>

<Sidebar class="w-2/12 pt-24 pl-3">
	<SidebarWrapper>
		<ColumnFiters {item_type} />
	</SidebarWrapper>
</Sidebar>
