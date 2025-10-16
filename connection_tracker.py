# Connection Tracker
# This application tracks active network connections on the system

import subprocess, json
from datetime import datetime

def get_active_connections():
    """Get all active network connections."""
    print("Fetching active network connections... Be patient, this may take a moment.")
    results = subprocess.run(['lsof', '-i', '-P', '-n'], capture_output=True, text=True)
    lines = results.stdout.strip().split('\n')[1:]

    connections = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 9:
            connections.append({
                'process': parts[0],
                'pid': parts[1],
                'local_address': parts[8].split('->')[0].split(':')[0],
                'local_port': parts[8].split('->')[0].split(':')[1] if ':' in parts[8].split('->')[0] else '',
                'remote_address': parts[8].split('->')[1].split(':')[0] if len(parts[8].split('->')) > 1 else '',
                'remote_port': parts[8].split('->')[1].split(':')[1] if len(parts[8].split('->')) > 1 and ':' in parts[8].split('->')[1] else '',
                'timestamp': datetime.now().isoformat()
            })

    print(json.dumps(connections, indent=2))

if __name__ == "__main__":
    get_active_connections()