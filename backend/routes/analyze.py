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
    scanner.scan()
    chunks = scanner.chunk_files(project_size)
    repo_structure = get_repo_structure(temp_dir)
    
    return jsonify({
        "status": "prepared",
        "chunks": chunks,
        "repo_structure": repo_structure,
        "metadata": {
            "total_files": len(scanner.files),
            "total_chunks": len(chunks)
        }
    }),200

    except Exception as e:
        import traceback
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

# @analyze_bp.route("/chunk", methods=["POST"])
# def chunk_repo():
#     data = request.json
#     repo_path = data.get("repoPath")
#     project_size = data.get("projectSize", "medium")

#     scanner = RepoScanner(repo_path)
#     scanner.scan()
#     chunks = scanner.chunk_files(project_size)

#     return jsonify({
#         "status": "chunked",
#         "total_chunks": len(chunks),
#         "chunk_preview": chunks[:3]
#     }),200


@analyze_bp.route("/analyze-chunks", methods=["POST"])
def analyze_chunks():
    data = request.json
    chunks = data.get("chunks")
    repo_structure = data.get("repoStructure")

    if not chunks:
        return jsonify({"error": "chunks are required"}), 400
    
    if not repo_structure:
        return jsonify({"error": "repoStructure is required"}), 400

    agent = MultiAIAgent()

    def progress_callback(current, total, phase):
        print(f"[{phase}] Progress: {current}/{total}")

    try:
        analysis_results = agent.analyze_chunks(chunks, repo_structure, progress_callback)

        return jsonify({
            "status": "analyzed",
            "analysis_results": analysis_results
        })
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


@analyze_bp.route("/generate-doc", methods=["POST"])
def generate_doc():
    data = request.json
    analysis_results = data.get("analysisResults")
    repo_structure = data.get("repoStructure")

    if not analysis_results:
        return jsonify({"error": "analysisResults are required"}), 400

    if not repo_structure:
        return jsonify({"error": "repoStructure is required"}), 400

    agent = MultiAIAgent()

    try:
        documentation = agent.generate_document(analysis_results, repo_structure)

        return jsonify({
            "status": "completed",
            "documentation": documentation,
            "metadata": analysis_results.get('metadata', {})
        })
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

