import glob
import json
import re
from pathlib import Path


def parse_file_toctree(file_path: str) -> list:
    """
    Parse a single file for .. toctree:: directives and extract entries with nested segments.

    Args:
        file_path: Path to the file to parse

    Returns:
        List of entries found in toctree directives, including nested segments
    """
    entries: list = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all toctree blocks with their options and content
        # First, find the entire toctree blocks
        toctree_pattern = r"\.\. toctree::\s*\n(.*?)(?=\n\.\.|\n\w|\Z)"
        toctree_blocks = re.findall(toctree_pattern, content, re.DOTALL | re.MULTILINE)
        
        # Process each block to separate options and content
        toctree_matches = []
        for block in toctree_blocks:
            # Split options and content manually
            lines = block.split('\n')
            options_lines = []
            content_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(':'):
                    options_lines.append(line)
                else:
                    content_lines.append(line)
            
            options_block = '\n'.join(options_lines) + '\n' if options_lines else ''
            content_block = '\n'.join(content_lines) + '\n' if content_lines else ''
            toctree_matches.append((options_block, content_block))

        for options_block, content_block in toctree_matches:
            # Extract caption from options
            caption_match = re.search(r":caption:\s*(.+)", options_block)
            caption = caption_match.group(1).strip() if caption_match else None

            # Parse entries from content
            segment_entries: list = []
            lines = content_block.split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith(":") and not line.startswith("#"):
                    # Handle external links (format: "Title <URL>")
                    if "<" in line and ">" in line:
                        title_match = re.match(r"^(.+?)\s*<(.+)>$", line)
                        if title_match:
                            title = title_match.group(1).strip()
                            url = title_match.group(2).strip()
                            segment_entries.append(
                                {
                                    "title": title,
                                    "url": url,
                                    "is_external": True,
                                    "children": [],
                                }
                            )
                    else:
                        # Internal page reference
                        segment_entries.append(
                            {
                                "title": line.replace("_", " ")
                                .replace("-", " ")
                                .title(),
                                "url": f"/{line}.html",
                                "is_external": False,
                                "children": [],
                            }
                        )

            # If there's a caption and entries, create a grouped entry
            if caption and segment_entries:
                entries.append(
                    {
                        "title": caption,
                        "url": f"/{Path(file_path).stem}.html",  # Link to the parent file
                        "is_external": False,
                        "children": segment_entries,
                    }
                )
            else:
                # No caption, add entries directly
                entries.extend(segment_entries)

    except FileNotFoundError:
        print(f"Warning: Could not find file: {file_path}")
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")

    return entries


def _extract_rst_header(file_path: str) -> str | None:
    """
    Extract the first header from an RST file.
    
    Args:
        file_path: Path to the RST file
        
    Returns:
        The first header text or None if not found
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Look for the first header (title with underline)
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Skip metadata lines (starting with :)
            if line.startswith(":"):
                continue
            
            # Check if this line is followed by a header underline
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Check for header underlines (=, -, ~, etc.)
                if next_line and all(c in "=-~^\"'`" for c in next_line) and len(next_line) >= len(line):
                    return line
        
        # If no header with underline found, look for single-line headers
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip metadata lines
            if line.startswith(":"):
                continue
            
            # Check for single-line headers (lines that are all caps or title case)
            if line.isupper() or (line.istitle() and len(line) > 3):
                return line
                
    except Exception as e:
        print(f"Error extracting header from RST file {file_path}: {e}")
    
    return None


def _extract_ipynb_header(file_path: str) -> str | None:
    """
    Extract the first header from a Jupyter notebook file.
    
    Args:
        file_path: Path to the .ipynb file
        
    Returns:
        The first header text or None if not found
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)
        
        # Look through cells for the first markdown header
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "markdown":
                source = cell.get("source", [])
                if isinstance(source, list):
                    # Join source lines
                    content = "".join(source)
                else:
                    content = source
                
                # Look for markdown headers (# ## ### etc.)
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        # Extract header text (remove # symbols)
                        header = re.sub(r'^#+\s*', '', line).strip()
                        if header:
                            return header
                
    except Exception as e:
        print(f"Error extracting header from notebook file {file_path}: {e}")
    
    return None


