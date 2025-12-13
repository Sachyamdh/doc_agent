import os

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".venv",
    "venv"
}

IGNORE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".ico", ".bmp", ".tiff"
}

def should_ignore_dir(dirname: str) -> bool:
    return dirname in IGNORE_DIRS

def should_ignore_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in IGNORE_EXTENSIONS
