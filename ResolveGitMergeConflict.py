
from git import Repo

def resolve_merge_conflict(repo_path):
    repo = Repo(repo_path)

    if repo.is_dirty():
        print("Error: Repository has uncommitted changes. Please commit or stash your changes first.")
        return

    if repo.index.unmerged_blobs():
        print("Error: Repository has merge conflicts. Please resolve the conflicts manually.")
        return

    # Check if there are any merge conflicts
    if not repo.index.conflicts:
        print("No merge conflicts found.")
        return

    # Iterate through conflicted files
    for conflicted_file in repo.index.conflicts:
        # Get the file path
        file_path = conflicted_file.a_blob.path

        print(f"\nConflict in file: {file_path}")
        print("---------------------------------------")
        print("Conflict markers:")
        print(conflicted_file.a_blob.data_stream.read().decode())

        # Prompt the user for their choice
        choice = input("Choose an option:\n[1] Keep changes from the current branch (HEAD)\n[2] Keep changes from the other branch\n[3] Manually merge the changes\nEnter your choice: ")

        # Resolve conflicts based on the user's choice
        if choice == "1":
            resolved_content = conflicted_file.a_blob.data_stream.read().decode()
        elif choice == "2":
            resolved_content = conflicted_file.b_blob.data_stream.read().decode()
        elif choice == "3":
            print("Please manually edit the file to merge the changes.")
            continue
        else:
            print("Invalid choice. Skipping this file.")
            continue

        # Open the file for writing and save the resolved content
        with open(file_path, 'w') as file:
            file.write(resolved_content)

        # Add the resolved file to the index
        repo.index.add(file_path)

    # Commit the resolved changes
    commit_msg = "Resolved merge conflicts"
    repo.index.commit(commit_msg)
    print("Merge conflicts resolved and changes committed successfully.")

# Usage: Call the resolve_merge_conflict() function with the path to the Git repository
resolve_merge_conflict('/path/to/repository')
