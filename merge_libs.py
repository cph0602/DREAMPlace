import os
import re

lib_folder = "ASAP7/LIB"
output_file = "ASAP7/LIB/asap7_merged.lib"

def extract_lib_header(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Match everything between 'library(...) {' and the first 'cell (...) {'
    match = re.search(r'library\s*\(.*?\)\s*{(.*?)(?=\bcell\s*\()', content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract header from {file_path}")
    return match.group(1).strip()

def extract_cells_with_nesting(file_path):
    cells = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    inside_cell = False
    brace_count = 0
    current_cell_lines = []

    for line in lines:
        # Start of a cell (handles various spacings)
        if not inside_cell:
            if re.search(r'^\s*cell\s*\(.*?\)\s*{', line):
                inside_cell = True
                brace_count = line.count('{') - line.count('}')
                current_cell_lines = [line]
        else:
            brace_count += line.count('{') - line.count('}')
            current_cell_lines.append(line)
            if brace_count == 0:
                inside_cell = False
                cells.append(''.join(current_cell_lines))

    return cells

def main():
    lib_files = sorted(f for f in os.listdir(lib_folder) if f.endswith('.lib'))

    if not lib_files:
        print("No .lib files found in folder.")
        return

    first_file_path = os.path.join(lib_folder, lib_files[0])
    header = extract_lib_header(first_file_path)

    all_cells = []
    for lib_file in lib_files:
        path = os.path.join(lib_folder, lib_file)
        print(f"Processing: {lib_file}")
        cells = extract_cells_with_nesting(path)
        print(f"  ➤ Found {len(cells)} cells")
        all_cells.extend(cells)

    with open(output_file, 'w') as out:
        out.write('library(asap7_merged) {\n')
        out.write(f"{header}\n\n")
        for cell in all_cells:
            out.write(f"{cell.strip()}\n\n")
        out.write("}\n")

    print(f"\n✅ Merge complete: {len(lib_files)} files → {len(all_cells)} cells in {output_file}")

if __name__ == "__main__":
    main()
