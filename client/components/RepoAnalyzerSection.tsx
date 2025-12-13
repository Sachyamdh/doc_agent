"use client";

import { useState,useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import RepoForm from "./RepoForm";
import CircularProgress from "./CircularProgressBar";

type RepoMutationVars = { repoUrl: string; size: string };




export default function RepoAnalyzerSection() {
  const [repoUrl, setRepoUrl] = useState("");
  const [projectSize, setProjectSize] = useState<"SMALL" | "MEDIUM">("SMALL");
  const [currentStep, setCurrentStep] = useState(0);
  const [repoData, setRepoData] = useState("");

  const steps = [
    "Validating URL",
    "Reading repository",
    "Processing thoughts",
    "Generating document",
  ];

// const mutation = useMutation<string, Error, RepoMutationVars>({
//   mutationFn: async ({ repoUrl, size }) => {
//     const steps = [
//       "Validating URL",
//       "Reading repository",
//       "Processing thoughts",
//       "Generating document",
//     ];

//     for (let i = 0; i < steps.length; i++) {
//       await new Promise((res) => setTimeout(res, 1500));
//       setCurrentStep(i + 1); // update progress directly
//     }

//     return `
// # Generated Document for ${repoUrl}

// ## Overview
// Dummy analysis document.

// ## Summary
// - Total files: 42
// - Languages: TypeScript, CSS
// - Structure: src/components, src/pages, etc.

// ## Notes
// Everything looks good!
// `;
//   },
//   onMutate: () => setRepoData(""),
//   onSuccess: (data) => setRepoData(data),
//   onError: (err) => alert(`Error: ${err.message}`),
// });

const analyzeRepoMutation = useMutation({
  mutationFn: async ({ repoUrl, projectSize }: { repoUrl: string; projectSize: "SMALL" | "MEDIUM" }) => {
    const res = await fetch("/api/analyze-repo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repoUrl, projectSize }),
    });
    if (!res.ok) throw new Error("Analysis failed");
    return res.json();
  },
  onSuccess: (data) => console.log("Analysis finished", data),
});

//  useEffect(() => {
//   if (!mutation.isLoading) return;

//   const interval = setInterval(() => {
//     setCurrentStep((prev) => {
//       if (prev < steps.length) return prev + 1;
//       clearInterval(interval);
//       return prev;
//     });
//   }, 1500);

//   return () => clearInterval(interval);
// }, [mutation.isLoading]);


  return (
    <div className="flex flex-col md:flex-row gap-6">
      {/* Left: Repo input & progress */}
      <div className="md:w-1/3 space-y-6">
        <RepoForm
          repoUrl={repoUrl}
          setRepoUrl={setRepoUrl}
          projectSize={projectSize}
          setProjectSize={setProjectSize}
          onSubmit={() => analyzeRepoMutation.mutate({ repoUrl, projectSize })}
        />

        <div className="space-y-4">
          {steps.map((step, idx) => (
            <CircularProgress
              key={step}
              progress={currentStep > idx ? 100 : 0}
              label={step}
            />
          ))}
        </div>
      </div>

      {/* Right: Document display */}
      <div className="md:w-2/3 bg-bg-secondary p-6 rounded-xl min-h-[300px] overflow-auto">
        {analyzeRepoMutation.isLoading ? (
          <p className="text-text-secondary">Processing repository...</p>
        ) : repoData ? (
          <pre className="whitespace-pre-wrap">{repoData}</pre>
        ) : (
          <p className="text-text-muted">Document will appear here</p>
        )}
      </div>
    </div>
  );
}
