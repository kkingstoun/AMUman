<script lang="ts">
	import Layout from '../dashboard/Layout.svelte';
</script>

<Layout>
	<slot />
</Layout>

<style>
	:global(:root) {
		--accent-color: #3d1999;
		--accent-color-hover: #2f0e6e;
	}
</style>
