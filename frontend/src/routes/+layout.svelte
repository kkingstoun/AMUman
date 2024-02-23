<script lang="ts">
	import 'tailwindcss/tailwind.css';

	import NavBar from '$lib/Navbar/NavBar.svelte';
	import Login from '$lib/Login.svelte';
	import { isAuthenticated } from '$stores/Auth';
	import { SvelteToast } from '@zerodevx/svelte-toast';
	import { onMount } from 'svelte';
	onMount(() => {
		document.documentElement.classList.add('dark');
	});
</script>

<svelte:head>
	<title>Amuman</title>
</svelte:head>

<SvelteToast />
{#if $isAuthenticated}
	<div class="flex flex-col h-screen bg-gray-900">
		<NavBar />
		<main class="flex-1 overflow-y-auto p-4 md:p-8">
			<slot />
		</main>
	</div>
{:else}
	<Login />
{/if}

<style>
	:global(:root) {
		--accent-color: #3d1999;
		--accent-color-hover: #2f0e6e;
		color-scheme: dark;
	}
</style>
