from flask import Blueprint, request, jsonify
import os
import traceback
from agents.repo_reader.repo_scaner import RepoScanner
from agents.bootstrap import build_orchestrator
from utils.file_filter import get_repo_structure

analyze_bp = Blueprint("analyze", __name__, url_prefix="/analyze")


# ----------------------------
# Validate repository path
# ----------------------------
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


# ----------------------------
# Scan repo and create chunks
# ----------------------------
@analyze_bp.route("/scan-and-chunk", methods=["POST"])
def scan_repo():
    data = request.json
    repo_path = data.get("repoPath")

    try:
        scanner = RepoScanner(repo_path)
        scanner.scan()
        chunks = scanner.chunk_files()
        repo_structure = get_repo_structure(repo_path)

        return jsonify({
            "status": "prepared",
            "chunks": chunks,
            "repo_structure": repo_structure,
            "metadata": {
                "total_files": len(scanner.files),
                "total_chunks": len(chunks)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


# ----------------------------
# Analyze chunks (MULTI-AGENT)
# ----------------------------
@analyze_bp.route("/analyze-chunks", methods=["POST"])
def analyze_chunks():
    data = request.json
    chunks = data.get("chunks")
    repo_structure = data.get("repoStructure")

    if not chunks:
        return jsonify({"error": "chunks are required"}), 400

    if not repo_structure:
        return jsonify({"error": "repoStructure is required"}), 400

    orchestrator = build_orchestrator()

    try:
        result = orchestrator.run(chunks, repo_structure)

        chunk_summaries = result.get("chunk_summaries", [])
        quality_and_improvements = result.get("quality_and_improvements", "")

        return jsonify({
            "status": "analyzed",
            "analysis_results": {
                "chunk_summaries": chunk_summaries,
                "quality_and_improvements": quality_and_improvements,
                "metadata": {
                    "total_chunks": len(chunk_summaries),
                    "total_files": len(set(
                        s["path"] for s in chunk_summaries
                    )),
                    "analysis_complete": True
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


# ----------------------------
# Generate documentation
# ----------------------------
@analyze_bp.route("/generate-doc", methods=["POST"])
def generate_doc():
    data = request.json
    analysis_results = data.get("analysisResults")
    repo_structure = data.get("repoStructure")

    if not analysis_results:
        return jsonify({"error": "analysisResults are required"}), 400

    if not repo_structure:
        return jsonify({"error": "repoStructure is required"}), 400

    orchestrator = build_orchestrator()

    try:
        context = {
            "chunk_summaries": analysis_results.get("chunk_summaries"),
            "quality_and_improvements": analysis_results.get("quality_and_improvements"),
            "repo_structure": repo_structure
        }

        documentation_result = orchestrator.agents["documentation"].run(context)

        return jsonify({
            "status": "completed",
            "documentation": documentation_result["documentation"],
            "metadata": analysis_results.get("metadata", {})
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500
