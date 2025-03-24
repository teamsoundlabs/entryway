<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" />
	<link
		href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Pixelify+Sans:wght@400..700&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
	<!-- Header -->
	<header class="navbar sticky top-0 z-10 text-white shadow-xl backdrop-blur-sm">
		<div class="flex flex-1 items-center space-x-2 p-2">
			<a class="text-2xl font-semibold uppercase" href="/">Entryway</a>
			<span class="text-lg font-light"
				>by <a href="https://github.com/teamsoundlabs">Sound Labs</a></span
			>
		</div>
	</header>

	<!-- Main -->
	<main class="container mx-auto flex h-full items-center justify-center">
		{@render children()}
	</main>

	<!-- Footer -->
	<footer class="footer sm:footer-horizontal bg-base-200 text-neutral-content items-center p-4">
		<aside class="grid-flow-col items-center">
			<p>
				© {new Date().getFullYear()} <a href="https://github.com/teamsoundlabs">Sound Labs</a>,
				<a href="https://aussies-fort.vercel.app">NotAussie.</a>
			</p>
		</aside>
	</footer>
</div>
