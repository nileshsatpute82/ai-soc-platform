"""
Authentication Manager for Atlas Co-Pilot
Handles LinkedIn OAuth authentication
"""

import os
import json
from flask import session, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
import requests

class User(UserMixin):
    def __init__(self, id, email, name, provider, avatar_url=None):
        self.id = id
        self.email = email
        self.name = name
        self.provider = provider
        self.avatar_url = avatar_url
        
    def get_id(self):
        return f"{self.provider}:{self.id}"

class AuthManager:
    def __init__(self, app=None):
        self.app = app
        self.oauth = None
        self.users = {}  # In-memory user store (use database in production)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        self.oauth = OAuth(app)
        
        # Configure OAuth providers
        self._configure_linkedin()
        
        # Store auth manager in app
        app.auth_manager = self
    
    def _configure_linkedin(self):
        """Configure LinkedIn OAuth"""
        self.linkedin = self.oauth.register(
            name='linkedin',
            client_id=os.getenv('LINKEDIN_CLIENT_ID'),
            client_secret=os.getenv('LINKEDIN_CLIENT_SECRET'),
            authorize_url='https://www.linkedin.com/oauth/v2/authorization',
            access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
            client_kwargs={
                'scope': 'r_liteprofile r_emailaddress'
            }
        )
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def create_or_update_user(self, provider, user_info):
        """Create or update user from OAuth response"""
        if provider == 'linkedin':
            user_id = user_info['id']
            email = user_info['emailAddress']
            name = f"{user_info['firstName']} {user_info['lastName']}"
            avatar_url = user_info.get('profilePicture', {}).get('displayImage')
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Create user object
        user = User(
            id=user_id,
            email=email,
            name=name,
            provider=provider,
            avatar_url=avatar_url
        )
        
        # Store user (in production, save to database)
        full_user_id = user.get_id()
        self.users[full_user_id] = user
        
        return user
    
    def is_configured(self):
        """Check if OAuth is properly configured"""
        linkedin_configured = bool(
            os.getenv('LINKEDIN_CLIENT_ID') and 
            os.getenv('LINKEDIN_CLIENT_SECRET')
        )
        
        return {
            'linkedin': linkedin_configured,
            'any': linkedin_configured
        }
    
    def get_login_url(self, provider):
        """Get OAuth login URL for provider"""
        if provider == 'linkedin':
            return url_for('auth_linkedin_login')
        else:
            return None

# Global auth manager instance
auth_manager = AuthManager()