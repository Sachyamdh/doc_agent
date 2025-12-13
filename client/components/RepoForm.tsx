"use client";

type ProjectSize = "SMALL" | "MEDIUM";

interface RepoFormProps {
  repoUrl: string;
  setRepoUrl: (url: string) => void;
  projectSize: ProjectSize;
  setProjectSize: (size: ProjectSize) => void;
  onSubmit: () => void;
}

export default function RepoForm({
  repoUrl,
  setRepoUrl,
  projectSize,
  setProjectSize,
  onSubmit,
}: RepoFormProps) {
  const isValidRepo =
    repoUrl.startsWith("https://github.com/") &&
    repoUrl.split("/").length >= 5;

  return (
    <div className="card p-6 space-y-5">
      <div className="space-y-2">
        <label className="text-sm text-text-secondary">
          GitHub Repository URL
        </label>
        <input
          className="input"
          placeholder="https://github.com/user/repo"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm text-text-secondary">
          Project Size
        </label>
        <div className="flex gap-3">
          {(["SMALL", "MEDIUM"] as ProjectSize[]).map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => setProjectSize(option)}
              className={`badge ${
                projectSize === option ? "border-brand text-brand" : ""
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      <button
        className="btn btn-primary w-full disabled:opacity-50"
        disabled={!isValidRepo}
        onClick={onSubmit}
      >
        Generate Document
      </button>
    </div>
  );
}
