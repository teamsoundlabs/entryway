import { sequence } from '@sveltejs/kit/hooks';
import { handleErrorWithSentry, sentryHandle } from '@sentry/sveltekit';
import * as Sentry from '@sentry/sveltekit';
import mongoose from 'mongoose';
import { MONGODB_URI } from '$env/static/private';

Sentry.init({
	dsn: 'https://95b36026d43bf617d595fe8344f20a60@o4508821281636352.ingest.de.sentry.io/4509028061610064',

	tracesSampleRate: 1.0,

	spotlight: import.meta.env.DEV
});

await mongoose.connect(MONGODB_URI);

// If you have custom handlers, make sure to place them after `sentryHandle()` in the `sequence` function.
export const handle = sequence(sentryHandle());

// If you have a custom error handler, pass it to `handleErrorWithSentry`
export const handleError = handleErrorWithSentry();
