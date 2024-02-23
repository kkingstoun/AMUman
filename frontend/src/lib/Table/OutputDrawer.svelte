<script lang="ts">
	import { Drawer, Button, CloseButton } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { FileLinesOutline } from 'flowbite-svelte-icons';

	import type { Job } from '$api/Api';
	let hidden1 = true;
	let transitionParams = {
		x: -320,
		duration: 60,
		easing: sineIn
	};
	export let job: Job;
</script>

<Button size="sm" on:click={() => (hidden1 = false)}><FileLinesOutline /></Button>

<Drawer transitionType="fly" {transitionParams} bind:hidden={hidden1} id="sidebar1" class="w-3/5">
	<div class="flex items-center">
		<h5
			id="drawer-label"
			class="inline-flex items-center mb-4 text-base font-semibold text-gray-500 dark:text-gray-400"
		>
			Output for job {job.id}
			{job.path}
		</h5>
		<CloseButton on:click={() => (hidden1 = true)} class="mb-4 dark:text-white" />
	</div>
	{job.path}
	{job.output}
</Drawer>
