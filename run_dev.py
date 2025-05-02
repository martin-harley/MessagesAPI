import subprocess
import sys
import os
import webbrowser
from time import sleep

def run_services():
    # Define commands for running both services
    if sys.platform.startswith('win'):
        backend_cmd = 'cd server && python -m flask --app main run'
        frontend_cmd = 'cd client && npm run dev -- --port 3000'
    else:
        backend_cmd = 'cd server && python3 -m flask --app main run'
        frontend_cmd = 'cd client && npm run dev -- --port 3000'

    try:
        # Start the Flask backend
        print("Starting Flask backend...")
        backend_process = subprocess.Popen(backend_cmd, shell=True)
        
        # Give the backend a moment to start
        sleep(2)
        
        # Start the Vue.js frontend
        print("Starting Vue.js frontend...")
        frontend_process = subprocess.Popen(frontend_cmd, shell=True)
        
        # Wait a few seconds for the frontend to start
        sleep(5)
        
        # Open the application in the default browser
        webbrowser.open('http://localhost:3000')
        
        print("\nDevelopment servers are running!")
        print("Backend: http://localhost:5000")
        print("Frontend: http://localhost:3000")
        print("\nPress Ctrl+C to stop both servers...")
        
        # Keep the script running until interrupted
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down development servers...")
        # Kill both processes
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Ensure processes are terminated in case of other errors
        try:
            backend_process.terminate()
            frontend_process.terminate()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    run_services() 