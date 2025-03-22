<script lang="ts">
	import { page } from '$app/state';
</script>

<p>{page.status}: {page.error?.message}</p>
