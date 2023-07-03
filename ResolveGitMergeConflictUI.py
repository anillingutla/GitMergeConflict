##replace '/path/to/repository' with the actual path to your Git repository. Also, ensure that the git and tkinter libraries are installed in your Python environment.

from git import Repo
import tkinter as tk
from tkinter import filedialog, messagebox

class MergeConflictResolver:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        self.conflicted_files = []

        if self.repo.is_dirty():
            messagebox.showerror("Error", "Repository has uncommitted changes. Please commit or stash your changes first.")
            return

        if self.repo.index.unmerged_blobs():
            messagebox.showerror("Error", "Repository has merge conflicts. Please resolve the conflicts manually.")
            return

        self.conflicted_files = self.repo.index.conflicts

        if not self.conflicted_files:
            messagebox.showinfo("Merge Conflict Resolver", "No merge conflicts found.")
            return

        self.root = tk.Tk()
        self.root.title("Merge Conflict Resolver")

        self.file_index = 0
        self.choice_var = tk.IntVar()

        self.label = tk.Label(self.root, text="Conflict in file:")
        self.label.pack()

        self.file_path_label = tk.Label(self.root, text="")
        self.file_path_label.pack()

        self.text_box = tk.Text(self.root, height=10, width=60)
        self.text_box.pack()

        self.choice_frame = tk.Frame(self.root)
        self.choice_frame.pack()

        self.option1 = tk.Radiobutton(self.choice_frame, text="Keep changes from the current branch (HEAD)", variable=self.choice_var, value=1)
        self.option1.pack(anchor=tk.W)

        self.option2 = tk.Radiobutton(self.choice_frame, text="Keep changes from the other branch", variable=self.choice_var, value=2)
        self.option2.pack(anchor=tk.W)

        self.option3 = tk.Radiobutton(self.choice_frame, text="Manually merge the changes", variable=self.choice_var, value=3)
        self.option3.pack(anchor=tk.W)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_conflict)
        self.next_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def next_conflict(self):
        if self.file_index >= len(self.conflicted_files):
            messagebox.showinfo("Merge Conflict Resolver", "All merge conflicts resolved and changes committed successfully.")
            self.root.destroy()
            return

        current_conflict = self.conflicted_files[self.file_index]
        file_path = current_conflict.a_blob.path
        conflict_data = current_conflict.a_blob.data_stream.read().decode()

        self.file_path_label.config(text=file_path)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, conflict_data)

        if self.file_index == len(self.conflicted_files) - 1:
            self.next_button.config(text="Finish")
        else:
            self.next_button.config(text="Next")

        self.file_index += 1

        if self.choice_var.get() == 1:
            resolved_content = current_conflict.a_blob.data_stream.read().decode()
        elif self.choice_var.get() == 2:
            resolved_content = current_conflict.b_blob.data_stream.read().decode()
        elif self.choice_var.get() == 3:
            resolved_content = self.text_box.get(1.0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid choice. Skipping this file.")
            return

        with open(file_path, 'w') as file:
            file.write(resolved_content)

        self.repo.index.add(file_path)

        self.next_conflict()

    def on_close(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

# Usage: Create an instance of the MergeConflictResolver class with the repository path
MergeConflictResolver('/path/to/repository')

