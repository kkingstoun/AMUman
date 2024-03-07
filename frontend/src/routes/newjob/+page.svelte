<script lang="ts">
	import type { Job } from '$api/Api';
	import { PriorityEnum, GpuPartitionEnum, JobStatusEnum } from '$api/Api';
	import { api } from '$stores/Auth';
	import { getRequestParams } from '$api/Auth';
	import NavBar from '$lib/Navbar/NavBar.svelte';
	let job: Job = {
		id: 0,
		user: 'username',
		path: '',
		priority: PriorityEnum.NORMAL,
		gpu_partition: GpuPartitionEnum.NORMAL,
		status: JobStatusEnum.PENDING,
		flags: '',
		duration: 1
	};

	const maxPathLength = 500;
	const maxFlagsLength = 150;

	async function submitJob() {
		let res = await api.jobsCreate(job, getRequestParams());
		if (res.status === 201) {
			console.log('Job created');
		} else {
			console.error('Job creation failed');
		}
		job.path = '';
	}
</script>

<NavBar />
<div class="flex flex-col items-center mx-auto w-5/12">
	<h1 class="text-4xl text-white">New Job</h1>
	<form class="space-y-4 text-white p-4 rounded w-full">
		<div>
			<label for="path" class="block">Path</label>
			<input
				type="text"
				id="path"
				bind:value={job.path}
				class="input"
				maxlength={maxPathLength}
				required
			/>
		</div>
		<div>
			<label for="priority" class="block">Priority</label>
			<select id="priority" bind:value={job.priority} class="input">
				<option value="" disabled>Select priority</option>
				{#each Object.values(PriorityEnum) as option}
					<option value={option}>{option}</option>
				{/each}
			</select>
		</div>
		<div>
			<label for="gpu_partition" class="block">GPU Partition</label>
			<select id="gpu_partition" bind:value={job.gpu_partition} class="input">
				<option value="" disabled>Select GPU partition</option>
				{#each Object.values(GpuPartitionEnum) as option}
					<option value={option}>{option}</option>
				{/each}
			</select>
		</div>
		<div>
			<label for="status" class="block">Status</label>
			<select id="status" bind:value={job.status} class="input">
				<option value="" disabled>Select status</option>
				{#each Object.values(JobStatusEnum) as option}
					<option value={option}>{option}</option>
				{/each}
			</select>
		</div>
		<div>
			<label for="flags" class="block">Flags</label>
			<input
				type="text"
				id="flags"
				bind:value={job.flags}
				class="input"
				maxlength={maxFlagsLength}
			/>
		</div>
		<div>
			<label for="duration" class="block">Duration (Hours)</label>
			<input type="number" id="duration" bind:value={job.duration} class="input" />
		</div>

		<button
			type="submit"
			class="ml-4 bg-violet-900 hover:bg-violet-950 text-white font-bold py-2 px-4 rounded"
			on:click={submitJob}>Submit</button
		>
	</form>
</div>

<style>
	.input {
		display: block;
		width: 100%;
		padding: 0.5rem;
		margin-top: 0.25rem;
		background-color: rgb(55 65 81);
		border: 1px solid #444;
		color: white;
		border-radius: 0.25rem;
	}
</style>
