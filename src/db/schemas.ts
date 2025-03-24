import mongoose, { Schema, Document } from 'mongoose';
import { v4 as uuidv4 } from 'uuid';

interface User {
	username: string;
	display_name: string;
	id: string;
}

interface Server {
	id: string;
	name: string;
}

interface Request extends Document {
	request_id: string;
	user: User;
	server: Server;
	created_at: Date;
	expires_at: Date;
	state: 'uncompleted' | 'completed';
}

const UserSchema = new Schema<User>({
	username: { type: String, required: true },
	display_name: { type: String, required: true },
	id: { type: String, required: true }
});

const ServerSchema = new Schema<Server>({
	id: { type: String, required: true },
	name: { type: String, required: true }
});

const RequestSchema = new Schema<Request>({
	request_id: { type: String, default: uuidv4 },
	user: { type: UserSchema, required: true },
	server: { type: ServerSchema, required: true },
	created_at: { type: Date, default: () => new Date() },
	expires_at: { type: Date, default: () => new Date(Date.now() + 15 * 60 * 1000) },
	state: { type: String, enum: ['uncompleted', 'completed'], default: 'uncompleted' }
});

export default mongoose.models.verification_requests ||
	mongoose.model('verification_requests', RequestSchema);
