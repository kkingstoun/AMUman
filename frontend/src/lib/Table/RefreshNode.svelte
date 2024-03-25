<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { RefreshOutline } from 'flowbite-svelte-icons';
	import { refreshNode } from '$api/Table';
	import type { Node } from '$api/OpenApi';
	export let node: Node;

	let isRefreshing = false;
	async function handleRefresh() {
		isRefreshing = true;
		await refreshNode(node);
		setTimeout(() => {
			isRefreshing = false;
		}, 1000);
	}
</script>

<Button outline color="dark" size="xs" on:click={handleRefresh}>
	<RefreshOutline class={isRefreshing ? 'animate-spin' : ''} />
</Button>
