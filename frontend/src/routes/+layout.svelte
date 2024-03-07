<script lang="ts">
	import 'tailwindcss/tailwind.css';
	import { Spinner } from 'flowbite-svelte';
	import { newToast } from '$lib/Utils';
	import { accessToken, refreshToken } from '$stores/Auth';
	import NavBar from '$lib/Navbar/NavBar.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import ToastList from '$lib/ToastList.svelte';
	let isLoading = true;
	onMount(() => {
		document.documentElement.classList.add('dark');
		let localStorageRefreshToken = localStorage.getItem('refresh_token');
		if (localStorageRefreshToken) {
			refreshToken.set(localStorageRefreshToken);
			let localStorageAccessToken = localStorage.getItem('access_token');
			if (localStorageAccessToken) {
				accessToken.set(localStorageAccessToken);
			}
			isLoading = false;
			// goto('/jobs');
		} else {
			isLoading = false;
			// goto('/login');
		}
	});
</script>

<svelte:head>
	<title>Amuman</title>
</svelte:head>

<!-- <ToastList /> -->

{#if isLoading}
	<div class="text-center align-middle">
		<Spinner size={8} />
	</div>
{:else}
	<div class="flex flex-col h-screen bg-gray-900">
		<slot />
	</div>
{/if}

<style>
	:global(:root) {
		--accent-color: #3d1999;
		--accent-color-hover: #2f0e6e;
		color-scheme: dark;
	}
</style>
