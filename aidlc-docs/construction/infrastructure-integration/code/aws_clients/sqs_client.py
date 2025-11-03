"""AWS SQS message queue handlers with batch processing."""

import boto3
import json
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError
import time

class SQSClient:
    """AWS SQS client with batch processing and error handling."""
    
    def __init__(self, config_service):
        self.config = config_service
        self.sqs = boto3.client(
            'sqs',
            region_name=self.config.get('AWS_REGION', 'us-east-1')
        )
        
        # Queue URLs cache
        self.queue_urls = {}
        self._initialize_queues()
    
    def _initialize_queues(self):
        """Initialize queue URLs."""
        queue_names = [
            'security-alerts-queue',
            'investigation-queue',
            'triage-queue',
            'notification-queue'
        ]
        
        for queue_name in queue_names:
            try:
                response = self.sqs.get_queue_url(QueueName=queue_name)
                self.queue_urls[queue_name] = response['QueueUrl']
            except ClientError:
                # Queue doesn't exist, create it
                self._create_queue(queue_name)
    
    def _create_queue(self, queue_name: str) -> str:
        """Create SQS queue with default attributes."""
        try:
            attributes = {
                'VisibilityTimeoutSeconds': '300',
                'MessageRetentionPeriod': '1209600',  # 14 days
                'DelaySeconds': '0',
                'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
            }
            
            response = self.sqs.create_queue(
                QueueName=queue_name,
                Attributes=attributes
            )
            
            queue_url = response['QueueUrl']
            self.queue_urls[queue_name] = queue_url
            return queue_url
            
        except ClientError as e:
            raise Exception(f"Failed to create queue {queue_name}: {str(e)}")
    
    def send_message(self, queue_name: str, message: Dict[str, Any], delay_seconds: int = 0) -> str:
        """Send single message to queue."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message),
                DelaySeconds=delay_seconds
            )
            
            return response['MessageId']
            
        except ClientError as e:
            raise Exception(f"Failed to send message to {queue_name}: {str(e)}")
    
    def send_batch_messages(self, queue_name: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send batch of messages to queue (max 10 per batch)."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            # SQS batch limit is 10 messages
            batch_size = 10
            results = {"successful": [], "failed": []}
            
            for i in range(0, len(messages), batch_size):
                batch = messages[i:i + batch_size]
                
                entries = []
                for idx, message in enumerate(batch):
                    entries.append({
                        'Id': str(i + idx),
                        'MessageBody': json.dumps(message)
                    })
                
                response = self.sqs.send_message_batch(
                    QueueUrl=queue_url,
                    Entries=entries
                )
                
                results["successful"].extend(response.get('Successful', []))
                results["failed"].extend(response.get('Failed', []))
            
            return results
            
        except ClientError as e:
            raise Exception(f"Failed to send batch messages to {queue_name}: {str(e)}")
    
    def receive_messages(self, queue_name: str, max_messages: int = 1, wait_time: int = 20) -> List[Dict[str, Any]]:
        """Receive messages from queue."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=min(max_messages, 10),  # SQS limit is 10
                WaitTimeSeconds=wait_time,
                AttributeNames=['All']
            )
            
            messages = []
            for message in response.get('Messages', []):
                try:
                    body = json.loads(message['Body'])
                except json.JSONDecodeError:
                    body = message['Body']
                
                messages.append({
                    'message_id': message['MessageId'],
                    'receipt_handle': message['ReceiptHandle'],
                    'body': body,
                    'attributes': message.get('Attributes', {}),
                    'md5_of_body': message.get('MD5OfBody')
                })
            
            return messages
            
        except ClientError as e:
            raise Exception(f"Failed to receive messages from {queue_name}: {str(e)}")
    
    def delete_message(self, queue_name: str, receipt_handle: str) -> bool:
        """Delete message from queue."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            
            return True
            
        except ClientError as e:
            raise Exception(f"Failed to delete message from {queue_name}: {str(e)}")
    
    def delete_batch_messages(self, queue_name: str, receipt_handles: List[str]) -> Dict[str, Any]:
        """Delete batch of messages from queue."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            # SQS batch limit is 10 messages
            batch_size = 10
            results = {"successful": [], "failed": []}
            
            for i in range(0, len(receipt_handles), batch_size):
                batch = receipt_handles[i:i + batch_size]
                
                entries = []
                for idx, receipt_handle in enumerate(batch):
                    entries.append({
                        'Id': str(i + idx),
                        'ReceiptHandle': receipt_handle
                    })
                
                response = self.sqs.delete_message_batch(
                    QueueUrl=queue_url,
                    Entries=entries
                )
                
                results["successful"].extend(response.get('Successful', []))
                results["failed"].extend(response.get('Failed', []))
            
            return results
            
        except ClientError as e:
            raise Exception(f"Failed to delete batch messages from {queue_name}: {str(e)}")
    
    def get_queue_attributes(self, queue_name: str) -> Dict[str, Any]:
        """Get queue attributes and statistics."""
        try:
            queue_url = self.queue_urls.get(queue_name)
            if not queue_url:
                raise Exception(f"Queue {queue_name} not found")
            
            response = self.sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['All']
            )
            
            return response['Attributes']
            
        except ClientError as e:
            raise Exception(f"Failed to get attributes for {queue_name}: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check SQS queues health."""
        try:
            queue_status = {}
            
            for queue_name, queue_url in self.queue_urls.items():
                try:
                    attributes = self.get_queue_attributes(queue_name)
                    queue_status[queue_name] = {
                        "status": "healthy",
                        "messages_available": int(attributes.get('ApproximateNumberOfMessages', 0)),
                        "messages_in_flight": int(attributes.get('ApproximateNumberOfMessagesNotVisible', 0)),
                        "queue_url": queue_url
                    }
                except Exception as e:
                    queue_status[queue_name] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
            
            return {
                "status": "healthy" if all(q["status"] == "healthy" for q in queue_status.values()) else "partial",
                "queues": queue_status
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }