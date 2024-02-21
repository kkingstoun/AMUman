<script lang="ts">
	import 'tailwindcss/tailwind.css';

	import NavBar from './NavBar.svelte';
	import Login from '$lib/Login.svelte';
	import Sidebar from './Sidebar.svelte';
	import { isAuthenticated } from '$stores/store';
	import { SvelteToast } from '@zerodevx/svelte-toast';
</script>

<SvelteToast />
{#if $isAuthenticated}
	<div class="flex flex-col h-screen bg-gray-900">
		<NavBar />
		<div class="flex flex-1 overflow-hidden">
			<Sidebar />
			<main class="flex-1 overflow-y-auto p-4 md:p-8">
				<slot />
			</main>
		</div>
	</div>
{:else}
	<Login />
{/if}
