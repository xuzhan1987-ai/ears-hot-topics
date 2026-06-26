#!/usr/bin/env python3
"""
Deployment options for HTML file
"""
import requests

# Netlify Drop has been deployed successfully but requires password protection for anonymous users
# The deployed URL is: https://stunning-belekoy-5f8dce.netlify.app
# URL with admin: https://app.netlify.com/sites/stunning-belekoy-5f8dce/overview

print("=" * 60)
print("Netlify Drop Deployment Summary")
print("=" * 60)
print()
print("Deployment URL: https://stunning-belekoy-5f8dce.netlify.app")
print()
print("IMPORTANT: Anonymous Netlify Drop deployments are password protected.")
print("To remove password protection, you need to:")
print("  1. Sign up for a free Netlify account")
print("  2. Claim the deployed site")
print("  3. Go to Site settings > Access control > Password protection")
print("  4. Remove or set your desired password")
print()
print("Alternative: Create a new deployment after signing in")
print()
