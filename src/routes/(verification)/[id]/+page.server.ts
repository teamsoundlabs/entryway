import type { PageServerLoad } from './$types';
import { validateToken } from '$lib/vaildate';
import { CLOUDFLARE_TURNSTILE_SECRET_KEY, CLOUDFLARE_TURNSTILE_SITE_KEY } from '$env/static/private';

export const load: PageServerLoad = async ({ params }) => {
	return {
		sitekey: CLOUDFLARE_TURNSTILE_SITE_KEY
	};
};

export const actions = {
	captcha: async ({ request }) => {
		const data = await request.formData();

		const token = data.get('cf-turnstile-response'); // if you edited the formsField option change this

		if (!token)
			return {
				error: 'No CAPTCHA token provided'
			};
		else if (typeof token !== 'string')
			return {
				error: 'Invalid CAPTCHA token'
			};

		const { success, error } = await validateToken(token, CLOUDFLARE_TURNSTILE_SECRET_KEY);
		if (!success)
			return {
				error: error || 'Invalid CAPTCHA'
			};

		return {
			success: true
		};
	}
};
