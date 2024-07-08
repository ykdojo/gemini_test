import os
import pathspec

def read_gitignore(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            return pathspec.PathSpec.from_lines('gitwildmatch', f)
    return None

def combine_files(source_dir, output_file):
    gitignore_spec = read_gitignore(source_dir)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)
                
                if gitignore_spec and gitignore_spec.match_file(relative_path):
                    continue
                
                outfile.write(f"File: {relative_path}\n")
                outfile.write("=" * 50 + "\n\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except UnicodeDecodeError:
                    outfile.write(f"Unable to read file: {relative_path} (possibly binary)\n")
                
                outfile.write("\n\n" + "=" * 50 + "\n\n")

if __name__ == "__main__":
    source_directory = "../summarizeThis"
    output_file = "combined_files.txt"
    
    combine_files(source_directory, output_file)
    print(f"All files have been combined into {output_file}")
