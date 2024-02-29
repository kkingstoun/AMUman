<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import { PlayOutline } from 'flowbite-svelte-icons';
	import type { Job } from '$api/Api';
	export let job: Job;

	function runJob() {
		console.log('Running job', job.id);
	}
</script>

<Button outline color="dark" size="xs" class="!text-green-400" on:click={runJob}>
	<PlayOutline />
</Button>
