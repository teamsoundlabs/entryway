export function decodeZodErrors(error: unknown): { errors: Record<string, string[]> } {
	if (error && typeof error === 'object' && 'errors' in error) {
		const zodError = error as { errors: { path: (string | number)[]; message: string }[] };
		const formattedErrors: Record<string, string[]> = {};

		for (const err of zodError.errors) {
			const path = err.path.join('.');
			if (!formattedErrors[path]) {
				formattedErrors[path] = [];
			}
			formattedErrors[path].push(err.message);
		}

		return { errors: formattedErrors };
	}

	return { errors: { general: ['An unknown error occurred'] } };
}
