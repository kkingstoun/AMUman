<script lang="ts">
	import JobList from '$lib/JobList.svelte';
	import { RefreshOutline } from 'flowbite-svelte-icons';
	import { lastFetchTime, timeSinceLastFetch } from '$stores/store';
	import { fetchJobs } from '$api/Jobs';
	import moment from 'moment';
</script>

<div class="flex pb-4 items-center">
	<h2 class="text-4xl">Jobs</h2>
	<div class="ml-7 text-gray-500">
		Last refresh: {moment($lastFetchTime).format('HH:mm:ss')} ({$timeSinceLastFetch})
	</div>
	<RefreshOutline on:click={fetchJobs} class="ml-3 text-gray-500" />
</div>
<JobList />
