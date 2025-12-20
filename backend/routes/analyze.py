from flask import Blueprint, request, jsonify
import os
import traceback
from agents.repo_reader.repo_scaner import RepoScanner
from agents.bootstrap import build_orchestrator
from utils.file_filter import get_repo_structure
from utils.logger import setup_logger

analyze_bp = Blueprint("analyze", __name__, url_prefix="/analyze")
logger = setup_logger(__name__)


@analyze_bp.route("/validate", methods=["POST"])
def validate_repo():
    logger.info("Validate repo endpoint called")
    data = request.json
    repo_path = data.get("repoPath")
    
    logger.debug(f"Validating repo path: {repo_path}")

    if not repo_path:
        logger.warning("Validation failed: repoPath is required")
        return jsonify({"error": "repoPath is required"}), 400

    if not os.path.exists(repo_path):
        logger.warning(f"Validation failed: repoPath does not exist - {repo_path}")
        return jsonify({"error": "repoPath does not exist"}), 400

    logger.info(f"Repo validated successfully: {repo_path}")
    return jsonify({
        "status": "valid",
        "repoPath": repo_path
    })


# ----------------------------
# Scan repo and create chunks
# ----------------------------
@analyze_bp.route("/scan-and-chunk", methods=["POST"])
def scan_repo():
    logger.info("Scan and chunk endpoint called")
    data = request.json
    repo_path = data.get("repoPath")
    
    logger.debug(f"Starting scan for repo: {repo_path}")

    try:
        scanner = RepoScanner(repo_path)
        logger.info("RepoScanner initialized")
        
        scanner.scan()
        logger.info(f"Repo scanned successfully, found {len(scanner.files)} files")
        
        chunks = scanner.chunk_files()
        logger.info(f"Files chunked successfully, created {len(chunks)} chunks")
        
        repo_structure = get_repo_structure(repo_path)
        logger.debug(f"Repo structure extracted with {len(repo_structure)} directories")

        result = {
            "status": "prepared",
            "chunks": chunks,
            "repo_structure": repo_structure,
            "metadata": {
                "total_files": len(scanner.files),
                "total_chunks": len(chunks)
            }
        }
        logger.info(f"Scan and chunk completed: {result['metadata']}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in scan_repo: {str(e)}", exc_info=True)
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
    logger.info("Analyze chunks endpoint called")
    data = request.json
    chunks = data.get("chunks")
    repo_structure = data.get("repoStructure")
    
    logger.debug(f"Received {len(chunks) if chunks else 0} chunks for analysis")

    if not chunks:
        logger.warning("Analysis failed: chunks are required")
        return jsonify({"error": "chunks are required"}), 400

    if not repo_structure:
        logger.warning("Analysis failed: repoStructure is required")
        return jsonify({"error": "repoStructure is required"}), 400

    logger.info("Building orchestrator for chunk analysis")
    orchestrator = build_orchestrator()

    try:
        logger.info("Starting orchestrator run for chunk analysis")
        result = orchestrator.run(chunks, repo_structure)
        logger.info("Orchestrator run completed successfully")

        chunk_summaries = result.get("chunk_summaries", [])
        quality_and_improvements = result.get("quality_and_improvements", "")
        
        logger.info(f"Analysis complete: {len(chunk_summaries)} summaries generated")

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
        logger.error(f"Error in analyze_chunks: {str(e)}", exc_info=True)
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
    logger.info("Generate documentation endpoint called")
    data = request.json
    analysis_results = data.get("analysisResults")
    repo_structure = data.get("repoStructure")
    
    logger.debug("Validating input for documentation generation")

    if not analysis_results:
        logger.warning("Documentation generation failed: analysisResults are required")
        return jsonify({"error": "analysisResults are required"}), 400

    if not repo_structure:
        logger.warning("Documentation generation failed: repoStructure is required")
        return jsonify({"error": "repoStructure is required"}), 400

    logger.info("Building orchestrator for documentation generation")
    orchestrator = build_orchestrator()

    try:
        context = {
            "chunk_summaries": analysis_results.get("chunk_summaries"),
            "quality_and_improvements": analysis_results.get("quality_and_improvements"),
            "repo_structure": repo_structure
        }
        logger.info("Starting documentation generation")

        documentation_result = orchestrator.agents["documentation"].run(context)
        logger.info("Documentation generated successfully")

        return jsonify({
            "status": "completed",
            "documentation": documentation_result["documentation"],
            "metadata": analysis_results.get("metadata", {})
        }), 200

    except Exception as e:
        logger.error(f"Error in generate_doc: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500
