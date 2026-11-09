import { SHARED_CONFIG, validateApp } from '@mfe/shared-contracts';
import { formatMoney } from '@studio/platform-kit';

const app = validateApp({ name: 'billing' });
console.log("Billing Sub-Route initialized with system endpoint:", SHARED_CONFIG.apiEndpoint, "billing:", SHARED_CONFIG.billingUrl);

export function renderBilling(containerId) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = `
      <div style="padding: 20px; background: #1e1e24; border-radius: 8px; color: #fff; font-family: sans-serif;">
        <h3 style="color: #4caf50; margin-top: 0;">Billing Component</h3>
        <p>Status: Active</p>
        <p>Test charge: ${formatMoney(1999)}</p>
        <button style="background: #4caf50; border: none; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer;">
          Process Test Payment
        </button>
      </div>
    `;
  }
}
window.MFE_BILLING = { renderBilling, app };
