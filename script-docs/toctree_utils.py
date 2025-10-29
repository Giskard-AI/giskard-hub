import glob
import json
import re
from pathlib import Path


def extract_rst_title(file_path: str) -> str | None:
    """
    Extract the text from the first line that starts with a letter in an RST file.

    Args:
        file_path: Path to the RST file

    Returns:
        The first line starting with a letter, with whitespace stripped, or None if not found.
    """
    try:
        if not file_path.endswith(".rst"):
            file_path = f"{file_path}.rst"

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped_line = line.lstrip()
                if stripped_line and stripped_line[0].isalnum():
                    return stripped_line.strip()
        return None
    except (FileNotFoundError, Exception) as e:
        print(f"Warning: Could not extract title from {file_path}: {e}")
        return None


def extract_ipynb_title(file_path: str) -> str | None:
    """
    Extract the first header from a Jupyter notebook file to use as the title.

    Args:
        file_path: Path to the .ipynb file

    Returns:
        The first header found in the notebook, or None if no header is found
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook_data = json.load(f)

        # Look through cells for the first markdown cell with a header
        for cell in notebook_data.get("cells", []):
            if cell.get("cell_type") == "markdown":
                source = cell.get("source", [])
                if isinstance(source, list):
                    # Join all source lines
                    content = "".join(source)
                else:
                    content = str(source)

                # Look for markdown headers (# ## ### etc.)
                lines = content.split("\n")
                for line in lines:
                    line = line.strip()
                    # Check if line starts with # (markdown header)
                    if line.startswith("#"):
                        # Remove the # symbols and return the title
                        title = line.lstrip("#").strip()
                        if title:  # Make sure it's not just # symbols
                            return title

        return None

    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Warning: Could not extract title from {file_path}: {e}")
        return None


def get_url_extension(file_path: str) -> str:
    """
    Get the appropriate URL extension for a file.

    Args:
        file_path: Path to the file

    Returns:
        ".html" for regular files, ".ipynb.html" for notebook files
    """
    file_path_obj = Path(file_path)
    if file_path_obj.suffix == ".ipynb":
        return ".ipynb.html"
    else:
        return ".html"


def extract_file_title(file_path: str) -> str | None:
    """
    Extract the first header from a file (RST or Jupyter notebook) to use as the title.
    Also handles wildcard patterns by returning None (they should be processed by glob patterns).

    Args:
        file_path: Path to the file

    Returns:
        The first header found in the file, or None if no header is found or if it's a wildcard pattern
    """
    # Handle wildcard patterns - these should not be processed for title extraction
    if "*" in file_path:
        return None

    file_path_obj = Path(file_path)

    if file_path_obj.suffix == ".rst" or file_path_obj.suffix == "":
        return extract_rst_title(file_path)
    elif file_path_obj.suffix == ".ipynb":
        return extract_ipynb_title(file_path)
    else:
        return None


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
        # Optimized regex to avoid catastrophic backtracking:
        # Use negated character class instead of .*? for better performance
        toctree_pattern = r"\.\. toctree::\s*\n([^\n]*(?:\n(?!\.\.|\w)[^\n]*)*)"
        toctree_blocks = re.findall(toctree_pattern, content, re.DOTALL | re.MULTILINE)

        # Process each block to separate options and content
        toctree_matches = []
        for block in toctree_blocks:
            # Split options and content manually
            lines = block.split("\n")
            options_lines = []
            content_lines = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(":"):
                    options_lines.append(line)
                else:
                    content_lines.append(line)

            options_block = "\n".join(options_lines) + "\n" if options_lines else ""
            content_block = "\n".join(content_lines) + "\n" if content_lines else ""
            toctree_matches.append((options_block, content_block))

        for options_block, content_block in toctree_matches:
            # Extract caption from options
            # Optimized regex to avoid potential backtracking issues
            caption_match = re.search(r":caption:\s*([^\n]+)", options_block)
            caption = caption_match.group(1).strip() if caption_match else None

            # Parse entries from content
            segment_entries: list = []
            lines = content_block.split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith(":") and not line.startswith("#"):
                    # Handle external links (format: "Title <URL>")
                    if "<" in line and ">" in line:
                        # Optimized regex to avoid catastrophic backtracking:
                        # Use greedy quantifier with negated character class to prevent backtracking
                        title_match = re.match(
                            r"^([^\n<>\s]+(?:\s+[^\n<>\s]+)*)\s*<([^<>]+)>$", line
                        )
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
                # Determine the correct URL extension for the parent file
                url_ext = get_url_extension(file_path)

                entries.append(
                    {
                        "title": caption,
                        "url": f"/{Path(file_path).stem}{url_ext}",  # Link to the parent file
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


def parse_toctree_file(
    toctree_path: str, processed_files: set[str] | None = None
) -> dict:
    """
    Parse a toctree file and extract navigation structure with nested items.
    Handles multiple toctree directives in a single file and recursively parses nested files.
    Each toctree with a caption becomes a separate section with its own header.

    Args:
        toctree_path: Path to the toctree file
        processed_files: Set of files already processed to prevent infinite loops

    Returns:
        Dictionary containing "sections" (list of sections, each with "caption" and "entries")
        For backward compatibility, also includes "caption" and "entries" (from first section)
    """
    if processed_files is None:
        processed_files = set()

    sections: list = []
    base_dir = Path(toctree_path).parent

    try:
        with open(toctree_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all toctree blocks in the file
        toctree_blocks = _extract_toctree_blocks(content)

        # Process each toctree block as a separate section
        for toctree_block in toctree_blocks:
            options_block, content_block = toctree_block

            # Extract caption from options
            caption_match = re.search(r":caption:\s*([^\n]+)", options_block)
            caption = caption_match.group(1).strip() if caption_match else ""

            # Parse entries from this toctree block
            entries = _parse_toctree_entries(
                content_block, str(base_dir), toctree_path, processed_files
            )

            # Only add section if it has entries or a caption
            if entries or caption:
                sections.append({"caption": caption, "entries": entries})

    except FileNotFoundError:
        print(f"Warning: Could not find toctree file: {toctree_path}")
    except Exception as e:
        print(f"Error parsing toctree file {toctree_path}: {e}")

    # For backward compatibility and when there's only one section, also provide top-level caption/entries
    toctree_data: dict = {"sections": sections}
    if sections:
        toctree_data["caption"] = sections[0]["caption"]
        toctree_data["entries"] = sections[0]["entries"]
    else:
        toctree_data["caption"] = ""
        toctree_data["entries"] = []

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
    lines = content.split("\n")

    for i, line in enumerate(lines):
        if line.strip().startswith(".. toctree::"):
            toctree_starts.append(i)

    # Process each toctree block
    for start_line in toctree_starts:
        options_lines = []
        content_lines = []

        # Process lines after the toctree directive
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            stripped = line.strip()

            # Stop if we hit another toctree directive (explicit check for multiple toctrees)
            if stripped.startswith(".. toctree::"):
                break

            # Stop if we hit another directive (but not toctree, which we handled above)
            if stripped.startswith(".."):
                break

            # Stop if we hit a non-indented line that's not empty (new section)
            if stripped and not line.startswith(" ") and not line.startswith("\t"):
                break

            # Skip empty lines
            if not stripped:
                continue

            # Check if this is an option line (starts with :)
            if stripped.startswith(":"):
                options_lines.append(stripped)
            else:
                # This is content (page references)
                content_lines.append(stripped)

        # Add the toctree block if it has content
        # (toctrees with only options but no content are typically incomplete/unused)
        if content_lines:
            options_block = "\n".join(options_lines)
            content_block = "\n".join(content_lines)
            toctree_blocks.append((options_block, content_block))

    return toctree_blocks


def _parse_toctree_entries(
    content_block: str,
    base_dir: str,
    toctree_path: str,
    processed_files: set[str] | None = None,
) -> list:
    """
    Parse entries from a toctree content block and recursively find nested toctrees.

    Args:
        content_block: The content section of a toctree directive
        base_dir: Base directory path for resolving relative paths
        toctree_path: Path to the current toctree file for context
        processed_files: Set of files already processed to prevent infinite loops

    Returns:
        List of entry dictionaries with nested children
    """
    if processed_files is None:
        processed_files = set()

    entries: list = []
    lines = content_block.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle wildcard patterns - these will be processed by glob discovery
        if "*" in line:
            # Store the glob pattern for later processing
            entries.append(
                {
                    "title": line.replace("*", "")
                    .replace("/", " ")
                    .replace("_", " ")
                    .replace("-", " ")
                    .strip()
                    .title(),
                    "url": f"/{line.replace('*', '').strip('/')}.html",
                    "is_external": False,
                    "children": [],
                    "is_glob_pattern": True,
                    "glob_pattern": line,
                }
            )
            continue

        # Handle external links (format: "Title <URL>")
        if "<" in line and ">" in line:
            # Optimized regex to avoid catastrophic backtracking:
            # Use greedy quantifier with negated character class to prevent backtracking
            title_match = re.match(
                r"^([^\n<>\s]+(?:\s+[^\n<>\s]+)*)\s*<([^<>]+)>$", line
            )
            if title_match:
                title = title_match.group(1).strip()
                url = title_match.group(2).strip()
                entries.append(
                    {
                        "title": title,
                        "url": url,
                        "is_external": True,
                        "children": [],
                    }
                )
        else:
            # Internal page reference - recursively parse nested toctrees
            # Handle special case: 'self' refers to the current file
            if line == "self":
                # For 'self', we don't want to create nested children, just reference the current file
                entry_path = Path(toctree_path)

                # If this is a toctree file, 'self' should refer to the main index
                if entry_path.stem == "toctree":
                    # Point to the main index.rst file in script-docs directory
                    if Path("script-docs").exists():
                        main_index_path = Path("script-docs") / "index.rst"
                    else:
                        main_index_path = Path("index.rst")
                    file_title = extract_file_title(str(main_index_path))
                    url = "/index.html"
                else:
                    # Extract title from the current file
                    file_title = extract_file_title(str(entry_path))
                    url_ext = get_url_extension(str(entry_path))
                    url = f"/{entry_path.stem}{url_ext}"

                if file_title:
                    title = file_title
                else:
                    # Fallback to filename
                    title = entry_path.stem.replace("_", " ").replace("-", " ").title()

                entries.append(
                    {
                        "title": title,
                        "url": url,
                        "is_external": False,
                        "children": [],  # No nested children for self
                    }
                )
                continue
            elif line.startswith("script-docs/"):
                # Absolute path from script-docs root
                entry_path = Path(line)
            elif "/" in line:
                # Path with directory separators - first try relative to current file's directory
                relative_path = Path(base_dir) / line
                if (
                    relative_path.exists()
                    or (relative_path.with_suffix(".rst")).exists()
                ):
                    entry_path = relative_path
                else:
                    # Fallback: resolve relative to script-docs root
                    if Path("script-docs").exists():
                        entry_path = Path("script-docs") / line
                    else:
                        entry_path = Path(line)
            else:
                # Simple filename - resolve relative to the current toctree file's directory
                entry_path = Path(base_dir) / line

            # Ensure the entry_path has the correct extension
            if not entry_path.suffix:
                # No extension, try to find the actual file
                rst_path = entry_path.with_suffix(".rst")
                ipynb_path = entry_path.with_suffix(".ipynb")
                if rst_path.exists():
                    entry_path = rst_path
                elif ipynb_path.exists():
                    entry_path = ipynb_path
                else:
                    # Default to .rst if file doesn't exist
                    entry_path = rst_path
            children = _get_nested_children(str(entry_path), processed_files)

            # Try to extract title from file first, fallback to filename
            file_title = extract_file_title(str(entry_path))
            if file_title:
                title = file_title
            else:
                # Generate title from filename as fallback
                title = line.replace("_", " ").replace("-", " ").title()

            # Determine the correct URL extension
            url_ext = get_url_extension(str(entry_path))

            # Construct the URL using the full path from entry_path
            # Convert absolute path to relative path from script-docs directory
            script_docs_path = Path(
                __file__
            ).parent  # Use absolute path to script-docs directory
            try:
                # Get relative path from script-docs directory
                relative_path = entry_path.relative_to(script_docs_path)
                url = f"/{relative_path.with_suffix(url_ext)}"
            except ValueError:
                # Fallback: try to extract the relevant parts
                parts = entry_path.parts
                if len(parts) > 1:
                    # Look for script-docs in the path parts
                    script_docs_index = None
                    for i, part in enumerate(parts):
                        if part == "script-docs":
                            script_docs_index = i
                            break

                    if script_docs_index is not None and script_docs_index + 1 < len(
                        parts
                    ):
                        # Extract path after script-docs
                        relevant_parts = parts[script_docs_index + 1 :]
                        url = f"/{'/'.join(relevant_parts).replace('.rst', url_ext).replace('.ipynb', '.ipynb.html')}"
                    else:
                        # Fallback: use the original line-based approach
                        url = f"/{line}{url_ext}"
                else:
                    # Single filename
                    url = f"/{line}{url_ext}"

            entries.append(
                {
                    "title": title,
                    "url": url,
                    "is_external": False,
                    "children": children,
                }
            )

    return entries


def _get_nested_children(
    file_path: str, processed_files: set[str] | None = None
) -> list:
    """
    Recursively get children from a file by parsing its toctree directives.
    Also uses glob patterns to discover additional nested files.

    Args:
        file_path: Path to the file to parse for nested toctrees
        processed_files: Set of files already processed to prevent infinite loops

    Returns:
        List of child entry dictionaries with absolute paths
    """
    if processed_files is None:
        processed_files = set()

    # Prevent infinite loops by tracking processed files
    if file_path in processed_files:
        return []

    processed_files.add(file_path)

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
        script_docs_path = Path(
            __file__
        ).parent  # Use absolute path to script-docs directory
        file_path_obj = Path(file_path)

        # Convert absolute path to relative path from script-docs
        try:
            # Try to get relative path from script-docs directory
            relative_path = file_path_obj.relative_to(script_docs_path)
            parent_path = relative_path.parent
            parent_url_prefix = f"/{parent_path}" if parent_path != Path(".") else ""
        except ValueError:
            # If file_path is not relative to script-docs, try to extract the relevant parts
            parts = file_path_obj.parts
            if len(parts) > 1:
                # Look for script-docs in the path parts
                script_docs_index = None
                for i, part in enumerate(parts):
                    if part == "script-docs":
                        script_docs_index = i
                        break

                if script_docs_index is not None and script_docs_index + 1 < len(parts):
                    # Extract path after script-docs
                    relevant_parts = parts[
                        script_docs_index + 1 : -1
                    ]  # Remove script-docs and filename
                    parent_url_prefix = (
                        f"/{'/'.join(relevant_parts)}" if relevant_parts else ""
                    )
                else:
                    # Handle case where file_path is already relative to script-docs
                    parent_parts = parts[:-1]  # Remove filename
                    parent_url_prefix = (
                        f"/{'/'.join(parent_parts)}" if parent_parts else ""
                    )
            else:
                parent_url_prefix = ""

        # Parse the file for toctree directives
        file_toctree_data = parse_toctree_file(file_path, processed_files)

        # Add children from the parsed toctree with absolute paths
        if file_toctree_data["entries"]:
            for entry in file_toctree_data["entries"]:
                # Update the URL to be absolute
                if not entry["is_external"]:
                    # Check if the URL is already correctly constructed (starts with / and has proper path)
                    current_url = entry["url"]
                    if current_url.startswith("/") and len(current_url.split("/")) >= 3:
                        # URL is already correctly constructed with full path, don't modify it
                        pass
                    else:
                        # Extract the path from the current URL (remove leading / and any extension)
                        path_part = current_url.lstrip("/")
                        # Remove both .html and .ipynb.html extensions
                        if path_part.endswith(".ipynb.html"):
                            path_part = path_part[:-10]  # Remove .ipynb.html
                        elif path_part.endswith(".html"):
                            path_part = path_part[:-5]  # Remove .html

                        # Determine the correct extension for this path
                        # Try to find the actual file to determine the extension
                        potential_ipynb = Path("script-docs") / f"{path_part}.ipynb"

                        if potential_ipynb.exists():
                            url_ext = ".ipynb.html"
                        else:
                            url_ext = ".html"

                        # Construct absolute path using the parent URL prefix
                        if parent_url_prefix:
                            entry["url"] = f"{parent_url_prefix}/{path_part}{url_ext}"
                        else:
                            entry["url"] = f"/{path_part}{url_ext}"

                # Children URLs are already processed by their own _get_nested_children calls
                # No need to modify them here as they will have their own absolute paths

                children.append(entry)

        # Only use glob patterns to discover additional files if wildcards are present
        # Check if any toctree entries are glob patterns
        has_wildcards = any(entry.get("is_glob_pattern", False) for entry in children)

        if has_wildcards:
            # Process glob patterns and replace placeholder entries with actual discovered files
            processed_children = []
            existing_urls = {
                child["url"]
                for child in children
                if not child.get("is_glob_pattern", False)
            }

            for entry in children:
                if entry.get("is_glob_pattern", False):
                    # This is a glob pattern entry, discover files for it
                    glob_pattern = entry.get("glob_pattern", "")
                    glob_discovered = _discover_files_with_glob_pattern(
                        file_path, glob_pattern
                    )

                    # Add discovered files
                    for discovered_entry in glob_discovered:
                        if discovered_entry["url"] not in existing_urls:
                            processed_children.append(discovered_entry)
                            existing_urls.add(discovered_entry["url"])
                else:
                    # Regular entry, keep it
                    processed_children.append(entry)

            children = processed_children

    except Exception as e:
        print(f"Error parsing nested file {file_path}: {e}")

    return children


def _discover_files_with_glob_pattern(file_path: str, glob_pattern: str) -> list:
    """
    Use a specific glob pattern to discover files.

    Args:
        file_path: Path to the file containing the glob pattern
        glob_pattern: The glob pattern to use for discovery

    Returns:
        List of discovered file entries
    """
    discovered_files: list = []

    try:
        file_path_obj = Path(file_path)
        file_dir = file_path_obj.parent

        # Convert the glob pattern to a file system pattern
        # Handle patterns like "/start/glossary/business/*"
        if glob_pattern.startswith("/"):
            # Absolute pattern from script-docs root - remove the leading slash
            pattern_path = glob_pattern.lstrip("/")
        else:
            # Relative pattern from current file directory
            pattern_path = str(file_dir / glob_pattern)

        # Use glob to find matching files
        import glob
        import os

        # Change to script-docs directory for glob to work correctly
        script_docs_path = Path(__file__).parent
        original_cwd = os.getcwd()
        try:
            os.chdir(script_docs_path)
            discovered_paths = glob.glob(str(pattern_path))
        finally:
            os.chdir(original_cwd)

        for discovered_path in discovered_paths:
            discovered_file = Path(
                discovered_path
            ).resolve()  # Resolve to absolute path

            # Skip directories and non-RST files
            if not discovered_file.is_file() or discovered_file.suffix not in [
                ".rst",
                ".ipynb",
            ]:
                continue

            # Skip index files
            if discovered_file.stem == "index":
                continue

            # Construct the URL path
            # Convert absolute path to relative path from script-docs directory
            script_docs_path = Path(
                __file__
            ).parent  # Use absolute path to script-docs directory
            try:
                # Get relative path from script-docs directory
                relative_path = discovered_file.relative_to(script_docs_path)
                url_path = f"/{relative_path.with_suffix('.html')}"
            except ValueError:
                # If not relative to script-docs, try to extract the relevant parts
                parts = discovered_file.parts
                if len(parts) > 1:
                    # Look for script-docs in the path parts
                    script_docs_index = None
                    for i, part in enumerate(parts):
                        if part == "script-docs":
                            script_docs_index = i
                            break

                    if script_docs_index is not None and script_docs_index + 1 < len(
                        parts
                    ):
                        # Extract path after script-docs
                        relevant_parts = parts[script_docs_index + 1 :]
                        url_path = f"/{'/'.join(relevant_parts).replace('.rst', '.html').replace('.ipynb', '.ipynb.html')}"
                    else:
                        # Fallback: use the filename only
                        url_path = f"/{discovered_file.name.replace('.rst', '.html').replace('.ipynb', '.ipynb.html')}"
                else:
                    # Single filename
                    url_path = f"/{discovered_file.name.replace('.rst', '.html').replace('.ipynb', '.ipynb.html')}"

            # Extract title from file
            file_title = extract_file_title(str(discovered_file))
            if file_title:
                title = file_title
            else:
                # Generate title from filename
                title = discovered_file.stem.replace("_", " ").replace("-", " ").title()

            # Create entry for discovered file
            entry = {
                "title": title,
                "url": url_path,
                "is_external": False,
                "children": [],  # Don't recursively discover children to avoid infinite loops
            }

            discovered_files.append(entry)

    except Exception as e:
        print(f"Error discovering files with glob pattern {glob_pattern}: {e}")

    return discovered_files


def _discover_files_with_glob(
    file_path: str, existing_entries: list | None = None
) -> list:
    """
    Use glob patterns to discover additional nested files that might not be in toctrees.
    Only discovers files when wildcards are present in the original toctree content.

    Args:
        file_path: Path to the file to discover nested files for
        existing_entries: List of already discovered entries to avoid duplicates

    Returns:
        List of discovered file entries
    """
    discovered_files: list = []

    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return discovered_files

        # Check if the original file content contains wildcards
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Only proceed if wildcards are present in the content
        if "*" not in content:
            return discovered_files

        # Get the directory containing the file
        file_dir = file_path_obj.parent

        # Use glob to find .rst and .ipynb files in the same directory and subdirectories
        # Only search in the same directory as the current file, not the entire script-docs tree
        patterns = [
            str(file_dir / "*.rst"),
            str(file_dir / "*.ipynb"),
            str(file_dir / "*/*.rst"),
            str(file_dir / "*/*.ipynb"),
            str(file_dir / "*/*/*.rst"),
            str(file_dir / "*/*/*.ipynb"),
        ]

        discovered_paths = set()
        for pattern in patterns:
            discovered_paths.update(glob.glob(pattern))

        # Get existing URLs to avoid duplicates
        existing_urls = set()
        if existing_entries:
            existing_urls = {entry["url"] for entry in existing_entries}

        # Filter out the current file, index files, and entries with wildcards
        current_file_stem = file_path_obj.stem
        for discovered_path in discovered_paths:
            discovered_file = Path(discovered_path)

            # Skip the current file, index files, files with * in their name, and the glob pattern itself
            if (
                discovered_file.stem == current_file_stem
                or discovered_file.stem == "index"
                or "*" in discovered_file.stem
                or discovered_file.stem == "*"  # Skip the glob pattern itself
            ):
                continue

            # Construct absolute path using the same logic as _get_nested_children
            # Get the parent URL prefix from the current file's location
            script_docs_path = Path(
                __file__
            ).parent  # Use absolute path to script-docs directory
            try:
                current_file_relative = file_path_obj.relative_to(script_docs_path)
                parent_path = current_file_relative.parent
                parent_url_prefix = (
                    f"/{parent_path}" if parent_path != Path(".") else ""
                )
            except ValueError:
                # If not relative to script-docs, try to extract the relevant parts
                parts = file_path_obj.parts
                if len(parts) > 1:
                    # Look for script-docs in the path parts
                    script_docs_index = None
                    for i, part in enumerate(parts):
                        if part == "script-docs":
                            script_docs_index = i
                            break

                    if script_docs_index is not None and script_docs_index + 1 < len(
                        parts
                    ):
                        # Extract path after script-docs
                        relevant_parts = parts[
                            script_docs_index + 1 : -1
                        ]  # Remove script-docs and filename
                        parent_url_prefix = (
                            f"/{'/'.join(relevant_parts)}" if relevant_parts else ""
                        )
                    else:
                        # Handle case where file_path is already relative to script-docs
                        parent_parts = parts[:-1]  # Remove filename
                        parent_url_prefix = (
                            f"/{'/'.join(parent_parts)}" if parent_parts else ""
                        )
                else:
                    parent_url_prefix = ""

            # Determine the correct URL extension for the discovered file
            url_ext = get_url_extension(str(discovered_file))

            # Construct absolute URL using the parent prefix
            if parent_url_prefix:
                url_path = f"{parent_url_prefix}/{discovered_file.stem}{url_ext}"
            else:
                # If no parent prefix, we need to construct the full path from script-docs
                script_docs_path = Path(
                    __file__
                ).parent  # Use absolute path to script-docs directory
                try:
                    # Get relative path from script-docs directory
                    relative_path = discovered_file.relative_to(script_docs_path)
                    url_path = f"/{relative_path.with_suffix(url_ext)}"
                except ValueError:
                    # Fallback: try to extract the relevant parts
                    parts = discovered_file.parts
                    if len(parts) > 1:
                        # Look for script-docs in the path parts
                        script_docs_index = None
                        for i, part in enumerate(parts):
                            if part == "script-docs":
                                script_docs_index = i
                                break

                        if (
                            script_docs_index is not None
                            and script_docs_index + 1 < len(parts)
                        ):
                            # Extract path after script-docs
                            relevant_parts = parts[script_docs_index + 1 :]
                            url_path = f"/{'/'.join(relevant_parts).replace('.rst', url_ext).replace('.ipynb', '.ipynb.html')}"
                        else:
                            # Fallback: use the filename only
                            url_path = f"/{discovered_file.stem}{url_ext}"
                    else:
                        # Single filename
                        url_path = f"/{discovered_file.stem}{url_ext}"

            # Skip if already exists
            if url_path in existing_urls:
                continue

            # Try to extract title from file first, fallback to filename
            file_title = extract_file_title(str(discovered_file))
            if file_title:
                title = file_title
            else:
                # Generate title from filename as fallback
                title = discovered_file.stem.replace("_", " ").replace("-", " ").title()

            # Create entry for discovered file
            entry = {
                "title": title,
                "url": url_path,
                "is_external": False,
                "children": [],  # Don't recursively discover children to avoid infinite loops
            }

            discovered_files.append(entry)

    except Exception as e:
        print(f"Error discovering files with glob for {file_path}: {e}")

    return discovered_files


def generate_sidebar_html(toctree_data: dict, sidebar_name: str) -> str:
    """
    Generate HTML sidebar template from toctree data with nested structure.
    Supports multiple sections with separate headers when multiple toctrees are present.

    Args:
        toctree_data: Parsed toctree data (with "sections" list or "caption"/"entries" for backward compatibility)
        sidebar_name: Name for the sidebar template file

    Returns:
        HTML content for the sidebar template
    """
    html_parts = []

    # Check if we have multiple sections
    if "sections" in toctree_data and len(toctree_data["sections"]) > 1:
        # Multiple sections - generate all captions and lists in the same nav table
        html_parts.append('<nav class="table w-full min-w-full my-6 lg:my-8">')

        for section in toctree_data["sections"]:
            if not section.get("entries"):
                continue  # Skip empty sections

            caption = section.get("caption", "")
            if caption:
                html_parts.append(
                    f'  <p class="caption" role="heading"><span class="caption-text">{caption}</span></p>'
                )
            html_parts.append('  <ul class="current">')

            for entry in section["entries"]:
                html_parts.extend(_generate_entry_html(entry, level=1))

            html_parts.append("  </ul>")

        html_parts.append("</nav>")
    else:
        # Single section - use backward compatible format
        caption = toctree_data.get("caption", "")
        entries = toctree_data.get("entries", [])

        html_parts.append('<nav class="table w-full min-w-full my-6 lg:my-8">')
        if caption:
            html_parts.append(
                f'  <p class="caption" role="heading"><span class="caption-text">{caption}</span></p>'
            )
        html_parts.append('  <ul class="current">')

        for entry in entries:
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
        # Theme already adds external link icon via awesome_external_links
        title_with_icon = entry["title"]
    else:
        link_class = "reference internal"
        title_with_icon = entry["title"]

    # Generate the main entry
    if entry.get("children"):
        # Entry with children - create expandable structure with Alpine.js
        expandable_class = "expandable"
        alpine_data = "x-data=\"{ expanded: $el.classList.contains('current') || $el.querySelector('.current') ? true : false }\""
        alpine_click = '@click="expanded = !expanded"'
        alpine_class = ":class=\"{ 'expanded' : expanded }\""
        alpine_show = 'x-show="expanded"'

        html_lines.append(f'{indent}<li class="{css_class}" {alpine_data}>')
        html_lines.append(
            f'{indent}  <a {alpine_class} {alpine_click} class="{link_class} {expandable_class}" href="{entry["url"]}">{title_with_icon}<button {alpine_click.replace("@click", "@click.prevent.stop")} type="button"><span class="sr-only"></span><svg fill="currentColor" height="18px" stroke="none" viewBox="0 0 24 24" width="18px" xmlns="http://www.w3.org/2000/svg"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></svg></button></a>'
        )
        html_lines.append(f"{indent}  <ul {alpine_show}>")

        # Generate children
        for child in entry["children"]:
            html_lines.extend(_generate_entry_html(child, level + 1))

        html_lines.append(f"{indent}  </ul>")
        html_lines.append(f"{indent}</li>")
    else:
        # Simple entry without children
        html_lines.append(
            f'{indent}<li class="{css_class}"><a class="{link_class}" href="{entry["url"]}">{title_with_icon}</a></li>'
        )

    html_lines = [line for line in html_lines if "*" not in line]
    html_lines = [
        line.replace("toctree_start.html", "index.html") for line in html_lines
    ]
    html_lines = [line.replace(".ipynb..html", ".html") for line in html_lines]
    html_lines = [line.replace(".ipynb.html", ".html") for line in html_lines]

    return html_lines
