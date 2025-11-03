// Security Operations - Real AI Processing

class SecurityOperations {
    constructor() {
        this.alertQueue = [];
        this.crewStatus = {};
        this.init();
    }

    init() {
        this.loadCrewStatus();
        this.loadAlertQueue();
        this.bindSecurityEvents();
        this.startSecurityMonitoring();
    }

    async loadCrewStatus() {
        try {
            const response = await fetch('/api/crews/status');
            const data = await response.json();
            this.updateCrewStatus(data.crews);
        } catch (error) {
            console.error('Failed to load crew status:', error);
        }
    }

    async loadAlertQueue() {
        try {
            const response = await fetch('/api/alerts/queue');
            const data = await response.json();
            this.updateAlertQueue(data.alerts);
        } catch (error) {
            console.error('Failed to load alert queue:', error);
        }
    }

    async processSecurityAlert(alertData = null) {
        try {
            this.showProcessingStatus('Processing security alert...');
            
            const response = await fetch('/api/alerts/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(alertData || {})
            });
            
            const data = await response.json();
            this.displayAlertResult(data.result);
            this.loadAlertQueue(); // Refresh queue
            
        } catch (error) {
            console.error('Failed to process alert:', error);
            this.showError('alert-processing', 'Failed to process security alert');
        }
    }

    async generateDemoAlerts() {
        try {
            this.showProcessingStatus('Generating demo security alerts...');
            
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
            this.showError('demo-alerts-results', 'Failed to generate demo alerts');
        }
    }

    updateCrewStatus(crews) {
        const container = document.getElementById('crew-status');
        if (!container) return;

        const crewHtml = Object.entries(crews).map(([crewName, status]) => `
            <div class="alert-item">
                <strong>${crewName.replace('_', ' ').toUpperCase()}:</strong> ${status.status}
                <br><small>Processed: ${status.alerts_processed || status.investigations_completed || status.network_events_analyzed || status.endpoints_monitored || 'N/A'}</small>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${Object.keys(crews).length}</div>
                    <div class="metric-label">AI Crews</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">ACTIVE</div>
                    <div class="metric-label">Status</div>
                </div>
            </div>
            <div class="alert-feed">
                ${crewHtml}
            </div>
        `;
    }

    updateAlertQueue(alerts) {
        const container = document.getElementById('alert-queue');
        if (!container) return;

        const alertsHtml = alerts.slice(0, 10).map(alert => `
            <div class="alert-item ${this.getAlertClass(alert.risk_score)}">
                <strong>${alert.alert_type.toUpperCase()}:</strong> Risk ${alert.risk_score}/10
                <br><small>${alert.description}</small>
                <br><small>ID: ${alert.alert_id} | ${alert.timestamp}</small>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">${alerts.length}</div>
                    <div class="metric-label">Total Alerts</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">${alerts.filter(a => a.risk_score >= 7).length}</div>
                    <div class="metric-label">High Risk</div>
                </div>
            </div>
            <div class="alert-feed">
                ${alertsHtml || '<div class="alert-item">No alerts in queue</div>'}
            </div>
        `;
    }

    displayAlertResult(result) {
        const container = document.getElementById('alert-processing');
        if (!container) return;

        container.innerHTML = `
            <div class="alert-item alert-high">
                <strong>Alert Processed:</strong> ${result.alert_id}
                <br><strong>Risk Score:</strong> ${result.risk_score}/10
                <br><strong>Classification:</strong> ${result.threat_classification}
            </div>
            <div class="alert-item">
                <strong>AI Analysis:</strong> ${result.ai_analysis.substring(0, 200)}...
            </div>
            <div class="alert-item">
                <strong>Plain English:</strong> ${result.plain_english}
            </div>
            <div class="alert-item">
                <strong>Recommended Actions:</strong>
                <ul>${result.recommended_actions.map(action => `<li>${action}</li>`).join('')}</ul>
            </div>
        `;
    }

    displayDemoResults(data) {
        const container = document.getElementById('demo-alerts-results');
        if (!container) return;

        const alertsHtml = data.alerts.map(alert => `
            <div class="alert-item ${this.getAlertClass(alert.risk_score)}">
                <strong>${alert.alert_id}:</strong> ${alert.threat_classification}
                <br><small>Risk: ${alert.risk_score}/10 | Processing: ${alert.processing_time}</small>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="alert-item alert-high">
                <strong>Demo Complete:</strong> ${data.message}
            </div>
            ${alertsHtml}
        `;
    }

    getAlertClass(riskScore) {
        if (riskScore >= 8) return 'alert-critical';
        if (riskScore >= 6) return 'alert-high';
        return '';
    }

    showProcessingStatus(message) {
        const containers = ['alert-processing', 'demo-alerts-results'];
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.innerHTML = `<div class="loading"></div> ${message}`;
            }
        });
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="alert-item alert-critical">❌ ${message}</div>`;
        }
    }

    bindSecurityEvents() {
        // Process Alert Button
        const processBtn = document.getElementById('process-alert-btn');
        if (processBtn) {
            processBtn.addEventListener('click', () => this.processSecurityAlert());
        }

        // Generate Demo Alerts Button
        const demoBtn = document.getElementById('generate-demo-btn');
        if (demoBtn) {
            demoBtn.addEventListener('click', () => this.generateDemoAlerts());
        }

        // Refresh Security Status Button
        const refreshBtn = document.getElementById('refresh-security-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadCrewStatus();
                this.loadAlertQueue();
            });
        }
    }

    startSecurityMonitoring() {
        // Auto-refresh every 10 seconds
        setInterval(() => {
            this.loadCrewStatus();
            this.loadAlertQueue();
        }, 10000);
    }
}

// Initialize Security Operations
document.addEventListener('DOMContentLoaded', () => {
    window.securityOps = new SecurityOperations();
});