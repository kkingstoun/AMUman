<script lang="ts">
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import ColumnFilters from './navbar/ColumnFiters.svelte';
	import Logout from './navbar/Logout.svelte';
	import Refresh from './navbar/Refresh.svelte';
</script>

<Navbar>
	<NavBrand href="/">
		<img src="/images/logo.png" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Amuman</span>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<Refresh />
		<ColumnFilters />
		<Logout />
	</NavUl>
</Navbar>
