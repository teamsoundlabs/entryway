<script lang="ts">
	import { Turnstile } from 'svelte-turnstile';

	let { form, data } = $props();
</script>

{#if form?.success}
	<p>Ding!</p>
{/if}

<form method="POST" action="?/captcha" id="captcha-form">
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Verification</legend>
		<Turnstile
			siteKey={data.sitekey}
			theme="dark"
			size="flexible"
			on:callback={() => {
				const form = document.getElementById('captcha-form') as HTMLFormElement;
				if (form) {
					form.submit();
				}
			}}
		/>
		<div class="validator-hint text-error">{form?.error}</div>
		<p class="fieldset-label">Please wait while we verify you.</p>
	</fieldset>
</form>
