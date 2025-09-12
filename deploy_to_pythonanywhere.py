#!/usr/bin/env python3
"""
Quick deployment script for PythonAnywhere
Run this after uploading files to update the live site
"""

import os
import subprocess

def run_command(command):
    """Run a command and print the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Success")
        if result.stdout:
            print(result.stdout)
    else:
        print("✗ Error")
        print(result.stderr)
    return result.returncode == 0

def main():
    print("🚀 Deploying to PythonAnywhere...")
    
    # Change to project directory
    os.chdir('/home/henryenyi/medical_lab_project')
    
    # Run migrations
    print("\n📊 Running database migrations...")
    run_command('python manage.py migrate')
    
    # Create sample blog posts
    print("\n📝 Creating sample blog posts...")
    run_command('python manage.py create_sample_posts')
    
    # Collect static files
    print("\n📁 Collecting static files...")
    run_command('python manage.py collectstatic --noinput')
    
    print("\n✅ Deployment complete!")
    print("Don't forget to reload your web app in the PythonAnywhere dashboard!")

if __name__ == "__main__":
    main()