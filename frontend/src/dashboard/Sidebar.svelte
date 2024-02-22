<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import ColumnFiters from './sidebar/ColumnFiters.svelte';
</script>

<Sidebar class="w-2/12">
	<SidebarWrapper>
		<ColumnFiters />
	</SidebarWrapper>
</Sidebar>
