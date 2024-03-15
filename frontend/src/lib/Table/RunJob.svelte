<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { PlayOutline } from 'flowbite-svelte-icons';
	import { runJob } from '$api/Table';
	import type { Job } from '$api/OpenApi';
	export let job: Job;
</script>

<Button
	outline
	color="dark"
	size="xs"
	class="!text-green-400"
	on:click={() => {
		runJob(job);
	}}
>
	<PlayOutline />
</Button>
