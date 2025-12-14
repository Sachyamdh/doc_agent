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

def get_repo_structure(repo_path: str) -> dict:
    structure = {}
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in [
            '.git', 'node_modules', '__pycache__', 'venv', '.venv', 
            'dist', 'build', '.next', 'coverage', '.pytest_cache'
        ]]
        
        files = [f for f in files if not f.startswith('.') and f not in [
            'package-lock.json', 'yarn.lock', 'poetry.lock', '.DS_Store'
        ]]
        
        if files:
            rel_path = os.path.relpath(root, repo_path)
            if rel_path == '.':
                rel_path = 'root'
            structure[rel_path] = files
    
    return structure