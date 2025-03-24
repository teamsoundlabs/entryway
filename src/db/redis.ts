import { REDIS_URI } from '$env/static/private';
import Redis from 'ioredis';

const redis = new Redis(REDIS_URI);

export default redis;