#!/usr/bin/env python3
"""
Setup script for Flask backend
"""
import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 Setting up Flask backend...")
    
    # Check if Python is available
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    run_command(f"{python_cmd} -m venv venv")
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("\n📚 Installing dependencies...")
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    print("\n✅ Setup complete!")
    print("\nTo run the Flask backend:")
    if sys.platform == "win32":
        print("1. venv\\Scripts\\activate")
    else:
        print("1. source venv/bin/activate")
    print("2. python app.py")

if __name__ == "__main__":
    main()