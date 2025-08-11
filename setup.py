#!/usr/bin/env python3
"""
Setup script for AI Doppelgänger Engine
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "models", 
        "logs",
        "dashboard/dist"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def setup_environment():
    """Set up environment configuration"""
    env_file = Path(".env")
    env_example = Path("config.env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("📝 Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ Could not find environment template")

def main():
    """Main setup function"""
    print("🧠 AI Doppelgänger Engine Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup environment
    print("\n⚙️ Setting up environment...")
    setup_environment()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python app.py")
    print("3. Open http://localhost:8000 in your browser")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 