<script lang="ts">
	import { onMount } from 'svelte';
	import type { Job } from '$api/OpenApi';
	import { api } from '$stores/Auth';
	import { getRequestParams } from '$api/Auth';
	import { newToast } from '$stores/Toast';

	export let job: Job;
	import Prism from 'prismjs';
	import 'prismjs/components/prism-go'; // Ensure the import path is correct

	let output = 'waiting for output...';
	onMount(async () => {
		const params = getRequestParams();
		if (params !== null) {
			output = await api
				.jobsOutputRetrieve(job.id, params)
				.then((res) => {
					return res.data.output;
				})
				.catch((err) => {
					newToast(`Failed to retrieve output for job ${job.id}`, 'red');
					return `Failed to retrieve output: ${(err as Error).message || String(err)}`;
				});
		}
	});
</script>

<strong class="inline-block w-32">output:</strong>
<div class="text-sm whitespace-pre-wrap shadow p-3 bg-slate-900">
	<div class="code">
		{@html Prism.highlight(output, Prism.languages['go'], 'go')}
	</div>
</div>
