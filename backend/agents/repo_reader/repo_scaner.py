import os
import re
from utils.file_filter import should_ignore_dir, should_ignore_file
from utils.constants import EXT_LANG_MAP,CHUNK_SIZES


class RepoScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.files = []

    # ---------- Step 1: Scan and read files ----------
    def scan(self):
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not should_ignore_dir(d)]

            for file in files:
                if should_ignore_file(file):
                    continue

                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self.repo_path)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
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

        return {
            "total_files": len(self.files),
            "files": self.files
        }

    # ---------- Step 2: Logical chunking ----------
    def chunk_files(self, project_size="SMALL"):
        chunk_limit = CHUNK_SIZES.get(project_size, 2000)
        chunks = []

        for file in self.files:
            content = file["content"]
            path = file["path"]
            language = file["language"]
            file_type = file["type"]

            # Determine split points
            split_points = []

            if language in ["JavaScript", "TypeScript", "Python", "Java"]:
                # Split by functions or classes
                pattern = r'(?:def\s+\w+\(|function\s+\w+\(|class\s+\w+)'
                split_points = [m.start() for m in re.finditer(pattern, content)]
            elif language == "Markdown":
                # Split by headings
                pattern = r'(?:^#{1,6}\s)'
                split_points = [m.start() for m in re.finditer(pattern, content, re.MULTILINE)]

            # fallback if no split points
            if not split_points:
                split_points = list(range(0, len(content), chunk_limit))
            else:
                # add end of content as last split
                if split_points[-1] != len(content):
                    split_points.append(len(content))

            # create chunks
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

        return chunks