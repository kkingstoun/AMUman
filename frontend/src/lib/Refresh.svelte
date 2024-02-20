<script lang="ts">
	import { lastFetchTime } from '../stores/store';
	import { Button } from 'flowbite-svelte';
	import { fetchJobs } from '../api/jobs';
	import moment from 'moment';
</script>

<div class="flex items-center">
	<p class="text-white text-sm">
		Last fetched: {moment($lastFetchTime).format('YYYY-MM-DD HH:mm:ss')} ({moment(
			$lastFetchTime
		).fromNow()})
	</p>
</div>
<Button class="font-extrabold" on:click={fetchJobs}>Refresh</Button>
