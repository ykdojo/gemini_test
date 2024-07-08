import os
import pathspec

def read_gitignore(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            return pathspec.PathSpec.from_lines('gitwildmatch', f)
    return None

def combine_files_and_list_paths(source_dirs, combined_output_file, list_output_file, additional_ignores=None, max_lines=1000):
    if additional_ignores is None:
        additional_ignores = []

    with open(combined_output_file, 'w', encoding='utf-8') as combined_outfile, \
         open(list_output_file, 'w', encoding='utf-8') as list_outfile:
        
        for source_dir in source_dirs:
            gitignore_spec = read_gitignore(source_dir)
            
            # Write a header for the current source directory using only the folder name
            folder_name = os.path.basename(os.path.normpath(source_dir))
            combined_outfile.write(f"Project: {folder_name}\n")
            combined_outfile.write("=" * 50 + "\n\n")
            list_outfile.write(f"Project: {folder_name}\n")
            list_outfile.write("=" * 50 + "\n\n")
            
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
                    
                    # Write the relative path of the file to the list output file
                    list_outfile.write(f"{relative_path}\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            lines = infile.readlines()
                            if len(lines) > max_lines:
                                continue
                            combined_outfile.write(f"File: {relative_path}\n")
                            combined_outfile.write("=" * 50 + "\n\n")
                            combined_outfile.writelines(lines)
                    except UnicodeDecodeError:
                        combined_outfile.write(f"Unable to read file: {relative_path} (possibly binary)\n")
                    
                    combined_outfile.write("\n\n" + "=" * 50 + "\n\n")

if __name__ == "__main__":
    source_directories = ["../cody"]
    combined_output_file = "combined_files.txt"
    list_output_file = "file_list.txt"
    additional_ignores = ["pnpm-lock.yaml"]  # Add more files to ignore as needed
    
    combine_files_and_list_paths(source_directories, combined_output_file, list_output_file, additional_ignores)
    print(f"File contents combined into {combined_output_file}")
    print(f"File paths listed in {list_output_file}")
