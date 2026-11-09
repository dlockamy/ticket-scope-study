import { SHARED_CONFIG, validateApp } from '@mfe/shared-contracts';

const app = validateApp({ name: 'reports' });
console.log("Reports Sub-Route initialized with system endpoint:", SHARED_CONFIG.apiEndpoint, "billing:", SHARED_CONFIG.billingUrl);

export function renderReports(containerId) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = `
      <div style="padding: 20px; background: #1e1e24; border-radius: 8px; color: #fff; font-family: sans-serif;">
        <h3 style="color: #4caf50; margin-top: 0;">Reports Component</h3>
        <p>Open invoices: 3</p>
        <button style="background: #4caf50; border: none; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer;">
          Export report
        </button>
      </div>
    `;
  }
}
window.MFE_REPORTS = { renderReports, app };
