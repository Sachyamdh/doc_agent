from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from agents.repo_reader.repo_scaner import RepoScanner
import os 

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "doc-agent-backend"
    })

@app.route("/analyze", methods=["POST"])
def analyze_repo():
    data = request.json
    
    repo_path = data.get("repoPath")
    project_size = data.get("projectSize")
    print(repo_path)
    print(os.path.exists(repo_path))
    if not repo_path:
        return jsonify({"error": "repoPath is required"}), 400
    
    if not os.path.exists(repo_path):
        return jsonify({"error": "repoPath does not exist"}), 400

    try:
        scanner = RepoScanner(repo_path)
        scan_result = scanner.scan()
        chunks = scanner.chunk_files(project_size)

        return jsonify({
        "status": "ready_for_ai",
        "total_files": len(scanner.files),
        "total_chunks": len(chunks),
        "chunks_preview": chunks[:5]
    })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
