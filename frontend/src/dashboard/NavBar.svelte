<script lang="ts">
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import ColumnFilters from './navbar/ColumnFiters.svelte';
	import Logout from './navbar/Logout.svelte';
</script>

<Navbar>
	<NavBrand href="/">
		<img src="/images/logo.png" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Amuman</span>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/">Home</NavLi>
		<ColumnFilters />
		<NavLi href="/settings">Setting</NavLi>
		<NavLi href="/pricing">Pricing</NavLi>
		<NavLi href="/contact">Contact</NavLi>
		<Logout />
	</NavUl>
</Navbar>
<!-- <script lang="ts">
	import { openSidebar } from '../store';
	import { isAuthenticated } from '../store';
	import { Button } from 'flowbite-svelte';
	import Refresh from '$lib/Refresh.svelte';
	import ColumnHider from '$lib/ColumnHider.svelte';
	function handleLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		isAuthenticated.set(false);
	}
</script>

<header class="h-16 md:h-20 items-center relative w-full z-10">
	<div class="flex flex-col flex-center h-full px-3 mx-auto relative justify-center">
		<div class="flex items-center pl-1 relative w-full sm:ml-0 sm:pr-2 lg:max-w-68">
			<Refresh />
			<ColumnHider />

			<div
				class="flex items-center justify-end ml-5 p-1 relative w-9/12 sm:mr-0 sm:right-auto md:w-1/4"
			>
				<span class="inline-block px-3 py-2 relative rounded text-white">
					<span>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"
							/>
						</svg>
					</span>
					<span
						class="absolute bg-violet-900 font-bold px-2 py-0.5 right-0 rounded-full text-xs top-0"
					>
						3
					</span>
				</span>
			</div>
			<div class="mt-2 ml-8 w-50">
				<div>
					<Button on:click={handleLogout} class="font-extrabold">Logout</Button>
				</div>
			</div>
		</div>
	</div>
</header> -->
