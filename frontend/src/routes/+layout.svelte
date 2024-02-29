<script lang="ts">
	import 'tailwindcss/tailwind.css';
	import { newToast } from '$lib/Utils';

	import NavBar from '$lib/Navbar/NavBar.svelte';
	import Login from '$lib/Login.svelte';
	import { isAuthenticated } from '$stores/Auth';
	import { onMount } from 'svelte';
	import ToastList from '$lib/ToastList.svelte';
	onMount(() => {
		document.documentElement.classList.add('dark');
		newToast('hi', 'blue');
		newToast('hi2', 'green');
	});
</script>

<svelte:head>
	<title>Amuman</title>
</svelte:head>

<!-- <ToastList /> -->
{#if $isAuthenticated}
	<div class="flex flex-col h-screen bg-gray-900">
		<NavBar />
		<slot />
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
