# File Integrity Checker
# This script checks the integrity of files in a specified directory by comparing their current
# hash values with previously stored hash values.

import os, hashlib, json, sys

def calculate_file_hash(file_path):
    """Calculate the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_baseline(directory):
    """Create baseline hash values for all files in the directory."""
    baseline_hashes = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            baseline_hashes[filename] = calculate_file_hash(file_path)

    with open('baseline_hashes.json', 'w') as file:
        json.dump(baseline_hashes, file, indent=2)
    print(f"Baseline hashes created and saved to baseline_hashes.json. \n {len(baseline_hashes)} files found.")

def verify_integrity(directory):
    """Verify the files in directory against the baseline hashes."""
    with open('baseline_hashes.json', 'r') as file:
        baseline_hashes = json.load(file)

    print("Verifying file integrity...")
    
    changes_detected = False
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            current_hash = calculate_file_hash(file_path)
            number_of_changes = 0
            if filename in baseline_hashes:
                if current_hash != baseline_hashes[filename] and filename != "baseline_hashes.json" and filename != "file_integrity_checker.py":
                    print(f"File modified: {filename}")
                    number_of_changes += 1
                elif filename == "baseline_hashes.json":
                    continue
            else:   
                print(f"New file detected: {filename} -- {current_hash}")
                number_of_changes += 1

    for filename in baseline_hashes:
        if filename not in os.listdir(directory):
            print(f"File deleted: {filename}")
            number_of_changes += 1
        
    if number_of_changes > 0:
        changes_detected = True
        print(f"Integrity check completed. {number_of_changes} changes detected.")
    else:
        print("Integrity check completed. No changes detected.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python file_integrity_checker.py [ create | verify ] [ directory ]")
        sys.exit(1)
    
    action = sys.argv[1]
    directory = sys.argv[2]

    if action == "create":
        create_baseline(directory)
    elif action == "verify":
        verify_integrity(directory)