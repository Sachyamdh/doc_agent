from flask import Blueprint, request, jsonify
from agents.repo_reader.repo_scaner import RepoScanner
from agents.llm.agent import MultiAIAgent
import os

analyze_bp = Blueprint("analyze", __name__, url_prefix="/analyze")

@analyze_bp.route("/validate", methods=["POST"])
def validate_repo():
    data = request.json
    repo_path = data.get("repoPath")

    if not repo_path:
        return jsonify({"error": "repoPath is required"}), 400

    if not os.path.exists(repo_path):
        return jsonify({"error": "repoPath does not exist"}), 400

    return jsonify({
        "status": "valid",
        "repoPath": repo_path
    })


@analyze_bp.route("/scan", methods=["POST"])
def scan_repo():
    data = request.json
    repo_path = data.get("repoPath")

    scanner = RepoScanner(repo_path)
    scan_result = scanner.scan()

    return jsonify({
        "status": "scanned",
        "total_files": len(scanner.files),
        "files": scanner.files[:20]  # preview only
    })

@analyze_bp.route("/chunk", methods=["POST"])
def chunk_repo():
    data = request.json
    repo_path = data.get("repoPath")
    project_size = data.get("projectSize", "medium")

    scanner = RepoScanner(repo_path)
    scanner.scan()
    chunks = scanner.chunk_files(project_size)

    return jsonify({
        "status": "chunked",
        "total_chunks": len(chunks),
        "chunk_preview": chunks[:3]
    })


@analyze_bp.route("/analyze-chunks", methods=["POST"])
def analyze_chunks():
    data = request.json
    chunks = data.get("chunks")

    if not chunks:
        return jsonify({"error": "chunks are required"}), 400

    agent = MultiAIAgent(code_model="openai", doc_model="gemini")

    def progress_callback(current, total):
        print(f"[AI Progress] {current}/{total}")

    summaries = agent.analyze_chunks(chunks, progress_callback)

    return jsonify({
        "status": "analyzed",
        "summaries": summaries
    })


@analyze_bp.route("/generate-doc", methods=["POST"])
def generate_doc():
    data = request.json
    summaries = data.get("summaries")

    if not summaries:
        return jsonify({"error": "summaries are required"}), 400

    agent = MultiAIAgent(code_model="openai", doc_model="gemini")
    final_doc = agent.generate_document(summaries)

    return jsonify({
        "status": "completed",
        "document": final_doc
    })
