import os

def list_player_files(directory="players"):
    """
    Lists the names of all player files in the specified directory.
    Default directory is 'players'.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out non-file entities and return the list of files
    return [file.split('.', 1)[0] for file in files if os.path.isfile(os.path.join(directory, file))]


if __name__ == '__main__':
    # Example usage
    player_files = list_player_files()
    print("Player files:", player_files)