import { verifyKey } from '@unkey/api';

import RequestModel from '$db/schemas';
import type { RequestHandler } from './$types';
import { createRequestBody } from '$lib/schema';

import { UNKEY_API_ID } from '$env/static/private';
import { decodeZodErrors } from '$lib/zod_helper';
import { json } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const auth = request.headers.get('Authorization');
	if (!auth) return new Response('Unauthorized', { status: 401 });

	const { result, error } = await verifyKey({ key: auth, apiId: UNKEY_API_ID });
	if (error) return new Response('Authentication failed', { status: 503 });
	if (!result.permissions?.includes('services.entryway.create_request'))
		return new Response('Unauthorized', { status: 401 });

	const rawBody = await request.text();
	if (!rawBody) return new Response('Bad request', { status: 400 });

	let body;
	try {
		body = JSON.parse(rawBody);
	} catch {
		return new Response('Invalid JSON', { status: 400 });
	}

	let data;
	try {
		data = createRequestBody.parse(body);
	} catch (error) {
		return json(
			{
				detail: 'Invalid request body',
				errors: decodeZodErrors(error as unknown).errors
			},
			{ status: 400 }
		);
	}

	const document = new RequestModel(data);
	await document.save();

	return json(
		{ detail: 'Success', id: document.request_id, expires_at: document.expires_at },
		{ status: 201 }
	);
};
