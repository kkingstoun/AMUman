<script lang="ts">
	import JobList from './JobList.svelte';
</script>

<div>
	<div class="mt-6 mb-3 text-gray-400">Active jobs</div>
	<JobList />
	<div class="mt-6 mb-3 text-gray-400">Queued jobs</div>
	<JobList />
	<div class="mt-6 mb-3 text-gray-400">Finished jobs</div>
	<JobList />
</div>

<style></style>
