import { z } from 'zod';

const userSchema = z.object({
	id: z.string(), // Assuming id is a string; change to z.number() if it's a number
	username: z.string().min(1, 'Username is required'),
	display_name: z.string().optional() // Assuming display_name is optional
});

const serverSchema = z.object({
	id: z.string(), // Assuming id is a string; change to z.number() if it's a number
	name: z.string().min(1, 'Server name is required')
});

export const createRequestBody = z.object({
	user: userSchema,
	server: serverSchema
});
