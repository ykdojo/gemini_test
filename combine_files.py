import os
import pathspec

def read_gitignore(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            return pathspec.PathSpec.from_lines('gitwildmatch', f)
    return None

def combine_files(source_dirs, output_file, additional_ignores=None, max_lines=1000):
    if additional_ignores is None:
        additional_ignores = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for source_dir in source_dirs:
            gitignore_spec = read_gitignore(source_dir)
            
            # Write a header for the current source directory using only the folder name
            folder_name = os.path.basename(os.path.normpath(source_dir))
            outfile.write(f"Project: {folder_name}\n")
            outfile.write("=" * 50 + "\n\n")
            
            for root, dirs, files in os.walk(source_dir):
                # Skip the .git directory
                dirs[:] = [d for d in dirs if d != '.git']
                
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, source_dir)
                    
                    # Check if the file should be ignored
                    if gitignore_spec and gitignore_spec.match_file(relative_path):
                        continue
                    if any(relative_path.endswith(ignore) for ignore in additional_ignores):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            lines = infile.readlines()
                            if len(lines) > max_lines:
                                continue
                            outfile.write(f"File: {relative_path}\n")
                            outfile.write("=" * 50 + "\n\n")
                            outfile.writelines(lines)
                    except UnicodeDecodeError:
                        outfile.write(f"Unable to read file: {relative_path} (possibly binary)\n")
                    
                    outfile.write("\n\n" + "=" * 50 + "\n\n")

if __name__ == "__main__":
    source_directories = ["../cody"]
    output_file = "combined_files.txt"
    additional_ignores = ["pnpm-lock.yaml"]  # Add more files to ignore as needed
    
    combine_files(source_directories, output_file, additional_ignores)
    print(f"All files have been combined into {output_file}")
