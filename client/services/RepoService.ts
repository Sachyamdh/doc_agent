import simpleGit from "simple-git";
import path from "path";
import fs from "fs";

type AnalyzeOptions = {
  repoUrl: string;
  projectSize: "SMALL" | "MEDIUM" | "LARGE";
};

export class RepoService {
  repoUrl: string;
  projectSize: "SMALL" | "MEDIUM" | "LARGE";
  localPath: string;

  constructor({ repoUrl, projectSize }: AnalyzeOptions) {
    this.repoUrl = repoUrl;
    this.projectSize = projectSize;
    const backendPath = path.resolve(process.cwd(), "..","backend");
    const tmpPath = path.join(backendPath, "tmp");
    console.info(`Backend path: ${backendPath}`);
    if (!fs.existsSync(tmpPath)) {
    fs.mkdirSync(tmpPath);
  }

  this.localPath = path.join(tmpPath, repoUrl.split("/").pop() || "repo");
  }

  async downloadRepo() {
    const git = simpleGit();
    if (fs.existsSync(this.localPath)) {
      fs.rmSync(this.localPath, { recursive: true, force: true });
    }
    console.log(`Cloning ${this.repoUrl} into ${this.localPath}`);
    await git.clone(this.repoUrl, this.localPath);
    return this.localPath;
  }

  async analyzeRepoBackend() {
     fs.rmSync(this.localPath, { recursive: true, force: true });

    // const res = await fetch("http://localhost:8000/analyze", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ repoPath: this.localPath, projectSize: this.projectSize }),
    // });
    // if (!res.ok) throw new Error("Backend analysis failed");
    // return res.json(); 
  }

  // 3️⃣ Full pipeline
  async run() {
    await this.downloadRepo();
    setTimeout(() => {  
        
      this.analyzeRepoBackend();
    },10000)
    return "Analysis complete (dummy response)";
  }
}
