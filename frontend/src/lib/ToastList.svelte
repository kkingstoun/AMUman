<script lang="ts">
	import { Toast } from 'flowbite-svelte';
	import { CheckCircleSolid } from 'flowbite-svelte-icons';
	import { fly } from 'svelte/transition';
	import { toasts } from '$stores/Other';
</script>

<div class="fixed w-full right-0 top-0">
	{#each $toasts as { message, color }, i}
		<div style="margin-top: {i * 1.5}rem;" class="right-0 top-0">
			<Toast transition={fly} params={{ x: 200 }} {color}>
				<svelte:fragment slot="icon">
					<CheckCircleSolid class="w-5 h-5" />
					<span class="sr-only">Check icon</span>
				</svelte:fragment>
				{message}
			</Toast>
		</div>
	{/each}
</div>
