<script lang="ts">
	import { Turnstile } from 'svelte-turnstile';

	let { form, data } = $props();
</script>

<svelte:head>
    <title>Entryway - Captcha</title> 
	<meta name="description" content="Verify your humanity before proceeding." />
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="lg:min-h-screen">
	<div class="card bg-base-200 w-96 rounded-md lg:mt-10">
		<div class="card-body">
			<h2 class="card-title">Are you human? 🤖</h2>
			<p>
				<b>{data.server.name}</b> requires you to verify your humanity before you can proceed.
			</p>

			{#if form?.success}
				<i>Success, you may return back to Guilded.</i>
			{/if}

			<div class="card-actions">
				{#if (!form?.success && !form?.hide) || false}
					<form method="POST" id="form">
						<Turnstile
							siteKey={data.sitekey}
							size="flexible"
							on:callback={() => {
								let form = document.getElementById('form') as HTMLFormElement;
								form.submit();
							}}
						/>
					</form>
				{/if}

				{#if form?.error}
					<i class="opacity-85">{form?.error}.</i>
				{/if}
			</div>
		</div>
	</div>
</div>
