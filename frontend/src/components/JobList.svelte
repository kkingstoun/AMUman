<script lang="ts">
	var activeTasks: {
		number: number;
		id: string;
		path: string;
		nodeName: string;
		port: number;
		submitTime: string;
	}[] = [
		{
			number: 1,
			id: '1',
			path: '/path/to/file',
			nodeName: 'node1',
			port: 8080,
			submitTime: '2022-01-01 00:00:00'
		},
		{
			number: 2,
			id: '2',
			path: '/path/to/file',
			nodeName: 'node2',
			port: 8081,
			submitTime: '2022-01-01 00:00:01'
		},
		{
			number: 3,
			id: '3',
			path: '/path/to/file',
			nodeName: 'node3',
			port: 8082,
			submitTime: '2022-01-01 00:00:02'
		}
	];
	import { onMount } from 'svelte';
	import OpenButton from './OpenButton.svelte';
	// import { getTasks } from '../api';

	onMount(async () => {
		// activeTasks = await getTasks();
		activeTasks = [
			{
				number: 1,
				id: '1',
				path: '/path/to/file',
				nodeName: 'node1',
				port: 8080,
				submitTime: '2022-01-01 00:00:00'
			},
			{
				number: 2,
				id: '2',
				path: '/path/to/file',
				nodeName: 'node2',
				port: 8081,
				submitTime: '2022-01-01 00:00:01'
			},
			{
				number: 3,
				id: '3',
				path: '/path/to/file',
				nodeName: 'node3',
				port: 8082,
				submitTime: '2022-01-01 00:00:02'
			}
		];
	});
</script>

<section>
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
						{#each activeTasks as task}
							<tr>
								<td class="table-cell">
									<!-- <p class="whitespace-no-wrap">{task.number}</p> -->
									{task.number}
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{task.id}</p>
								</td>
								<td class="table-cell">
									<p class="whitespace-no-wrap">{task.path}</p>
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
									<p class="whitespace-no-wrap">{task.submitTime}</p>
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
