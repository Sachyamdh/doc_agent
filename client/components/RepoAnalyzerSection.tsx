"use client";

import { useState } from "react";
import RepoForm from "./RepoForm";
import CircularProgress from "./CircularProgressBar";
import { useAnalyzeRepo, STEPS } from "@/hooks/useAnalyzeRepo";
import ReactMarkdown from "react-markdown";

export default function RepoAnalyzerSection() {
  const [repoUrl, setRepoUrl] = useState("");
  const [projectSize, setProjectSize] = useState<"SMALL" | "MEDIUM">("SMALL");
  const [currentStep, setCurrentStep] = useState(0);
  const [document, setDocument] = useState("");

  const analyzeMutation = useAnalyzeRepo((step) => {
    setCurrentStep(step);
  });

  const handleAnalyze = () => {
    setDocument("");
    analyzeMutation.mutate(
      { repoPath: repoUrl, projectSize },
      {
        onSuccess: (doc) => setDocument(doc),
      }
    );
  };

  return (
    <div className="flex flex-col md:flex-row gap-6">
      {/* Left */}
      <div className="md:w-1/3 space-y-6">
        <RepoForm
          repoUrl={repoUrl}
          setRepoUrl={setRepoUrl}
          projectSize={projectSize}
          setProjectSize={setProjectSize}
          onSubmit={handleAnalyze}
        />

        <div className="space-y-4">
          {STEPS.map((step, idx) => (
            <CircularProgress
              key={step}
              progress={currentStep > idx ? 100 : 0}
              label={step}
            />
          ))}
        </div>
      </div>

      {/* Right */}
      <div className="md:w-2/3 bg-bg-secondary p-6 rounded-xl min-h-[300px] overflow-auto">
        {analyzeMutation.isLoading && (
          <p className="text-text-secondary">
            {STEPS[currentStep] || "Processing..."}
          </p>
        )}

        {analyzeMutation.isError && (
          <p className="text-red-500">
            {(analyzeMutation.error as Error)?.message}
          </p>
        )}

        {document && (
          <article className="prose prose-invert max-w-none">
            <ReactMarkdown>{document}</ReactMarkdown>
          </article>
        )}

        {!document && !analyzeMutation.isLoading && (
          <p className="text-text-muted">Your documentation will be shown here.......</p>
        )}
      </div>
    </div>
  );
}
