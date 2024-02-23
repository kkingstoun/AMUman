<script lang="ts">
	import { Sidebar, SidebarWrapper } from 'flowbite-svelte';
	import ColumnFiters from './sidebar/ColumnFiters.svelte';
</script>

<Sidebar class="w-2/12 pt-24 pl-3">
	<SidebarWrapper>
		<ColumnFiters />
	</SidebarWrapper>
</Sidebar>
