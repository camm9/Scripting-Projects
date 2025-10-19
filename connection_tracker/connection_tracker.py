# Connection Tracker
# This application tracks active network connections on the system

import subprocess, json, sys, os
from datetime import datetime

def parse_address_port(address_str):
    """ Parses address and port from lsof output. Handles both IPv4 and IPv6 formats. """
    address_str = address_str.strip()

    # IPv6 formats
    if address_str.startswith('['):
        if ']:' in address_str:
            address, port = address_str.rsplit(']:', 1)
            address = address.lstrip('[')
            return address, port
        else:
            # No port specified
            return address_str.strip('[]'), ''
    
    # IPv4 formats
    if ':' in address_str:
        parts = address_str.rsplit(':',1)
        return parts[0], parts[1]
    
    # No port
    return address_str, ''

def get_active_connections():
    """Get all active network connections."""
    print("Fetching active network connections... Be patient, this may take a moment.")
    results = subprocess.run(['lsof', '-i', '-P', '-n'], capture_output=True, text=True)
    lines = results.stdout.strip().split('\n')[1:]

    connections = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 9:

            name_field = parts[8]

            if '->' in name_field:
                # Connection with both local and remote
                local_part, remote_part = name_field.split('->')
                local_addr, local_port = parse_address_port(local_part)
                remote_addr, remote_port = parse_address_port(remote_part)
            else:
                # Only local address
                local_addr, local_port = parse_address_port(name_field)
                remote_addr, remote_port = '', ''

            connections.append({
                'process': parts[0],
                'pid': parts[1],
                'local_address': local_addr,
                'local_port': local_port,
                'remote_address': remote_addr,
                'remote_port': remote_port,
                'timestamp': datetime.now().isoformat()
            })

    return connections

def display_connections(connections):
    """ Display connections in an easy-to-read format """
    print("\nNetwork Connections: \n")
    for connection in connections:
        print(f"Process: {connection['process']} (PID: {connection['pid']})")
        print(f"  Local:  {connection['local_address']}")
        if connection['local_port']:
            print(f"    Local Port: {connection['local_port']}")
        if connection['remote_address']:
            print(f"  Remote: {connection['remote_address']}")
        if connection['remote_port']:
            print(f"    Remote Port: {connection['remote_port']}")
        print()

def save_connections(connections, filename='connections.json'):
    """ Save connections to a JSON file """
    with open(filename, 'w') as file:
        json.dump(connections, file, indent=4)
    
    file_local = os.path.join(os.getcwd(), filename)
    print(f"Saved {len(connections)} connections to {file_local}")


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python connection_tracker.py [ view | save ]")
        sys.exit(1)

    connections = get_active_connections()

    action = sys.argv[1]

    if action == 'view':
        display_connections(connections)
    elif action == 'save':
        save_connections(connections)
    else:
        print("Usage: python connection_tracker.py [ view | save ]")
