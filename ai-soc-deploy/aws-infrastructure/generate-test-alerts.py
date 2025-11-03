#!/usr/bin/env python3
"""Generate test security alerts for the AI SOC platform."""

import boto3
import json
import time
import datetime
from typing import Dict, Any

class SecurityAlertGenerator:
    def __init__(self, region='us-east-1'):
        self.sns = boto3.client('sns', region_name=region)
        self.region = region
        
    def get_topic_arn(self) -> str:
        """Get SNS topic ARN from CloudFormation stack."""
        cf = boto3.client('cloudformation', region_name=self.region)
        try:
            response = cf.describe_stacks(StackName='ai-soc-platform-infrastructure')
            outputs = response['Stacks'][0]['Outputs']
            for output in outputs:
                if output['OutputKey'] == 'SNSTopicArn':
                    return output['OutputValue']
        except Exception as e:
            print(f"Error getting topic ARN: {e}")
            return None
    
    def generate_failed_login_alert(self) -> Dict[str, Any]:
        """Generate a failed login security alert."""
        return {
            "version": "0",
            "id": f"failed-login-{int(time.time())}",
            "detail-type": "AWS Console Sign In via CloudTrail",
            "source": "aws.signin",
            "account": "123456789012",
            "time": datetime.datetime.now().isoformat(),
            "region": self.region,
            "detail": {
                "eventVersion": "1.05",
                "userIdentity": {
                    "type": "IAMUser",
                    "principalId": "AIDACKCEVSQ6C2EXAMPLE",
                    "arn": "arn:aws:iam::123456789012:user/suspicious-user",
                    "accountId": "123456789012",
                    "userName": "suspicious-user"
                },
                "eventTime": datetime.datetime.now().isoformat(),
                "eventSource": "signin.amazonaws.com",
                "eventName": "ConsoleLogin",
                "awsRegion": self.region,
                "sourceIPAddress": "203.0.113.12",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "errorCode": "SigninFailure",
                "errorMessage": "Failed authentication",
                "responseElements": {"ConsoleLogin": "Failure"},
                "additionalEventData": {
                    "LoginTo": "https://console.aws.amazon.com/console/home",
                    "MobileVersion": "No",
                    "MFAUsed": "No"
                }
            }
        }
    
    def generate_root_usage_alert(self) -> Dict[str, Any]:
        """Generate a root account usage alert."""
        return {
            "version": "0",
            "id": f"root-usage-{int(time.time())}",
            "detail-type": "AWS Console Sign In via CloudTrail",
            "source": "aws.signin",
            "account": "123456789012",
            "time": datetime.datetime.now().isoformat(),
            "region": self.region,
            "detail": {
                "eventVersion": "1.05",
                "userIdentity": {
                    "type": "Root",
                    "principalId": "123456789012",
                    "arn": "arn:aws:iam::123456789012:root",
                    "accountId": "123456789012"
                },
                "eventTime": datetime.datetime.now().isoformat(),
                "eventSource": "signin.amazonaws.com",
                "eventName": "ConsoleLogin",
                "awsRegion": self.region,
                "sourceIPAddress": "198.51.100.14",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "responseElements": {"ConsoleLogin": "Success"},
                "additionalEventData": {
                    "LoginTo": "https://console.aws.amazon.com/console/home",
                    "MobileVersion": "No",
                    "MFAUsed": "Yes"
                }
            }
        }
    
    def generate_iam_changes_alert(self) -> Dict[str, Any]:
        """Generate an IAM changes alert."""
        return {
            "version": "0",
            "id": f"iam-changes-{int(time.time())}",
            "detail-type": "AWS API Call via CloudTrail",
            "source": "aws.iam",
            "account": "123456789012",
            "time": datetime.datetime.now().isoformat(),
            "region": self.region,
            "detail": {
                "eventVersion": "1.05",
                "userIdentity": {
                    "type": "IAMUser",
                    "principalId": "AIDACKCEVSQ6C2EXAMPLE",
                    "arn": "arn:aws:iam::123456789012:user/admin-user",
                    "accountId": "123456789012",
                    "userName": "admin-user"
                },
                "eventTime": datetime.datetime.now().isoformat(),
                "eventSource": "iam.amazonaws.com",
                "eventName": "CreateUser",
                "awsRegion": self.region,
                "sourceIPAddress": "192.0.2.1",
                "userAgent": "aws-cli/2.0.0",
                "requestParameters": {
                    "userName": "new-suspicious-user"
                },
                "responseElements": {
                    "user": {
                        "path": "/",
                        "userName": "new-suspicious-user",
                        "userId": "AIDACKCEVSQ6C2NEWUSER",
                        "arn": "arn:aws:iam::123456789012:user/new-suspicious-user"
                    }
                }
            }
        }
    
    def send_alert(self, alert: Dict[str, Any], topic_arn: str) -> bool:
        """Send alert to SNS topic."""
        try:
            response = self.sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(alert),
                Subject=f"Security Alert: {alert['detail-type']}"
            )
            print(f"✅ Alert sent: {alert['detail-type']} (MessageId: {response['MessageId']})")
            return True
        except Exception as e:
            print(f"❌ Failed to send alert: {e}")
            return False
    
    def generate_test_alerts(self):
        """Generate and send test security alerts."""
        topic_arn = self.get_topic_arn()
        if not topic_arn:
            print("❌ Could not find SNS topic ARN. Make sure infrastructure is deployed.")
            return
        
        print(f"🎯 Sending test alerts to: {topic_arn}")
        
        # Generate different types of alerts
        alerts = [
            ("Failed Login", self.generate_failed_login_alert()),
            ("Root Account Usage", self.generate_root_usage_alert()),
            ("IAM Changes", self.generate_iam_changes_alert())
        ]
        
        for alert_name, alert_data in alerts:
            print(f"\n📡 Generating {alert_name} alert...")
            success = self.send_alert(alert_data, topic_arn)
            if success:
                print(f"   Alert will appear in your platform within 30 seconds")
            time.sleep(2)  # Small delay between alerts
        
        print(f"\n🎉 Test alerts generated! Check your platform at /alerts/ endpoint")

if __name__ == "__main__":
    generator = SecurityAlertGenerator()
    generator.generate_test_alerts()