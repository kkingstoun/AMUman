<script lang="ts">
	import 'tailwindcss/tailwind.css';
	import { Spinner } from 'flowbite-svelte';
	import { initStores } from '$lib/Utils';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import ToastList from '$lib/ToastList.svelte';
	import { refreshToken } from '$stores/Auth';
	let isLoading = true;
	onMount(() => {
		window.fetch = fetch; // suppress warnings
		document.documentElement.classList.add('dark');

		initStores();

		isLoading = false;
		if (!$refreshToken) {
			goto('/login');
		}
	});
</script>

<svelte:head>
	<title>Amuman</title>
</svelte:head>

<ToastList />

<div class="bg-gray-900">
	{#if isLoading}
		<div class="flex justify-center items-center h-screen">
			<Spinner size={12} />
		</div>
	{:else}
		<div class="flex flex-col h-screen">
			<slot />
		</div>
	{/if}
</div>

<style>
	:global(:root) {
		--accent-color: #3d1999;
		--accent-color-hover: #2f0e6e;
		color-scheme: dark;
	}
</style>
