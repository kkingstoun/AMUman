<script lang="ts">
	import { NavLi } from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';

	import { lastFetchTime } from '$stores/store';
	import { fetchJobs } from '$api/jobs';
	import moment from 'moment';
</script>

<NavLi class="cursor-pointer" on:click={fetchJobs}>
	Last refresh: {moment($lastFetchTime).format('HH:mm:ss')}</NavLi
>
