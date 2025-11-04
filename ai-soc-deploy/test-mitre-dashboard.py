#!/usr/bin/env python3
"""Test script to populate MITRE data and verify dashboard functionality."""

import requests
import json
import time

def test_mitre_dashboard(base_url="http://localhost:5000"):
    """Test MITRE dashboard functionality."""
    
    print("🧪 Testing MITRE Dashboard Functionality")
    print("=" * 50)
    
    # Test 1: Populate MITRE demo data
    print("\n1. Populating MITRE demo data...")
    try:
        response = requests.post(f"{base_url}/api/demo/populate-mitre")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('message', 'MITRE data populated')}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Check MITRE techniques endpoint
    print("\n2. Testing MITRE techniques API...")
    try:
        response = requests.get(f"{base_url}/api/mitre/techniques/")
        if response.status_code == 200:
            data = response.json()
            techniques = data.get('techniques', [])
            print(f"✅ Success: Found {len(techniques)} MITRE techniques")
            
            if techniques:
                print("\nTop 3 MITRE techniques:")
                for i, tech in enumerate(techniques[:3]):
                    print(f"  {i+1}. {tech.get('technique_id', 'Unknown')} - {tech.get('technique_name', 'Unknown')}")
                    print(f"     Tactic: {tech.get('tactic', 'Unknown')} | Detections: {tech.get('detection_count', 0)}")
            else:
                print("⚠️  No MITRE techniques found - check database initialization")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Check dashboard metrics
    print("\n3. Testing dashboard metrics...")
    try:
        response = requests.get(f"{base_url}/api/dashboard/metrics")
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('metrics', {})
            print(f"✅ Success: Dashboard metrics loaded")
            print(f"   Total Alerts: {metrics.get('total_alerts', 0)}")
            print(f"   High Priority: {metrics.get('high_priority_alerts', 0)}")
            print(f"   Active Threats: {metrics.get('active_threats', 0)}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Check system health
    print("\n4. Testing system health...")
    try:
        response = requests.get(f"{base_url}/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: System health check passed")
            print(f"   Mode: {data.get('mode', 'unknown')}")
            print(f"   Status: {data.get('status', 'unknown')}")
            
            aws_integration = data.get('aws_integration', {})
            print(f"   AWS Integration:")
            for service, status in aws_integration.items():
                if isinstance(status, str):
                    print(f"     {service}: {status}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Generate demo alert to trigger MITRE mapping
    print("\n5. Generating demo alert with MITRE mapping...")
    try:
        demo_alert = {
            "alert_id": f"test_mitre_{int(time.time())}",
            "source": "Test_Script",
            "severity": "HIGH",
            "description": "Test alert for MITRE mapping - suspicious login detected",
            "indicators": ["suspicious_login", "failed_auth", "user_creation"]
        }
        
        response = requests.post(f"{base_url}/api/alerts/process", json=demo_alert)
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            print(f"✅ Success: Demo alert processed")
            
            mitre_mapping = result.get('mitre_mapping', [])
            if mitre_mapping:
                print(f"   MITRE Techniques Mapped: {', '.join(mitre_mapping)}")
            else:
                print("   No MITRE techniques mapped")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 MITRE Dashboard Test Complete!")
    print("\nNext steps:")
    print("1. Visit your dashboard: http://localhost:5000/")
    print("2. Look for the MITRE ATT&CK card in the metrics")
    print("3. Check the MITRE techniques section below")
    print("4. Run AWS logging setup: setup-all-logging.bat")

if __name__ == "__main__":
    import sys
    
    # Allow custom URL for testing deployed app
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print(f"Testing MITRE dashboard at: {base_url}")
    test_mitre_dashboard(base_url)