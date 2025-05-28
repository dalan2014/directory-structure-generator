import os
import re

def parse_line_details(line_str):
    """
    Parses a line to determine its indentation level, name, and if it's a directory.
    Handles comments and various tree drawing characters.
    """
    # 1. Remove comments (text after '#') and strip trailing whitespace from the comment-free part
    line_no_comments = line_str.split('#', 1)[0].rstrip()

    # 2. Determine if it's a directory from the comment-free, right-stripped line
    is_directory = line_no_comments.endswith('/')

    # 3. Extract the actual name
    # Remove all known tree prefix characters (│, └, ├, ─) and spaces from the beginning.
    # Then strip any leading/trailing whitespace that might remain around the name itself.
    # This regex targets characters typically used for tree drawing at the start of the string.
    name_part = re.sub(r"^[│\s└├─]*", "", line_no_comments).strip()
    
    # If it was a directory, remove the trailing slash from the extracted name_part
    if is_directory:
        name_part = name_part.rstrip('/')
    
    cleaned_name = name_part

    # 4. Calculate indent_level.
    # Use the line *before* comment removal for indent calculation if comments are strictly at the end.
    # Or, to be safer, use the line after comment removal but before stripping leading tree characters for the name.
    # The original script's indent logic based on connector position is generally sound.
    # We apply it to the line_for_indent_calc.
    
    line_for_indent_calc = line_str.split('#', 1)[0] # Use line before comment, but keeping its original spacing for indent

    indent_prefix_len = 0
    # Try to find standard tree connectors "├──" or "└──"
    connector_match = re.search(r"├──|└──", line_for_indent_calc)
    if connector_match:
        indent_prefix_len = connector_match.start()
    else:
        # If no connector, it's likely a root item or an item directly under a parent.
        # The indentation is the length of leading whitespace before the first non-whitespace character.
        name_start_match = re.search(r"\S", line_for_indent_calc) # \S matches any non-whitespace character
        if name_start_match:
            indent_prefix_len = name_start_match.start()
        # If the line was empty or all whitespace (after comment removal), indent_prefix_len remains 0.
        # Empty/whitespace-only lines are typically skipped by the main loop.
            
    # Assuming 4 characters per indent step (e.g., "│   " or "    ").
    indent_level = indent_prefix_len // 4
    
    # Ensure that an empty cleaned_name (e.g. from a line like "├── /") is handled if necessary,
    # though os.makedirs might handle it, open() would not. Valid names are expected.
    if not cleaned_name:
        # This could happen for malformed lines like "├── /".
        # Depending on desired behavior, could raise an error or return a special marker.
        # For now, let's assume valid names are extracted.
        pass

    return indent_level, cleaned_name, is_directory

def create_directory_structure_from_file(input_filepath="dic.txt"):
    """
    Reads a file describing a directory structure and creates it.

    Args:
        input_filepath (str): Path to the file containing the directory structure.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{input_filepath}' not found.")
        return

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file '{input_filepath}': {e}")
        return

    path_parts = [] 
    first_line_processed = False

    for line_number, line_content in enumerate(lines, 1):
        line = line_content.rstrip('\n') 
        
        if not line.strip(): 
            continue

        try:
            indent_level, name, is_dir = parse_line_details(line)
            if not name: # Skip if parse_line_details returns an empty name (e.g. from "├── /")
                print(f"Warning: Parsed an empty name on line {line_number} ('{line}'). Skipping item.")
                continue
        except Exception as e:
            print(f"Error parsing line {line_number} ('{line}'): {e}. Skipping.")
            continue
        
        # Debug print (optional)
        # print(f"Line {line_number}: Indent: {indent_level}, Name: '{name}', IsDir: {is_dir}, PathStack: {path_parts}")

        if not first_line_processed:
            if indent_level == 0 and is_dir:
                try:
                    os.makedirs(name, exist_ok=True)
                    path_parts = [name] 
                    first_line_processed = True
                except OSError as e:
                    print(f"Error creating root directory '{name}': {e}. Aborting.")
                    return
            elif indent_level == 0 and not is_dir: 
                try:
                    # Ensure parent directory (current working directory in this case) exists implicitly.
                    with open(name, 'w') as f_obj: pass 
                    path_parts = [] # Root is a file, no deeper path stack from it.
                    print(f"Note: Root item '{name}' is a file.")
                    first_line_processed = True
                except OSError as e:
                    print(f"Error creating root file '{name}': {e}. Aborting.")
                    return
            else:
                print(f"Error: First non-empty line ('{line}') is not a valid root. Expected indent_level 0. Parsed indent: {indent_level}. Aborting.")
                return
            continue 
        
        # Adjust path_parts to represent the parent directory for the current item
        # The parent of an item at indent_level N is at path_parts[N] if N < len(path_parts)
        # So, the components of the parent path are path_parts[0...N]. Length is N+1.
        # Example: item indent_level 1. Parent components: path_parts[0], path_parts[1]. Slice path_parts[:1+1]
        if indent_level < len(path_parts):
            current_parent_path_components = path_parts[:indent_level+1]
        elif indent_level == len(path_parts): # Item is a direct child of the last directory in path_parts
             current_parent_path_components = list(path_parts)
        else: # indent_level > len(path_parts) - A jump in indentation, implies missing parent dirs in input
             print(f"Warning on line {line_number} ('{line}'): Indentation level {indent_level} is deeper than current path depth {len(path_parts)}. Structure might be inconsistent or missing intermediate directories in the input. Attempting to use full current path as parent.")
             current_parent_path_components = list(path_parts)


        parent_path_str = os.path.join(*current_parent_path_components) if current_parent_path_components else ""
        current_item_full_path = os.path.join(parent_path_str, name)

        try:
            if is_dir:
                os.makedirs(current_item_full_path, exist_ok=True)
                # Update path_parts: current parent + this new directory
                path_parts = current_parent_path_components + [name]
            else: 
                if parent_path_str: # Ensure parent directory exists
                    os.makedirs(parent_path_str, exist_ok=True)
                elif not parent_path_str and current_parent_path_components: # Should not happen if logic is correct
                    print(f"Warning: parent_path_str is empty but current_parent_path_components is not for file '{name}'. This is unexpected.")

                with open(current_item_full_path, 'w') as f_obj:
                    pass 
                # For a file, path_parts should reflect its parent directory for the next sibling
                path_parts = current_parent_path_components
        except OSError as e:
            print(f"Error creating item '{current_item_full_path}' on line {line_number}: {e}. Skipping item.")
            path_parts = current_parent_path_components # Revert path_parts to parent level
            continue
            
    print(f"Directory structure from '{input_filepath}' processed.")

if __name__ == '__main__':
    # Create a dummy dic.txt for testing

    test_file_path = "dic.txt"
   
    print(f"'{test_file_path}' created for testing.")
    print("Attempting to create directory structure...")
    create_directory_structure_from_file(test_file_path)
    print("\nScript finished. Check your file system for the 'ai-multimodal-hub' directory and its contents.")
    print(f"You can delete '{test_file_path}' and the 'ai-multimodal-hub/' directory if you wish.")