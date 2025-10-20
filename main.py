import os
import paramiko
from dotenv import load_dotenv
import sys

def sftp_upload(sftp, local_path, remote_path):
    print(f"Uploading '{local_path}' to '{remote_path}'...")
    # If remote_path is a directory, append filename
    try:
        if os.path.isfile(local_path):
            try:
                # Check if remote_path is a directory
                attr = sftp.stat(remote_path)
                if str(attr.st_mode).startswith('16877') or remote_path.endswith('/'):
                    # It's a directory, append filename
                    remote_path = os.path.join(remote_path, os.path.basename(local_path))
            except IOError:
                # If stat fails, assume it's a file path
                pass
            sftp.put(local_path, remote_path)
        else:
            # Ensure remote parent directory exists
            parent = os.path.dirname(remote_path)
            try:
                sftp.stat(parent)
            except IOError:
                print(f"Remote parent directory '{parent}' does not exist.")
                raise
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass  # Directory may already exist
            for item in os.listdir(local_path):
                sftp_upload(
                    sftp,
                    os.path.join(local_path, item),
                    os.path.join(remote_path, item)
                )
    except Exception as e:
        print(f"SFTP put error: {type(e).__name__}: {e}")
        raise

def main():
    load_dotenv()
    password = os.getenv("PASSWORD")
    ssh_string = os.getenv("SSH")
    source = os.getenv("SOURCE")
    destination = os.getenv("DESTINATION")
    port = int(os.getenv("PORT", 22))

    # Check for missing values
    missing = []
    for var, val in [("PASSWORD", password), ("SSH", ssh_string), ("SOURCE", source), ("DESTINATION", destination)]:
        if not val:
            missing.append(var)
    if missing:
        print(f"Error: Missing values in .env: {', '.join(missing)}")
        sys.exit(1)

    # Check SSH string format
    if '@' not in ssh_string:
        print("Error: SSH must be in the format user@host")
        sys.exit(1)
    username, host = ssh_string.split('@', 1)

    # Check source existence
    if not os.path.exists(source):
        print(f"Error: SOURCE path does not exist: {source}")
        sys.exit(1)

    # Check source/destination type compatibility
    if os.path.isdir(source):
        # Destination must be a directory (end with /)
        if not (destination.endswith("/")):
            print("Error: SOURCE is a directory, but DESTINATION is not a directory (must end with '/').")
            sys.exit(1)
    elif os.path.isfile(source):
        # Destination must be a file (not end with /)
        if destination.endswith("/"):
            print("Error: SOURCE is a file, but DESTINATION is a directory (must not end with '/').")
            sys.exit(1)

    print(f"Source: {source}\nDestination: {destination}")
    print(f"Connecting to {host} as {username}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp_upload(sftp, source, destination)
        sftp.close()
        ssh.close()
        print("Transfer complete.")
    except Exception as e:
        print(f"Error during transfer: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
