<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { PlayOutline } from 'flowbite-svelte-icons';
	import type { Job } from '$api/Api';
	export let job: Job;

	function runJob() {
		console.log('Running job', job.id);
	}
</script>

<Button color="green" size="sm" on:click={runJob}>
	<PlayOutline />
</Button>
