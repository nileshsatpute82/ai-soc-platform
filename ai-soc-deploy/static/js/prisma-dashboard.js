// Prisma-style Dashboard JavaScript

class PrismaDashboard {
    constructor() {
        this.alertCount = 0;
        this.crewStatus = {};
        this.alertQueue = [];
        this.init();
    }

    init() {
        this.loadInitialData();
        this.bindEvents();
        this.startAutoRefresh();
    }

    async loadInitialData() {
        await Promise.all([
            this.loadSystemHealth(),
            this.loadCrewStatus(),
            this.loadAlertQueue()
        ]);
    }

    async loadSystemHealth() {
        try {
            const response = await fetch('/health/');
            const data = await response.json();
            this.updateSystemHealth(data);
        } catch (error) {
            console.error('Failed to load system health:', error);
            this.showError('system-health-content', 'Failed to load system health');
        }
    }

    async loadCrewStatus() {
        try {
            const response = await fetch('/api/crews/status');
            const data = await response.json();
            this.crewStatus = data.crews || {};
            this.updateCrewStatus(data.crews || {});
        } catch (error) {
            console.error('Failed to load crew status:', error);
            this.showError('crew-status-content', 'Failed to load crew status');
        }
    }

    async loadAlertQueue() {
        try {
            const response = await fetch('/api/alerts/queue');
            const data = await response.json();
            this.alertQueue = data.alerts || [];
            this.updateAlertQueue(data.alerts || []);
            this.updateAlertCount(data.alerts?.length || 0);
        } catch (error) {
            console.error('Failed to load alert queue:', error);
            this.showError('alert-queue-content', 'Failed to load alert queue');
        }
    }

