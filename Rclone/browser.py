import paramiko
from dotenv import load_dotenv
import os


load_dotenv()

# Server details
SERVER_IP = os.getenv("SERVER_IP")
USERNAME = os.getenv("SERVER_USERNAME")
PASSWORD = os.getenv("SERVER_PASSWORD")

# Initialize SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)


def run_command(command, stream_output=False):
    stdin, stdout, stderr = ssh.exec_command(command)

    if stream_output:
        for line in iter(stdout.readline, ""):
            print(line, end="")  # Print each line in real-time
        return "", stderr.read().decode()

    return stdout.read().decode(), stderr.read().decode()


def list_remotes():
    print("Fetching available rclone remotes...")
    stdout, stderr = run_command("rclone listremotes")
    if stderr:
        print("Error:", stderr)
        return []
    remotes = stdout.strip().split("\n")
    return [r.strip(":") for r in remotes]


def list_directory(remote, path=""):
    list_path = f"{remote}:{path}" if path else f"{remote}:"
    stdout, stderr = run_command(f"rclone lsf '{list_path}' --dirs-only")
    directories = stdout.strip().split("\n") if stdout else []
    stdout, stderr = run_command(f"rclone lsf '{list_path}' --files-only")
    files = stdout.strip().split("\n") if stdout else []
    return directories, files


def download_item(remote, path, destination):
    list_path = f"{remote}:{path}".replace("//", "/")

    # Ensure the destination directory exists
    run_command(f"mkdir -p '{os.path.dirname(destination)}'")

    command = f"rclone copy '{list_path}' '{destination}' --progress"
    print(f"Downloading {list_path} to {destination} (on the server)...")

    _, stderr = run_command(command, stream_output=True)  # Stream output

    if stderr:
        print("Error:", stderr)
    else:
        print("\nDownload complete!")



# Main interaction loop
def main():
    remotes = list_remotes()
    if not remotes:
        print("No remotes found. Exiting...")
        return

    print("Available Rclone Remotes:")
    for i, remote in enumerate(remotes, 1):
        print(f"[{i}] {remote}")

    choice = int(input("Select a remote: ")) - 1
    if choice < 0 or choice >= len(remotes):
        print("Invalid selection. Exiting...")
        return

    remote = remotes[choice]
    path = ""

    while True:
        directories, files = list_directory(remote, path)

        print("\nBrowsing:", remote, path)
        print("[0] .. (Go Back)")
        for i, d in enumerate(directories, 1):
            print(f"[{i}] [D] {d}")
        for i, f in enumerate(files, len(directories) + 1):
            print(f"[{i}] [F] {f}")
        print("[X] Exit")

        choice = input("Enter choice: ")
        if choice.lower() == "x":
            break
        elif choice == "0":
            path = "/".join(path.split("/")[:-1]) if path else ""
        elif choice.isdigit():
            index = int(choice) - 1
            if index < len(directories):
                path = f"{path}/{directories[index]}" if path else directories[index]
            elif index < len(directories) + len(files):
                file_to_download = files[index - len(directories)]
                destination = input("Enter destination folder (server): ")
                download_item(remote, f"{path}/{file_to_download}" if path else file_to_download, destination)
            else:
                print("Invalid choice.")
        else:
            print("Invalid input.")

    ssh.close()


if __name__ == "__main__":
    main()
