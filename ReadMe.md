# LAN File/Folder Share via SSH/SFTP

This tool allows you to securely transfer files or folders from one Mac to another over a local network using SSH and SFTP. All configuration is handled via a `.env` file for simplicity and security.

## 1. Installing the Requirements

First, install the required Python packages:

```sh
pip install -r requirements.txt
```

## 2. Configuring the Input Fields

Create or edit the `.env` file in the project directory. Fill in the following fields:

```
USERNAME=your_ssh_username
PASSWORD=your_ssh_password
SSH=your_ssh_username@remote_ip
SOURCE=/path/to/local/file_or_folder
DESTINATION=/remote/path/on/target
PORT=22
```

- `USERNAME`: SSH username for the remote Mac.
- `PASSWORD`: SSH password for the remote Mac.
- `SSH`: SSH string in the format `username@ip` (e.g., `helloar@192.168.1.2`).
- `SOURCE`: Full path to the local file or folder you want to send.
- `DESTINATION`: Full path to the destination directory or file on the remote machine. If a directory, the filename will be appended automatically.
- `PORT`: SSH port (default is 22).

## 3. Running the Program

Simply run the following command:

```sh
python3 main.py
```

The program will:
- Read all configuration from `.env`.
- Connect to the remote Mac using SSH/SFTP.
- Transfer the specified file or folder to the destination path.
- Print clear error messages if any issues occur (missing fields, connection errors, permission issues, etc.).

## Notes
- Ensure the remote destination directory exists and is writable by the specified user.
- For folder transfers, all contents will be recursively uploaded.
- No command-line arguments are required; all configuration is handled via `.env`.

---

For troubleshooting, check the error messages printed by the program. If you need further help, review your `.env` values and remote permissions.

