import os
import sys
import time
import subprocess
import webbrowser

def print_banner():
    banner = """
========================================================================
             AEGIS CI: Autonomous Self-Healing CI/CD Agent
========================================================================
    A Next.js full-stack platform coordinating specialized AI agents
    to autonomously fix failing codebases inside sandboxed runtimes.
========================================================================
    """
    print(banner)

def main():
    print_banner()
    
    # 1. Install packages if node_modules doesn't exist
    if not os.path.exists('node_modules'):
        print("[*] node_modules not found. Installing packages...")
        try:
            subprocess.run("npm install", shell=True, check=True)
            print("[OK] Packages installed successfully.")
        except Exception as e:
            print(f"[ERROR] Error installing node modules: {e}")
            sys.exit(1)
            
    # 2. Setup .env if missing
    if not os.path.exists('.env'):
        print("[*] Creating default local .env configuration...")
        with open('.env', 'w') as f:
            f.write('DATABASE_URL="file:./dev.db"\n')
            f.write('BETTER_AUTH_SECRET="hF9kZ5mX3rW1vP7sN9qD4tY2uA8iC0oE1bV5xZ8j"\n')
            f.write('BETTER_AUTH_URL="http://localhost:3000"\n')
            f.write('GEMINI_API_KEY=""\n')

    # 3. Initialize Prisma DB if dev.db does not exist
    if not os.path.exists('prisma/dev.db') and not os.path.exists('dev.db'):
        print("[*] Initializing local SQLite database with Prisma...")
        subprocess.run("npx prisma db push", shell=True, check=False)

    # 4. Check for Gemini Key
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key:
        print("[!] Note: GEMINI_API_KEY environment variable is not set.")
        print("    You can run preset demos in Simulation Mode right away, or")
        print("    enter your Gemini API key in the UI settings (⚙️) anytime.")
        print()
    else:
        print("[OK] GEMINI_API_KEY environment variable detected.")

    # 5. Create temp workspaces folder
    os.makedirs('temp-workspaces', exist_ok=True)
    
    # 4. Start Next.js Development Server
    print("[*] Booting Next.js development server...")
    try:
        # Run npm run dev
        process = subprocess.Popen("npm run dev", shell=True)
        
        # Give next.js dev server 3 seconds to spin up
        time.sleep(3)
        
        # 5. Open browser
        url = "http://localhost:3000"
        print(f"[OK] Server started! Opening dashboard in browser: {url}")
        webbrowser.open(url)
        
        # Keep python running to allow terminal output monitoring
        process.wait()
    except KeyboardInterrupt:
        print("\n[!] Shutting down development server...")
    except Exception as e:
        print(f"[ERROR] Failed to launch server: {e}")

if __name__ == "__main__":
    main()