def _extract_file_header(file_path: str) -> str | None:
    """
    Extract the first header from a file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        The first header text or None if not found
    """
    file_path_obj = Path(file_path)
    
    if file_path_obj.suffix == ".rst":
        return _extract_rst_header(file_path)
    elif file_path_obj.suffix == ".ipynb":
        return _extract_ipynb_header(file_path)
    
    return None


def discover_nested_files(base_path: str, max_depth: int = 3) -> dict:
    """
    Discover nested files in a directory structure using glob patterns.

    Args:
        base_path: Base directory path to search
        max_depth: Maximum depth to search for nested files

    Returns:
        Dictionary mapping directory paths to their nested files
    """
    nested_files: dict[str, list] = {}
    base_path_obj = Path(base_path)

    if not base_path_obj.exists():
        return nested_files

    # Find all .rst and .ipynb files in subdirectories
    for depth in range(1, max_depth + 1):
        pattern = str(base_path_obj) + "/" + "*/" * depth + "*.rst"
        rst_files = glob.glob(pattern)

        pattern = str(base_path_obj) + "/" + "*/" * depth + "*.ipynb"
        ipynb_files = glob.glob(pattern)

        all_files = rst_files + ipynb_files

        for file_path in all_files:
            file_obj = Path(file_path)
            parent_dir = str(file_obj.parent)

            if parent_dir not in nested_files:
                nested_files[parent_dir] = []

            # Convert to relative path from base_path
            rel_path = file_obj.relative_to(base_path_obj)

            # Parse toctree directives from this file
            toctree_entries = []
            if file_obj.suffix == ".rst":
                toctree_entries = parse_file_toctree(file_path)

            nested_files[parent_dir].append(
                {
                    "name": file_obj.stem,
                    "path": str(rel_path),
                    "full_path": file_path,
                    "is_notebook": file_obj.suffix == ".ipynb",
                    "toctree_entries": toctree_entries,
                }
            )

    return nested_files


