<script lang="ts">
	import { Navbar, NavBrand, NavUl, NavHamburger, NavLi } from 'flowbite-svelte';
	import Avatar from './Avatar.svelte';
</script>

<Navbar class="!bg-gray-800">
	<NavBrand href="/jobs">
		<img src="/images/logo.png" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Amuman</span>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/newjob">New Job</NavLi>
		<NavLi href="/jobs">Jobs</NavLi>
		<NavLi href="/nodes">Nodes</NavLi>
		<NavLi href="/gpus">GPUs</NavLi>
	</NavUl>
	<Avatar />
</Navbar>
