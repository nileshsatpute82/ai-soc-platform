// AI Security Operations Dashboard - JavaScript

class SecurityDashboard {
    constructor() {
        this.apiBase = '';
        this.refreshInterval = 5000; // 5 seconds
        this.init();
    }

    init() {
        this.loadSystemHealth();
        this.loadConfiguration();
        this.loadMitreTechniques();
        this.loadAuditEvents();
        this.startAutoRefresh();
        this.bindEvents();
    }

    async loadSystemHealth() {
        try {
            const response = await fetch('/health/');
            const data = await response.json();
            this.updateHealthStatus(data);
        } catch (error) {
            console.error('Failed to load system health:', error);
            this.showError('health-status', 'Failed to load system health');
        }
    }

    async loadConfiguration() {
        try {
            const response = await fetch('/api/config/');
            const data = await response.json();
            this.updateConfiguration(data);
        } catch (error) {
            console.error('Failed to load configuration:', error);
            this.showError('config-status', 'Failed to load configuration');
        }
    }

    async loadMitreTechniques() {
        try {
            const response = await fetch('/api/mitre/techniques');
            const data = await response.json();
            this.updateMitreTechniques(data);
        } catch (error) {
            console.error('Failed to load MITRE techniques:', error);
            this.showError('mitre-status', 'Failed to load MITRE data');
        }
    }

    async loadAuditEvents() {
        try {
            const response = await fetch('/api/audit/events');
            const data = await response.json();
            this.updateAuditEvents(data);
        } catch (error) {
            console.error('Failed to load audit events:', error);
            this.showError('audit-status', 'Failed to load audit events');
        }
    }

    async runDemo() {
        try {
            this.showLoading('demo-results');
            const response = await fetch('/demo/');
            const data = await response.json();
            this.updateDemoResults(data);
        } catch (error) {
            console.error('Failed to run demo:', error);
            this.showError('demo-results', 'Failed to run demo operations');
        }
    }

    updateHealthStatus(data) {
        const container = document.getElementById('health-status');
        if (!container) return;

        const healthHtml = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${data.status === 'healthy' ? '✅' : '❌'}</div>
                    <div class="metric-label">System Status</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">${Object.keys(data.components || {}).length}</div>
                    <div class="metric-label">Components</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">${data.mode || 'Unknown'}</div>
                    <div class="metric-label">Mode</div>
                </div>
            </div>
            <div class="alert-feed">
                ${Object.entries(data.components || {}).map(([name, status]) => `
                    <div class="alert-item ${status.status === 'healthy' ? '' : 'alert-critical'}">
                        <strong>${name}:</strong> ${status.status} ${status.mode ? `(${status.mode})` : ''}
                    </div>
                `).join('')}
            </div>
        `;
        container.innerHTML = healthHtml;
    }

    updateConfiguration(data) {
        const container = document.getElementById('config-status');
        if (!container) return;

        const configHtml = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${Object.keys(data.config || {}).length}</div>
                    <div class="metric-label">Config Items</div>
                </div>
            </div>
            <div class="alert-feed">
                ${Object.entries(data.config || {}).map(([key, value]) => `
                    <div class="alert-item">
                        <strong>${key}:</strong> ${value}
                    </div>
                `).join('')}
            </div>
        `;
        container.innerHTML = configHtml;
    }

    updateMitreTechniques(data) {
        const container = document.getElementById('mitre-status');
        if (!container) return;

        const mitreHtml = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${data.count || 0}</div>
                    <div class="metric-label">Techniques</div>
                </div>
            </div>
            <div class="alert-feed">
                ${(data.techniques || []).map(technique => `
                    <div class="alert-item">
                        <strong>${technique.id}:</strong> ${technique.name}
                        <br><small>Tactic: ${technique.tactic}</small>
                    </div>
                `).join('')}
            </div>
        `;
        container.innerHTML = mitreHtml;
    }

    updateAuditEvents(data) {
        const container = document.getElementById('audit-status');
        if (!container) return;

        const auditHtml = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${data.count || 0}</div>
                    <div class="metric-label">Events</div>
                </div>
            </div>
            <div class="alert-feed">
                ${(data.events || []).map(event => `
                    <div class="alert-item">
                        <strong>${event.event_type}:</strong> ${event.severity}
                        <br><small>${event.timestamp}</small>
                    </div>
                `).join('')}
            </div>
        `;
        container.innerHTML = auditHtml;
    }

    updateDemoResults(data) {
        const container = document.getElementById('demo-results');
        if (!container) return;

        const demoHtml = `
            <div class="alert-item alert-high">
                <strong>Demo Complete:</strong> ${data.message}
            </div>
            <div class="alert-item">
                <strong>AI Analysis:</strong> ${JSON.stringify(data.operations.ai_analysis)}
            </div>
            <div class="alert-item">
                <strong>MITRE Mapping:</strong> ${data.operations.mitre_mapping.techniques.length} techniques mapped
            </div>
        `;
        container.innerHTML = demoHtml;
    }

    showLoading(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '<div class="loading"></div> Loading...';
        }
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="alert-item alert-critical">❌ ${message}</div>`;
        }
    }

    bindEvents() {
        // Demo button
        const demoBtn = document.getElementById('run-demo-btn');
        if (demoBtn) {
            demoBtn.addEventListener('click', () => this.runDemo());
        }

        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshAll());
        }
    }

    refreshAll() {
        this.loadSystemHealth();
        this.loadConfiguration();
        this.loadMitreTechniques();
        this.loadAuditEvents();
    }

    startAutoRefresh() {
        setInterval(() => {
            this.loadSystemHealth();
            this.loadAuditEvents();
        }, this.refreshInterval);
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new SecurityDashboard();
});