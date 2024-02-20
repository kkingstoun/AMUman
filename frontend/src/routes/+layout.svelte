<script lang="ts">
	import Layout from '$dashboard/Layout.svelte';
	import { onMount } from 'svelte';
	onMount(() => {
		document.documentElement.classList.add('dark');
	});
</script>

<svelte:head>
	<title>Amuman</title>
</svelte:head>

<Layout>
	<slot />
</Layout>

<style>
	:global(:root) {
		--accent-color: #3d1999;
		--accent-color-hover: #2f0e6e;
		color-scheme: dark;
	}
</style>
