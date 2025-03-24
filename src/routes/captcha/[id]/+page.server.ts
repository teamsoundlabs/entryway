import type { PageServerLoad } from './$types';
import { validateToken } from '$lib/vaildate';
import {
	CLOUDFLARE_TURNSTILE_SECRET_KEY,
	CLOUDFLARE_TURNSTILE_SITE_KEY,
	REDIS_CHANNEL
} from '$env/static/private';
import RequestModel from '$db/schemas';
import { error } from '@sveltejs/kit';
import redis from '$db/redis';


export const load: PageServerLoad = async (params) => {
	const document = await RequestModel.findOne({ request_id: params.params.id }).lean();
	if (!document) {
		error(404, 'Verification request not found');
	}

	if (document.expires_at < new Date()) {
		error(410, 'Verification request expired');
	}

	return {
		sitekey: CLOUDFLARE_TURNSTILE_SITE_KEY,
		user: { ...document.user, _id: document.user._id.toString() },
		server: { ...document.server, _id: document.server._id.toString() }
	};
};

export const actions = {
	default: async ({ request, params }) => {
		const data = await request.formData();
		const token = data.get('cf-turnstile-response');

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

		const document = await RequestModel.findOne({ request_id: params.id });
		if (!document)
			return {
				error: 'Verification request not found',
				hide: true
			};

		if (document.state === 'completed')
			return {
				error: 'Verification request already completed',
				hide: true
			};
		
		await redis.publish(REDIS_CHANNEL, JSON.stringify({
			entry_id: document.request_id,
			server: document.server.id,
			user: document.user.id
		}));

		document.state = 'completed';
		await document.save();

		return {
			success: true
		};
	}
};
