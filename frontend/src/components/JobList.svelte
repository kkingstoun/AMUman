<script lang="ts">
	import type { Job } from '../types';

	var activeJobs: Job[] = [];
	import { onMount } from 'svelte';
	import OpenButton from './OpenButton.svelte';
	import { getJobs } from '../api';
	export let job_status = '';
	onMount(async () => {
		activeJobs = await getJobs(job_status);
	});
</script>

<section>
	<div class="mt-6 mb-3 text-gray-400">{job_status} jobs</div>
	<div class="mt-8 rounded-2xl" style="background: rgb(146 151 179 / 13%)">
		<div class="container mx-auto">
			<div class="max-w-full overflow-x-auto rounded-lg">
				<table class="w-full leading-normal text-white">
					<thead>
						<tr>
							<th class="table-header"> User </th>
							<th class="table-header"> Role </th>
							<th class="table-header"> Created_at </th>
							<th class="table-header"> status </th>
							<th class="table-header"> status </th>
							<th class="table-header"> status </th>
						</tr>
					</thead>
					<tbody>
						{#if activeJobs.length === 0}
							<tr>
								<td class="table-cell" colspan="6">
									<p class="whitespace-no-wrap">No active jobs</p>
								</td>
							</tr>
						{/if}
						{#each activeJobs as job}
							<tr>
								<td class="table-cell">
									{job.id}
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{job.id}</p>
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{job.path}</p>
								</td>
								<td class="table-cell">
									<span class="relative inline-block px-3 py-1 font-semibold leading-tight">
										<span
											aria-hidden="true"
											class="absolute inset-0 bg-green-200 opacity-50 rounded-full"
										/> <span class="relative">active</span>
									</span>
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap"><OpenButton /></p>
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{job.submit_time}</p>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</section>

<style>
	.table-header {
		@apply px-5 py-3 border-b border-gray-200 text-left text-sm uppercase font-normal;
	}
	.table-cell {
		@apply px-5 py-5 border-b border-gray-200 text-sm;
	}
</style>