    async processSecurityAlert() {
        try {
            this.showProcessing('alert-processing-results', 'Processing security alert with AI...');
            
            const response = await fetch('/api/alerts/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            this.displayAlertResult(data.result);
            this.loadAlertQueue(); // Refresh queue
            
        } catch (error) {
            console.error('Failed to process alert:', error);
            this.showError('alert-processing-results', 'Failed to process security alert');
        }
    }

    async generateDemoAlerts() {
        try {
            this.showProcessing('alert-processing-results', 'Generating realistic security scenarios...');
            
            const response = await fetch('/api/security/demo-alerts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });
            
            const data = await response.json();
            this.displayDemoResults(data);
            this.loadAlertQueue(); // Refresh queue
            this.loadCrewStatus(); // Refresh crew status
            
        } catch (error) {
            console.error('Failed to generate demo alerts:', error);
            this.showError('alert-processing-results', 'Failed to generate demo alerts');
        }
    }

    updateSystemHealth(data) {
        const container = document.getElementById('system-health-content');
        if (!container) return;

        const components = Object.entries(data.components || {});
        const healthyCount = components.filter(([_, status]) => status.status === 'healthy').length;
        
        const healthHtml = components.map(([name, status]) => `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">${this.formatComponentName(name)}</div>
                    <div class="row-subtitle">${status.mode ? `Mode: ${status.mode}` : 'System component'}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${status.status === 'healthy' ? 'risk-low' : 'risk-critical'}">
                        ${status.status.toUpperCase()}
                    </span>
                </div>
            </div>
        `).join('');

        container.innerHTML = healthHtml || `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">System Status: ${data.status}</div>
                    <div class="row-subtitle">${healthyCount}/${components.length} components healthy</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${data.status === 'healthy' ? 'risk-low' : 'risk-critical'}">
                        ${data.status.toUpperCase()}
                    </span>
                </div>
            </div>
        `;
    }

    updateCrewStatus(crews) {
        const container = document.getElementById('crew-status-content');
        if (!container) return;

        const crewHtml = Object.entries(crews).map(([crewName, status]) => `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">${this.formatCrewName(crewName)}</div>
                    <div class="row-subtitle">${this.getCrewDescription(crewName, status)}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${status.status === 'active' ? 'risk-low' : 'risk-warning'}">
                        ${status.status.toUpperCase()}
                    </span>
                </div>
            </div>
        `).join('');

        container.innerHTML = crewHtml || `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">No crew data available</div>
                    <div class="row-subtitle">Unable to load AI crew status</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge risk-critical">OFFLINE</span>
                </div>
            </div>
        `;
    }

    updateAlertQueue(alerts) {
        const container = document.getElementById('alert-queue-content');
        if (!container) return;

        if (!alerts || alerts.length === 0) {
            container.innerHTML = `
                <div class="table-row">
                    <div class="row-main">
                        <div class="row-title">No alerts in queue</div>
                        <div class="row-subtitle">All security alerts have been processed</div>
                    </div>
                    <div class="row-meta">
                        <span class="risk-badge risk-low">CLEAR</span>
                    </div>
                </div>
            `;
            return;
        }

        const alertHtml = alerts.slice(0, 10).map(alert => `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">${alert.alert_type.replace('_', ' ').toUpperCase()}: ${alert.description}</div>
                    <div class="row-subtitle">ID: ${alert.alert_id} | ${new Date(alert.timestamp).toLocaleString()}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${this.getRiskClass(alert.risk_score)}">
                        RISK ${alert.risk_score}/10
                    </span>
                </div>
            </div>
        `).join('');

        container.innerHTML = alertHtml;
    }

    updateAlertCount(count) {
        const element = document.getElementById('active-alerts');
        if (element) {
            element.textContent = count;
        }
        this.alertCount = count;
    }

    displayAlertResult(result) {
        const container = document.getElementById('alert-processing-results');
        if (!container) return;

        container.innerHTML = `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">Alert Processed: ${result.alert_id}</div>
                    <div class="row-subtitle">${result.threat_classification}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${this.getRiskClass(result.risk_score)}">
                        RISK ${result.risk_score}/10
                    </span>
                </div>
            </div>
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">AI Analysis Complete</div>
                    <div class="row-subtitle">${result.plain_english}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge risk-low">ANALYZED</span>
                </div>
            </div>
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">Recommended Actions</div>
                    <div class="row-subtitle">${result.recommended_actions.slice(0, 2).join(', ')}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge risk-medium">ACTION REQUIRED</span>
                </div>
            </div>
        `;
    }

    displayDemoResults(data) {
        const container = document.getElementById('alert-processing-results');
        if (!container) return;

        const alertsHtml = data.alerts.slice(0, 3).map(alert => `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">${alert.alert_id}: ${alert.threat_classification}</div>
                    <div class="row-subtitle">Processing time: ${alert.processing_time}</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge ${this.getRiskClass(alert.risk_score)}">
                        RISK ${alert.risk_score}/10
                    </span>
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="table-row">
                <div class="row-main">
                    <div class="row-title">Demo Complete: ${data.message}</div>
                    <div class="row-subtitle">Generated and processed ${data.alerts.length} realistic security scenarios</div>
                </div>
                <div class="row-meta">
                    <span class="risk-badge risk-low">SUCCESS</span>
                </div>
            </div>
            ${alertsHtml}
        `;
    }

    showProcessing(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="table-row">
                    <div class="row-main">
                        <div class="row-title">${message}</div>
                        <div class="row-subtitle">Please wait while AI processes the request...</div>
                    </div>
                    <div class="row-meta">
                        <span class="loading-spinner"></span>
                    </div>
                </div>
            `;
        }
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="table-row">
                    <div class="row-main">
                        <div class="row-title">Error</div>
                        <div class="row-subtitle">${message}</div>
                    </div>
                    <div class="row-meta">
                        <span class="risk-badge risk-critical">ERROR</span>
                    </div>
                </div>
            `;
        }
    }

    formatComponentName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatCrewName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    getCrewDescription(crewName, status) {
        const descriptions = {
            'triage_crew': `Processed ${status.alerts_processed || 0} alerts with ${status.accuracy || 'N/A'} accuracy`,
            'investigation_crew': `Completed ${status.investigations_completed || 0} investigations in avg ${status.avg_investigation_time || 'N/A'}`,
            'network_security_crew': `Analyzed ${status.network_events_analyzed || 0} network events, blocked ${status.threats_blocked || 0} threats`,
            'endpoint_security_crew': `Monitoring ${status.endpoints_monitored || 0} endpoints, ${status.quarantine_success || 'N/A'} quarantine success`
        };
        return descriptions[crewName] || 'AI security crew operational';
    }

    getRiskClass(riskScore) {
        if (riskScore >= 8) return 'risk-critical';
        if (riskScore >= 6) return 'risk-high';
        if (riskScore >= 4) return 'risk-medium';
        return 'risk-low';
    }

    bindEvents() {
        // Process Alert Button
        const processBtn = document.getElementById('process-alert-btn');
        if (processBtn) {
            processBtn.addEventListener('click', () => this.processSecurityAlert());
        }

        // Generate Demo Button
        const demoBtn = document.getElementById('generate-demo-btn');
        if (demoBtn) {
            demoBtn.addEventListener('click', () => this.generateDemoAlerts());
        }

        // Refresh Buttons
        const refreshQueueBtn = document.getElementById('refresh-queue-btn');
        if (refreshQueueBtn) {
            refreshQueueBtn.addEventListener('click', () => this.loadAlertQueue());
        }

        const refreshCrewsBtn = document.getElementById('refresh-crews-btn');
        if (refreshCrewsBtn) {
            refreshCrewsBtn.addEventListener('click', () => this.loadCrewStatus());
        }

        const healthCheckBtn = document.getElementById('health-check-btn');
        if (healthCheckBtn) {
            healthCheckBtn.addEventListener('click', () => this.loadSystemHealth());
        }
    }

    startAutoRefresh() {
        // Auto-refresh every 15 seconds
        setInterval(() => {
            this.loadAlertQueue();
            this.loadCrewStatus();
        }, 15000);

        // Health check every 30 seconds
        setInterval(() => {
            this.loadSystemHealth();
        }, 30000);
    }
}

// Initialize Prisma Dashboard
document.addEventListener('DOMContentLoaded', () => {
    new PrismaDashboard();
});