def parse_toctree_file(toctree_path: str) -> dict:
    """
    Parse a toctree file and extract navigation structure with nested items.
    Handles multiple toctree directives in a single file and recursively parses nested files.

    Args:
        toctree_path: Path to the toctree file

    Returns:
        Dictionary containing caption and entries from all toctrees in the file
    """
    toctree_data: dict = {"caption": "", "entries": []}
    base_dir = Path(toctree_path).parent

    try:
        with open(toctree_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all toctree blocks in the file
        toctree_blocks = _extract_toctree_blocks(content)
        
        # Process each toctree block
        for toctree_block in toctree_blocks:
            options_block, content_block = toctree_block
            
            # Extract caption from options (use first caption found)
            if not toctree_data["caption"]:
                caption_match = re.search(r":caption:\s*(.+)", options_block)
                if caption_match:
                    toctree_data["caption"] = caption_match.group(1).strip()

            # Parse entries from this toctree block
            entries = _parse_toctree_entries(content_block, str(base_dir), toctree_path)
            toctree_data["entries"].extend(entries)

    except FileNotFoundError:
        print(f"Warning: Could not find toctree file: {toctree_path}")
    except Exception as e:
        print(f"Error parsing toctree file {toctree_path}: {e}")

    return toctree_data


def _extract_toctree_blocks(content: str) -> list:
    """
    Extract all toctree blocks from RST content.
    
    Args:
        content: RST file content
        
    Returns:
        List of tuples (options_block, content_block) for each toctree found
    """
    toctree_blocks = []
    
    # Find all toctree directives
    toctree_starts = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if line.strip().startswith('.. toctree::'):
            toctree_starts.append(i)
    
    # Process each toctree block
    for start_line in toctree_starts:
        options_lines = []
        content_lines = []
        
        # Process lines after the toctree directive
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            stripped = line.strip()
            
            # Stop if we hit another directive or section
            if stripped.startswith('..') and not stripped.startswith('.. toctree::'):
                break
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                # This is a new section, stop processing
                break
            
            # Skip empty lines
            if not stripped:
                continue
                
            # Check if this is an option line (starts with :)
            if stripped.startswith(':'):
                options_lines.append(stripped)
            else:
                # This is content (page references)
                content_lines.append(stripped)
        
        # Only add if we have content
        if content_lines:
            options_block = '\n'.join(options_lines)
            content_block = '\n'.join(content_lines)
            toctree_blocks.append((options_block, content_block))
    
    return toctree_blocks


def _parse_toctree_entries(content_block: str, base_dir: str, toctree_path: str) -> list:
    """
    Parse entries from a toctree content block and recursively find nested toctrees.
    
    Args:
        content_block: The content section of a toctree directive
        base_dir: Base directory path for resolving relative paths
        toctree_path: Path to the current toctree file for context
        
    Returns:
        List of entry dictionaries with nested children
    """
    entries: list = []
    lines = content_block.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle external links (format: "Title <URL>")
        if "<" in line and ">" in line:
            title_match = re.match(r"^(.+?)\s*<(.+)>$", line)
            if title_match:
                title = title_match.group(1).strip()
                url = title_match.group(2).strip()
                entries.append({
                    "title": title,
                    "url": url,
                    "is_external": True,
                    "children": [],
                })
        else:
            # Check if this is a glob pattern (contains *)
            if "*" in line:
                # Expand glob pattern to actual file paths
                expanded_paths = _expand_glob_pattern(line, base_dir)
                for expanded_path in expanded_paths:
                    # Process each expanded path as a regular entry
                    entry = _create_entry_from_path(expanded_path, base_dir)
                    if entry:
                        entries.append(entry)
            else:
                # Regular internal page reference
                entry = _create_entry_from_path(line, base_dir)
                if entry:
                    entries.append(entry)
    
    return entries


def _expand_glob_pattern(pattern: str, base_dir: str) -> list:
    """
    Expand a glob pattern to actual file paths.
    
    Args:
        pattern: Glob pattern (e.g., "/start/glossary/security/*")
        base_dir: Base directory for resolving relative paths
        
    Returns:
        List of expanded file paths
    """
    expanded_paths = []
    
    try:
        # Handle both absolute and relative patterns
        if pattern.startswith("/"):
            # Absolute pattern from script-docs root
            search_pattern = f"script-docs{pattern}.rst"
        else:
            # Relative pattern from base_dir
            search_pattern = str(Path(base_dir) / f"{pattern}.rst")
        
        # Use glob to find matching files
        matching_files = glob.glob(search_pattern)
        
        # Convert to relative paths for processing
        script_docs_path = Path("script-docs")
        for file_path in matching_files:
            try:
                relative_path = Path(file_path).relative_to(script_docs_path)
                # Remove .rst extension and convert to path format
                path_without_ext = str(relative_path).replace(".rst", "")
                expanded_paths.append(path_without_ext)
            except ValueError:
                # If not relative to script-docs, use the filename
                path_without_ext = Path(file_path).stem
                expanded_paths.append(path_without_ext)
        
        # Sort for consistent ordering
        expanded_paths.sort()
        
    except Exception as e:
        print(f"Error expanding glob pattern {pattern}: {e}")
    
    return expanded_paths


def _create_entry_from_path(line: str, base_dir: str) -> dict | None:
    """
    Create an entry dictionary from a file path.
    
    Args:
        line: File path line from toctree
        base_dir: Base directory for resolving relative paths
        
    Returns:
        Entry dictionary or None if invalid
    """
    try:
        # Handle both relative and absolute paths
        if line.startswith(str(Path(base_dir).name)):
            # The line is already a full path relative to script-docs
            entry_path = Path("script-docs") / line
        else:
            # The line is relative to the current toctree file's directory
            entry_path = Path(base_dir) / line
        
        children = _get_nested_children(str(entry_path))
        
        # Generate title from filename
        title = line.replace("_", " ").replace("-", " ").title()
        
        return {
            "title": title,
            "url": f"/{line}.html",
            "is_external": False,
            "children": children,
        }
    except Exception as e:
        print(f"Error creating entry from path {line}: {e}")
        return None


def _get_nested_children(file_path: str) -> list:
    """
    Recursively get children from a file by parsing its toctree directives.
    
    Args:
        file_path: Path to the file to parse for nested toctrees
        
    Returns:
        List of child entry dictionaries with absolute paths
    """
    children: list = []
    
    try:
        # Check if the file exists
        if not Path(file_path).exists():
            # Try with .rst extension
            rst_path = f"{file_path}.rst"
            if Path(rst_path).exists():
                file_path = rst_path
            else:
                return children
        
        # Get the relative path from script-docs directory for URL construction
        script_docs_path = Path("script-docs")
        try:
            relative_path = Path(file_path).relative_to(script_docs_path)
            parent_url_prefix = f"/{relative_path.parent}" if relative_path.parent != Path(".") else ""
        except ValueError:
            # If file_path is not relative to script-docs, use the filename
            parent_url_prefix = ""
        
        # Parse the file for toctree directives
        file_toctree_data = parse_toctree_file(file_path)
        
        # Add children from the parsed toctree with absolute paths
        if file_toctree_data["entries"]:
            for entry in file_toctree_data["entries"]:
                # Update the URL to be absolute
                if not entry["is_external"]:
                    # Extract the path from the current URL (remove leading / and .html)
                    current_url = entry["url"]
                    path_part = current_url.lstrip("/").replace(".html", "")
                    
                    # Construct absolute path
                    if parent_url_prefix:
                        entry["url"] = f"{parent_url_prefix}/{path_part}.html"
                    else:
                        entry["url"] = f"/{path_part}.html"
                
                children.append(entry)
        
    except Exception as e:
        print(f"Error parsing nested file {file_path}: {e}")
    
    return children


def generate_sidebar_html(toctree_data: dict, sidebar_name: str) -> str:
    """
    Generate HTML sidebar template from toctree data with nested structure.

    Args:
        toctree_data: Parsed toctree data
        sidebar_name: Name for the sidebar template file

    Returns:
        HTML content for the sidebar template
    """
    html_parts = [
        '<nav class="table w-full min-w-full my-6 lg:my-8">',
        f'  <p class="caption" role="heading"><span class="caption-text">{toctree_data["caption"]}</span></p>',
        "  <ul>",
    ]

    for entry in toctree_data["entries"]:
        html_parts.extend(_generate_entry_html(entry, level=1))

    html_parts.extend(["  </ul>", "</nav>"])

    return "\n".join(html_parts)


def _generate_entry_html(entry: dict, level: int = 1) -> list:
    """
    Generate HTML for a single navigation entry with its children.

    Args:
        entry: Navigation entry dictionary
        level: Current nesting level (1, 2, 3, etc.)

    Returns:
        List of HTML lines for this entry
    """
    html_lines = []
    indent = "    " * level
    css_class = f"toctree-l{level}"

    if entry["is_external"]:
        link_class = "reference external"
    else:
        link_class = "reference internal"

    # Generate the main entry
    if entry.get("children"):
        # Entry with children - create expandable structure
        html_lines.append(
            f'{indent}<li class="{css_class}"><a class="{link_class}" href="{entry["url"]}">{entry["title"]}</a>'
        )
        html_lines.append(f"{indent}  <ul>")

        # Generate children
        for child in entry["children"]:
            html_lines.extend(_generate_entry_html(child, level + 1))

        html_lines.append(f"{indent}  </ul>")
        html_lines.append(f"{indent}</li>")
    else:
        # Simple entry without children
        html_lines.append(
            f'{indent}<li class="{css_class}"><a class="{link_class}" href="{entry["url"]}">{entry["title"]}</a></li>'
        )

    return html_lines


