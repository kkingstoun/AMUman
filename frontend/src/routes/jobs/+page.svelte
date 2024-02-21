<script lang="ts">
	import JobList from '$lib/JobList.svelte';
	import { RefreshOutline } from 'flowbite-svelte-icons';
	import { lastFetchTime } from '$stores/store';
	import { fetchJobs } from '$api/jobs';
	import moment from 'moment';
	import { onMount, onDestroy } from 'svelte';

	let intervalId: ReturnType<typeof setInterval>;
	let timeSinceLastFetch = moment($lastFetchTime).fromNow();

	function refreshTimeSinceLastFetch() {
		timeSinceLastFetch = moment($lastFetchTime).fromNow();
	}
	onMount(() => {
		intervalId = setInterval(refreshTimeSinceLastFetch, 1000 * 60);
	});

	onDestroy(() => {
		clearInterval(intervalId);
	});
</script>

<div class="flex pb-4 items-center">
	<h2 class="text-4xl">Jobs</h2>
	<div class="ml-7 text-gray-500">
		Last refresh:{moment($lastFetchTime).format('HH:mm:ss')} ({timeSinceLastFetch})
	</div>
	<RefreshOutline on:click={fetchJobs} class="ml-3 text-gray-500" />
</div>
<JobList />
