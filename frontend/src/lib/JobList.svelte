<script lang="ts">
	import type { Job } from '../Api';
	import { api } from '../store';
	import { errorToast } from './Toast';
	// export let jobStatus: 'running' | 'queued' | 'finished' = 'running';
	var activeJobs: Job[] = [];
	import { onMount } from 'svelte';
	import OpenButton from './OpenButton.svelte';
	import { AccordionItem, Accordion } from 'flowbite-svelte';

	onMount(async () => {
		api
			.jobsList()
			.then((res) => {
				activeJobs = res.data;
			})
			.catch((err) => {
				console.error(err);
				errorToast('Failed to fetch jobs');
			});
	});
</script>

<section>
	<div class="mt-8 rounded-2xl" style="background: rgb(146 151 179 / 13%)">
		<div class="container mx-auto">
			<div class="max-w-full overflow-x-auto rounded-lg">
				<script>
					import { AccordionItem, Accordion } from 'flowbite-svelte';
				</script>

				<Accordion>
					<AccordionItem>
						<span slot="header">My Header 1</span>
						<p class="mb-2 text-gray-500 dark:text-gray-400">
							Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
							explicabo ...
						</p>
						<p class="text-gray-500 dark:text-gray-400">
							Check out this guide to learn how to <a
								href="/"
								target="_blank"
								rel="noreferrer"
								class="text-blue-600 dark:text-blue-500 hover:underline"
							>
								get started
							</a>
							and start developing websites even faster with components on top of Tailwind CSS.
						</p>
					</AccordionItem>
					<AccordionItem>
						<span slot="header">My Header 2</span>
						<p class="mb-2 text-gray-500 dark:text-gray-400">
							Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
							explicabo ...
						</p>
						<p class="mb-2 text-gray-500 dark:text-gray-400">
							Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
							explicabo ...
						</p>
						<p class="mb-2 text-gray-500 dark:text-gray-400">
							Learn more about these technologies:
						</p>
						<ul class="list-disc ps-5 dark:text-gray-400 text-gray-500">
							<li>
								<a
									href="/"
									target="_blank"
									rel="noreferrer"
									class="text-blue-600 dark:text-blue-500 hover:underline"
								>
									Lorem ipsum
								</a>
							</li>
							<li>
								<a
									href="https://tailwindui.com/"
									rel="noreferrer"
									target="_blank"
									class="text-blue-600 dark:text-blue-500 hover:underline"
								>
									Tailwind UI
								</a>
							</li>
						</ul>
					</AccordionItem>
				</Accordion>
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
						{#each activeJobs as job}
							<tr class="hover:bg-gray-700">
								<td class="table-cell">
									{job.id}
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{job.id}</p>
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">path</p>
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
									<p class="whitespace-no-wrap">submit_time</p>
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
