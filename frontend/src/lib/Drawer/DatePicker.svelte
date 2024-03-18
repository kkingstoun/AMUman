<script>
	import { DateInput } from 'date-picker-svelte';
	let date = new Date();
</script>

<DateInput bind:value={date} />

<style>
	:root {
		--date-picker-background: #1b1e27;
		--date-picker-foreground: #f7f7f7;
	}
</style>
