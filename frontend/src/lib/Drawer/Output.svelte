<script lang="ts">
	import { onMount } from 'svelte';
	import type { Job } from '$api/Api';
	export let job: Job;
	import Prism from 'prismjs';
	import 'prismjs/components/prism-go'; // Ensure the import path is correct

	let output = '';
	onMount(() => {
		output = job.output || 'nope';
	});
</script>

<strong class="inline-block w-32">output:</strong>
<div class="text-sm whitespace-pre-wrap shadow p-3 bg-slate-900">
	<div class="code">
		{@html Prism.highlight(output, Prism.languages['go'], 'go')}
	</div>
</div>

<svelte:head>
	<link
		href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/themes/prism.min.css"
		rel="stylesheet"
	/>
</svelte:head>
