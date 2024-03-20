<script lang="ts">
	import { Pagination } from 'flowbite-svelte';
	import { jobsFilters } from '$stores/Sidebar';
	import { fetchJobs } from '$api/Table';
	import { pagination } from '$stores/Tables';

	interface Page {
		name: string;
	}
	let pages: Page[] = [];
	$: if ($pagination.count !== undefined && $jobsFilters.limit !== undefined) {
		let page_number = Math.ceil($pagination.count / $jobsFilters.limit);
		pages = Array.from({ length: page_number }, (_, i) => ({ name: (i + 1).toString() }));
	}

	const previous = () => {
		if ($pagination.count === undefined || $jobsFilters.limit === undefined) {
			return;
		}
		$jobsFilters.offset -= $jobsFilters.limit;
		$jobsFilters.offset = Math.max(0, $jobsFilters.offset);
		$jobsFilters.offset = Math.min($jobsFilters.offset, $pagination.count - $jobsFilters.limit);
		fetchJobs();
	};
	const next = () => {
		if ($pagination.count === undefined || $jobsFilters.limit === undefined) {
			return;
		}
		$jobsFilters.offset += $jobsFilters.limit;
		$jobsFilters.offset = Math.max(0, $jobsFilters.offset);
		$jobsFilters.offset = Math.min($jobsFilters.offset, $pagination.count - $jobsFilters.limit);

		fetchJobs();
	};
	const handleClick = (event: MouseEvent) => {
		if (event.target instanceof HTMLElement) {
			let page_clicked = Number(event.target.innerHTML);
			$jobsFilters.offset = (page_clicked - 1) * $jobsFilters.limit;
			fetchJobs();
		}
	};
</script>

<div class="flex items-center justify-center m-4">
	<Pagination
		{pages}
		on:previous={previous}
		on:next={next}
		on:click={(event) => {
			handleClick(event);
		}}
	/>
</div>
