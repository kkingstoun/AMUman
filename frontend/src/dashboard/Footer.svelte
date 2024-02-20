<script>
	import { Footer, FooterCopyright, FooterIcon } from 'flowbite-svelte';
	import { GithubSolid } from 'flowbite-svelte-icons';
</script>

<Footer footerType="socialmedia">
	<hr class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
	<div class="sm:flex sm:items-center sm:justify-between">
		<FooterCopyright
			href="https://github.com/kkingstoun/AMUman"
			by="Mathieu Moalic & Mateusz Zelent"
		/>

		<div class="flex mt-4 space-x-6 rtl:space-x-reverse sm:justify-center sm:mt-0">
			<FooterIcon href="https://github.com/kkingstoun/AMUman">
				<GithubSolid
					class="w-4 h-4 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white"
				/>
			</FooterIcon>
		</div>
	</div>
</Footer>
