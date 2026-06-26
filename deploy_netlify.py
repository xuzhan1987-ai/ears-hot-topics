#!/usr/bin/env python3
"""
Netlify Drop Anonymous Deploy Script
Uses Netlify's API for anonymous file deployment
"""
import requests
import json
import os
import base64
import hashlib

# Read the HTML file
html_path = "/app/data/所有对话/主对话/hot_web/index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Calculate file hash
file_hash = hashlib.md5(html_content.encode()).hexdigest()

# Netlify Drop uses the deploy API
# First, we need to get a deploy token
# The API endpoint for anonymous drops

# Try using the Netlify API directly
# According to Netlify docs, anonymous drops use a specific endpoint

# Let's try the Netlify CLI API approach
# POST to https://api.netlify.com/api/v1/sites (anonymous)

print("Attempting anonymous deployment to Netlify...")

# Method 1: Try direct API call
api_url = "https://api.netlify.com/api/v1/sites"

try:
    # Create site without authentication (anonymous)
    response = requests.post(
        api_url,
        headers={
            "Content-Type": "application/zip",
        },
        data=html_content.encode(),
        timeout=30
    )
    print(f"API Response status: {response.status_code}")
    print(f"Response: {response.text[:500] if response.text else 'Empty'}")
except Exception as e:
    print(f"Error: {e}")

print("\nTrying alternative approach with zip upload...")

# Method 2: Create a proper zip and upload
import zipfile
import io

# Create zip in memory
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.writestr('index.html', html_content)
zip_buffer.seek(0)
zip_content = zip_buffer.read()

# Try uploading zip
try:
    response = requests.post(
        api_url,
        headers={
            "Content-Type": "application/zip",
        },
        data=zip_content,
        timeout=30
    )
    print(f"Zip API Response status: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"Site URL: {data.get('url', 'No URL')}")
        print(f"Admin URL: {data.get('admin_url', 'No admin URL')}")
    else:
        print(f"Response: {response.text[:500] if response.text else 'Empty'}")
except Exception as e:
    print(f"Error: {e}")

print("\nDone.")
