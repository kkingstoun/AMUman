<script>
	import { DateInput } from 'date-picker-svelte';
	let date = new Date();
</script>

<DateInput bind:value={date} />
