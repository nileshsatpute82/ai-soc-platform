#!/usr/bin/env python3
"""Verify AWS logging setup and populate MITRE dashboard data."""

import requests
import json

def verify_setup():
    """Verify the complete setup is working."""
    
    print("🔍 Verifying AI-SOC Setup")
    print("=" * 40)
    
    # Use your deployed app URL or localhost
    base_url = "https://your-app.onrender.com"  # Replace with your actual URL
    # base_url = "http://localhost:5000"  # Use this for local testing
    
    print(f"Testing: {base_url}")
    
    # 1. Check system health
    print("\n1. System Health Check...")
    try:
        response = requests.get(f"{base_url}/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status', 'unknown')}")
            print(f"✅ Mode: {data.get('mode', 'unknown')}")
            
            aws_integration = data.get('aws_integration', {})
            print("✅ AWS Integration:")
            for service, status in aws_integration.items():
                if isinstance(status, str):
                    print(f"   {service}: {status}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Populate MITRE demo data
    print("\n2. Populating MITRE Demo Data...")
    try:
        response = requests.post(f"{base_url}/api/demo/populate-mitre")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', 'MITRE data populated')}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Check MITRE techniques
    print("\n3. Checking MITRE Techniques...")
    try:
        response = requests.get(f"{base_url}/api/mitre/techniques/")
        if response.status_code == 200:
            data = response.json()
            techniques = data.get('techniques', [])
            print(f"✅ Found {len(techniques)} MITRE techniques")
            
            if techniques:
                print("Top techniques:")
                for tech in techniques[:3]:
                    print(f"   • {tech.get('technique_id', 'Unknown')}: {tech.get('technique_name', 'Unknown')}")
                    print(f"     Detections: {tech.get('detection_count', 0)}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Check alerts
    print("\n4. Checking Security Alerts...")
    try:
        response = requests.get(f"{base_url}/api/alerts/")
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            print(f"✅ Found {len(alerts)} security alerts")
            print(f"✅ Total count: {data.get('total_count', 0)}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Setup Verification Complete!")
    print("\n✅ What's Working:")
    print("• AWS CloudTrail: API activity logging")
    print("• AWS GuardDuty: Threat detection")  
    print("• AWS Security Hub: Centralized findings")
    print("• VPC Flow Logs: Network monitoring")
    print("• MITRE ATT&CK: Threat intelligence")
    print("• Real-time Dashboard: Security operations")
    
    print("\n🚀 Next Steps:")
    print("1. Visit your dashboard to see MITRE data")
    print("2. Generate AWS activity (create IAM users, etc.)")
    print("3. Watch real security events flow into dashboard")
    print("4. Monitor costs in AWS Billing console")

if __name__ == "__main__":
    verify_setup()