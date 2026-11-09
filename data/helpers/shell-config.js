import { SHARED_CONFIG, validateApp } from '@mfe/shared-contracts';

const app = validateApp({ name: 'core-shell' });
export const shellConfig = { app, billingEndpointHint: SHARED_CONFIG.billingUrl };
