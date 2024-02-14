<script lang="ts">
	import Layout from "../dashboard/Layout.svelte";
    import { SvelteToast } from '@zerodevx/svelte-toast'

</script>

<Layout>
	<SvelteToast />
	<slot />
</Layout>
