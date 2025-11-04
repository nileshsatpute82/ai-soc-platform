# 🚨 Security Incident Generation Commands

## 📋 **Quick Reference Guide**

Use these commands to generate realistic security incidents for testing your AI SOC platform.

---

## 🔥 **Critical Severity Incidents**

### **1. Malware Detection**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "MAL_001",
  "source": "EDR_System",
  "alert_type": "malware",
  "severity": "critical",
  "description": "Advanced persistent threat (APT) malware detected on domain controller",
  "indicators": ["malicious_hash_def456", "lateral_movement", "privilege_escalation", "data_exfiltration"]
}'
```

### **2. Data Breach**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "BREACH_001",
  "source": "DLP_System",
  "alert_type": "data_exfiltration",
  "severity": "critical",
  "description": "Large volume of sensitive customer data accessed and downloaded",
  "indicators": ["bulk_data_access", "external_transfer", "customer_pii", "unauthorized_download"]
}'
```

### **3. Ransomware Attack**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "RANSOM_001",
  "source": "File_Monitor",
  "alert_type": "ransomware",
  "severity": "critical",
  "description": "Mass file encryption detected across multiple servers",
  "indicators": ["file_encryption", "ransom_note", "backup_deletion", "network_share_access"]
}'
```

---

## ⚠️ **High Severity Incidents**

### **4. Network Intrusion**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "NET_001",
  "source": "IDS_System",
  "alert_type": "network_intrusion",
  "severity": "high",
  "description": "Unauthorized access detected from foreign IP address",
  "indicators": ["external_ip_connection", "port_scanning", "vulnerability_exploit", "command_injection"]
}'
```

### **5. Phishing Campaign**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "PHISH_001",
  "source": "Email_Security",
  "alert_type": "phishing",
  "severity": "high",
  "description": "Targeted spear-phishing campaign against executives",
  "indicators": ["credential_harvesting", "executive_targeting", "domain_spoofing", "malicious_links"]
}'
```

### **6. Insider Threat**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "INSIDER_001",
  "source": "UEBA_System",
  "alert_type": "insider_threat",
  "severity": "high",
  "description": "Employee accessing sensitive data outside normal patterns",
  "indicators": ["unusual_data_access", "off_hours_activity", "privilege_abuse", "data_hoarding"]
}'
```

---

## 🟡 **Medium Severity Incidents**

### **7. Suspicious Login**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "LOGIN_001",
  "source": "Identity_System",
  "alert_type": "suspicious_login",
  "severity": "medium",
  "description": "Multiple failed login attempts followed by successful login",
  "indicators": ["brute_force_attempt", "geographic_anomaly", "new_device", "credential_stuffing"]
}'
```

### **8. Policy Violation**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "POLICY_001",
  "source": "Compliance_Monitor",
  "alert_type": "policy_violation",
  "severity": "medium",
  "description": "Unauthorized software installation detected",
  "indicators": ["unapproved_software", "admin_bypass", "policy_breach", "shadow_it"]
}'
```

### **9. Web Application Attack**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "WEB_001",
  "source": "WAF_System",
  "alert_type": "web_attack",
  "severity": "medium",
  "description": "SQL injection attempt detected on customer portal",
  "indicators": ["sql_injection", "input_validation_bypass", "database_probing", "authentication_bypass"]
}'
```

---

## 🟢 **Low Severity Incidents**

### **10. Failed Authentication**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "AUTH_001",
  "source": "AD_Monitor",
  "alert_type": "failed_authentication",
  "severity": "low",
  "description": "Repeated failed authentication attempts from single user",
  "indicators": ["password_spray", "account_lockout", "authentication_failure", "user_error"]
}'
```

### **11. Anomalous Network Traffic**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "TRAFFIC_001",
  "source": "Network_Monitor",
  "alert_type": "network_anomaly",
  "severity": "low",
  "description": "Unusual network traffic pattern detected",
  "indicators": ["bandwidth_spike", "unusual_protocol", "internal_scanning", "dns_tunneling"]
}'
```

---

## 🏛️ **Compliance-Related Incidents**

### **12. RBI Compliance Violation**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "RBI_001",
  "source": "Banking_System",
  "alert_type": "compliance_violation",
  "severity": "high",
  "description": "Customer financial data accessed without proper authorization",
  "indicators": ["data_breach", "customer_data", "unauthorized_access", "financial_records"]
}'
```

