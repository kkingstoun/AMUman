<script>
	import { Pagination } from 'flowbite-svelte';
	import { ArrowLeftOutline, ArrowRightOutline } from 'flowbite-svelte-icons';
	let helper = { start: 1, end: 10, total: 100 };

	const previous = () => {
		alert('Previous btn clicked. Make a call to your server to fetch data.');
	};
	const next = () => {
		alert('Next btn clicked. Make a call to your server to fetch data.');
	};
</script>

<div class="flex items-center justify-center m-4">
	<Pagination table>
		<div slot="prev" class="flex items-center gap-2 text-white">
			<ArrowLeftOutline class="w-3.5 h-3.5 me-2" />
			Prev
		</div>
		<div slot="next" class="flex items-center gap-2 text-white">
			Next
			<ArrowRightOutline class="w-3.5 h-3.5 ms-2" />
		</div>
	</Pagination>
</div>
