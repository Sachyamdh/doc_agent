import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

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
    should_ignore = dirname in IGNORE_DIRS
    if should_ignore:
        logger.debug(f"Ignoring directory: {dirname}")
    return should_ignore

def should_ignore_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    should_ignore = ext in IGNORE_EXTENSIONS
    if should_ignore:
        logger.debug(f"Ignoring file: {filename} (extension: {ext})")
    return should_ignore

def get_repo_structure(repo_path: str) -> dict:
    logger.info(f"Building repository structure for: {repo_path}")
    structure = {}
    total_dirs = 0
    total_files = 0
    
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
            total_dirs += 1
            total_files += len(files)
    
    logger.info(f"Repository structure built: {total_dirs} directories, {total_files} files")
    logger.debug(f"Structure keys: {list(structure.keys())[:10]}...")  # Show first 10 dirs
    return structure