### **13. SEBI Compliance Violation**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "SEBI_001",
  "source": "Trading_System",
  "alert_type": "compliance_violation",
  "severity": "high",
  "description": "Unauthorized access to market data and trading algorithms",
  "indicators": ["market_data", "trading_algorithms", "unauthorized_access", "insider_trading"]
}'
```

---

## 🤖 **AI/ML Specific Incidents**

### **14. Model Poisoning**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "AI_001",
  "source": "ML_Monitor",
  "alert_type": "model_attack",
  "severity": "high",
  "description": "Adversarial inputs detected attempting to poison ML model",
  "indicators": ["adversarial_input", "model_drift", "training_data_manipulation", "ai_security"]
}'
```

### **15. API Abuse**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "API_001",
  "source": "API_Gateway",
  "alert_type": "api_abuse",
  "severity": "medium",
  "description": "Excessive API calls detected from single source",
  "indicators": ["rate_limiting_bypass", "api_scraping", "ddos_attempt", "resource_exhaustion"]
}'
```

---

## 🌐 **Cloud-Specific Incidents**

### **16. AWS IAM Compromise**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "AWS_001",
  "source": "CloudTrail",
  "alert_type": "iam_compromise",
  "severity": "critical",
  "description": "Suspicious IAM role assumption and privilege escalation",
  "indicators": ["privilege_escalation", "role_assumption", "aws_compromise", "cloud_attack"]
}'
```

### **17. S3 Bucket Exposure**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/process \
-H "Content-Type: application/json" \
-d '{
  "alert_id": "S3_001",
  "source": "AWS_Config",
  "alert_type": "data_exposure",
  "severity": "high",
  "description": "S3 bucket with sensitive data made publicly accessible",
  "indicators": ["public_bucket", "data_exposure", "misconfiguration", "cloud_security"]
}'
```

---

## 📊 **Batch Generation Commands**

### **Generate Multiple Demo Alerts**
```bash
curl -X POST https://your-app.onrender.com/api/security/demo-alerts
```

### **Analyze Compliance for Test Alert**
```bash
curl -X POST https://your-app.onrender.com/api/alerts/analyze-compliance
```

### **Populate MITRE Techniques with Demo Data**
```bash
curl -X POST https://your-app.onrender.com/api/demo/populate-mitre
```

---

## 🔧 **Testing Commands**

### **Check System Health**
```bash
curl https://your-app.onrender.com/health/
```

### **Get Current Alerts**
```bash
curl https://your-app.onrender.com/api/alerts/
```

### **Get MITRE Techniques**
```bash
curl https://your-app.onrender.com/api/mitre/techniques/
```

### **Get AI Crew Status**
```bash
curl https://your-app.onrender.com/api/crews/status
```

---

## 💡 **Usage Tips**

1. **Replace URL**: Change `https://your-app.onrender.com` to your actual app URL
2. **Customize Data**: Modify alert fields to test specific scenarios
3. **Severity Levels**: Use `critical`, `high`, `medium`, `low`
4. **Alert Types**: Mix different types to test AI classification
5. **Indicators**: Add relevant indicators for better MITRE mapping

## 🎯 **Quick Test Sequence**

Run these commands in order for a comprehensive test:

```bash
# 1. Generate demo alerts
curl -X POST https://your-app.onrender.com/api/security/demo-alerts

# 2. Add MITRE data
curl -X POST https://your-app.onrender.com/api/demo/populate-mitre

# 3. Test compliance
curl -X POST https://your-app.onrender.com/api/alerts/analyze-compliance

# 4. Check results
curl https://your-app.onrender.com/api/alerts/
```

**🚀 Your AI SOC platform will analyze each incident with real AI and provide detailed security insights!**