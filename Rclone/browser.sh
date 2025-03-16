#!/bin/bash

# Check if rclone is installed
if ! command -v rclone &> /dev/null
then
    echo "rclone could not be found. Please install it first."
    exit 1
fi

# Function to display available rclone remotes and allow selection
display_remotes() {
    echo "Available Rclone Remotes:"
    local remotes=()
    local index=1

    while IFS= read -r line; do
        remotes+=("${line%:}")  # Remove trailing colon
        echo "[$index] ${line%:}"
        ((index++))
    done < <(rclone listremotes)

    echo "-------------------------------------"
    echo "Enter the number of the remote to browse:"
    read -r input

    if [[ "$input" =~ ^[0-9]+$ ]] && (( input > 0 && input <= ${#remotes[@]} )); then
        remote="${remotes[input-1]}"
        echo "Selected remote: $remote"
        browse_directory "$remote" ""
    else
        echo "Invalid selection. Exiting."
        exit 1
    fi
}

# Function to browse a remote directory
browse_directory() {
    local remote="$1"
    local path="$2"

    while true; do
        echo -e "\nBrowsing: $remote:$path"
        echo "-------------------------------------"
        local items=()
        local index=1

        # Ensure correct root path listing
        local list_path="$remote:${path%/}"

        # List directories
        while IFS= read -r line; do
            items+=("$line/")
            echo "[$index] [D] $line"
            ((index++))
        done < <(rclone lsf "$list_path" --dirs-only)

        # List files
        while IFS= read -r line; do
            items+=("$line")
            echo "[$index] [F] $line"
            ((index++))
        done < <(rclone lsf "$list_path" --files-only)

        echo "-------------------------------------"
        echo "Enter the number to navigate/download, '..' to go back, or 'exit' to quit:"
        read -r input

        if [[ "$input" == "exit" ]]; then
            exit 0
        elif [[ "$input" == ".." ]]; then
            if [[ -z "$path" ]]; then
                echo "Already at root directory."
            else
                path="${path%/*}"
                path="${path#/}"  # Remove leading slash if needed
            fi
        elif [[ "$input" =~ ^[0-9]+$ ]] && (( input > 0 && input <= ${#items[@]} )); then
            selected_item="${items[input-1]}"
            if [[ "$selected_item" == */ ]]; then
                echo "Do you want to (1) enter the directory or (2) download it?"
                read -r choice
                if [[ "$choice" == "1" ]]; then
                    path="${path:+$path/}${selected_item%/}"
                elif [[ "$choice" == "2" ]]; then
                    echo "Enter destination folder on server:"
                    read -r dest
                    mkdir -p "$dest"
                    rclone copy "$list_path/${selected_item%/}" "$dest" --progress --stats-one-line
                    echo "Download completed."
                else
                    echo "Invalid choice."
                fi
            else
                echo "Enter destination folder on server:"
                read -r dest
                mkdir -p "$dest"
                rclone copy "$list_path/$selected_item" "$dest" --progress --stats-one-line
                echo "Download completed."
            fi
        else
            echo "Invalid input. Try again."
        fi
    done
}

# Main script
clear
display_remotes
