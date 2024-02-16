<script lang="ts">
	import { Checkbox, Label } from 'flowbite-svelte';
	function toggle(event: any) {
		console.log(event);
	}
</script>

<Checkbox checked color="red">Red</Checkbox>
<Checkbox checked color="green">Green</Checkbox>
<Checkbox checked color="purple">Purple</Checkbox>
<Checkbox checked color="teal">Teal</Checkbox>
<Checkbox checked color="yellow">Yellow</Checkbox>
<Checkbox checked color="orange">Orange</Checkbox>
<Checkbox>
	<div class="text-gray-200">Default checkbox</div></Checkbox
>
<Label class="flex items-center">
	<Checkbox checked inline class="text-sky-400 focus:ring-pink-500" />
	Your custom color
</Label>
<!-- <div>
	<button class="bg-violet-900 hover:bg-violet-950 text-white font-bold py-2 px-4 rounded">
		Queue watchdog
	</button>
</div>

<label class="inline-flex items-center cursor-pointer">
	<input type="checkbox" value="" class="sr-only peer" on:click={toggle} />
	<div
		class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:bg-gray-200 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-violet-900"
	/>
	<span class="ms-3 text-sm font-medium text-gray-900">Autorun jobs</span>
</label> -->

<!-- <div class="s s--slider" style="font-size:{fontSize}px">
	<span>Autorun jobs</span>
	<button
		role="switch"
		aria-checked={checked}
		aria-labelledby={`switch-${uniqueID}`}
		on:click={handleClick}
	/>
</div> -->
