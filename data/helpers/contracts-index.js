export const SHARED_CONFIG = {
  theme: 'dark',
  apiEndpoint: 'https://homelab.local',
  billingVersion: '1.0.0',
  billingUrl: 'https://homelab.local/billing'
};

export function validateApp(app) {
  if (!app || !app.name) throw new Error('app.name is required');
  return { ...app };
}
