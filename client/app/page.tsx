import RepoAnalyzerSection from "@/components/RepoAnalyzerSection";

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-5xl space-y-6">
        <h1 className="text-3xl font-bold">Repo Intelligence Agent</h1>
        <p className="text-text-secondary">
          Enter a GitHub repository URL, and generate documentation interactively.
        </p>

        <RepoAnalyzerSection />
      </div>
    </main>
  );
}
