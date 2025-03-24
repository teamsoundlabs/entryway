<script lang="ts">
	import { page } from '$app/state';
</script>

<div class="lg:min-h-screen">
	<p class="lg:mt-10">{page.status}: <i>{page.error?.message}.</i></p>
</div>
