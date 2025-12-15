import os
import re
from utils.file_filter import should_ignore_dir, should_ignore_file
from utils.constants import EXT_LANG_MAP,CHUNK_SIZES
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RepoScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.files = []
        logger.info(f"RepoScanner initialized for path: {repo_path}")

    # ---------- Step 1: Scan and read files ----------
    def scan(self):
        logger.info(f"Starting repository scan: {self.repo_path}")
        file_count = 0
        ignored_dirs = 0
        ignored_files = 0
        error_files = 0
        
        for root, dirs, files in os.walk(self.repo_path):
            # Filter ignored directories
            original_dir_count = len(dirs)
            dirs[:] = [d for d in dirs if not should_ignore_dir(d)]
            ignored_dirs += original_dir_count - len(dirs)

            for file in files:
                if should_ignore_file(file):
                    ignored_files += 1
                    continue

                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self.repo_path)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    file_count += 1
                except Exception as e:
                    logger.warning(f"Could not read file {relative_path}: {str(e)}")
                    error_files += 1
                    continue

                ext = os.path.splitext(file)[1].lower()
                language = EXT_LANG_MAP.get(ext, "Unknown")

                # classify type
                file_type = "source"
                if "test" in relative_path.lower():
                    file_type = "test"
                elif ext in [".md", ".txt"]:
                    file_type = "doc"

                self.files.append({
                    "path": relative_path,
                    "size": len(content),
                    "extension": ext,
                    "language": language,
                    "type": file_type,
                    "content": content
                })

        logger.info(f"Scan completed: {file_count} files processed, {ignored_dirs} dirs ignored, {ignored_files} files ignored, {error_files} errors")
        logger.debug(f"File types found: {set(f['language'] for f in self.files)}")
        
        return {
            "total_files": len(self.files),
            "files": self.files
        }

    # ---------- Step 2: Logical chunking ----------
    def chunk_files(self, project_size="SMALL"):
        logger.info(f"Starting file chunking with project size: {project_size}")
        chunk_limit = CHUNK_SIZES.get(project_size, 2000)
        logger.debug(f"Chunk limit set to: {chunk_limit} characters")
        chunks = []

        for idx, file in enumerate(self.files):
            content = file["content"]
            path = file["path"]
            language = file["language"]
            file_type = file["type"]
            
            logger.debug(f"Chunking file {idx + 1}/{len(self.files)}: {path} ({language})")

            # Determine split points
            split_points = []

            if language in ["JavaScript", "TypeScript", "Python", "Java"]:
                # Split by functions or classes
                pattern = r'(?:def\s+\w+\(|function\s+\w+\(|class\s+\w+)'
                split_points = [m.start() for m in re.finditer(pattern, content)]
                logger.debug(f"Found {len(split_points)} code structure split points in {path}")
            elif language == "Markdown":
                # Split by headings
                pattern = r'(?:^#{1,6}\s)'
                split_points = [m.start() for m in re.finditer(pattern, content, re.MULTILINE)]
                logger.debug(f"Found {len(split_points)} heading split points in {path}")

            # fallback if no split points
            if not split_points:
                split_points = list(range(0, len(content), chunk_limit))
                logger.debug(f"Using fallback chunking for {path}: {len(split_points)} chunks")
            else:
                # add end of content as last split
                if split_points[-1] != len(content):
                    split_points.append(len(content))

            # create chunks
            file_chunks = 0
            for i in range(len(split_points)-1):
                start = split_points[i]
                end = split_points[i+1]
                chunk_content = content[start:end].strip()
                if not chunk_content:
                    continue
                chunks.append({
                    "path": path,
                    "language": language,
                    "type": file_type,
                    "size": len(chunk_content),
                    "content": chunk_content,
                    "start_line": content[:start].count("\n") + 1,
                    "end_line": content[:end].count("\n")
                })
                file_chunks += 1
            
            logger.debug(f"Created {file_chunks} chunks for {path}")

        logger.info(f"Chunking completed: {len(chunks)} total chunks from {len(self.files)} files")
        logger.debug(f"Average chunks per file: {len(chunks) / len(self.files) if self.files else 0:.2f}")
        return chunks