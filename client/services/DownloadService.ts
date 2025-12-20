import fs from "fs";
import path from "path";

type AnalyzeOptions = {
  repoUrl: string;
  projectSize: "SMALL" | "MEDIUM" | "LARGE";
}
type FileObject = {
  path: string;
  content: string;
};
export class RepoDownloadService{
  repoUrl: string;
  projectSize: "SMALL" | "MEDIUM" | "LARGE";
  repoOwner: string;
  repoName: string;
  localPath: string;

  constructor({ repoUrl, projectSize }: AnalyzeOptions) {
    this.repoUrl = repoUrl;
    this.projectSize = projectSize;

    const match = repoUrl.match(/github\.com\/([^/]+)\/([^/]+)/);
    if (!match) throw new Error("Invalid GitHub URL");

    this.repoOwner = match[1];
    this.repoName = match[2];

    // Temp folder to save files
    console.info("default directory",path.join(process.cwd(),"../backend/tmp"))
    const tmpDir = path.join(process.cwd(), "../backend/tmp");
    if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir);
    this.localPath = path.join(tmpDir, this.repoName);

    if (!fs.existsSync(this.localPath)) fs.mkdirSync(this.localPath, { recursive: true });
  }

  // Fetch file tree
  async fetchFileTree(): Promise<string[]> {
    const res = await fetch(
      `https://api.github.com/repos/${this.repoOwner}/${this.repoName}/git/trees/main?recursive=1`
    );
    if (!res.ok) throw new Error("Failed to fetch file tree");
    const data = await res.json();
    return data.tree.filter((f: any) => f.type === "blob").map((f: any) => f.path);
  }

  async fetchAndSaveFiles(): Promise<FileObject[]> {
    const paths = await this.fetchFileTree();
    const files: FileObject[] = [];

    for (const filePath of paths) {
      try {
        const res = await fetch(
          `https://raw.githubusercontent.com/${this.repoOwner}/${this.repoName}/main/${filePath}`
        );
        if (!res.ok) continue;

        const content = await res.text();
        const localFilePath = path.join(this.localPath, filePath);
        const dir = path.dirname(localFilePath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

        fs.writeFileSync(localFilePath, content, "utf-8");

        files.push({ path: filePath, content });
      } catch (err) {
        console.warn(`Failed to fetch/save file: ${filePath}`);
      }
    }

    return files;
  }


}