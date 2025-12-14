

const API = "http://localhost:8000/analyze";



export class AnalyzeService {
  static validate(repoPath: string) {
    return fetch(`${API}/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repoPath }),
    }).then(res => res.json());
  }

  static scan(repoPath: string) {
    return fetch(`${API}/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repoPath }),
    }).then(res => res.json());
  }

  static chunk(repoPath: string, projectSize: string) {
    return fetch(`${API}/chunk`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repoPath, projectSize }),
    }).then(res => res.json());
  }

  static analyzeChunks(chunks: string, repoStructure:strin) {
    return fetch(`${API}/analyze-chunks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chunks,repoStructure }),
    }).then(res => res.json());
  }

  static generateDoc(summaries: any[]) {
    return fetch(`${API}/generate-doc`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ summaries }),
    }).then(res => res.json());
  }
}
