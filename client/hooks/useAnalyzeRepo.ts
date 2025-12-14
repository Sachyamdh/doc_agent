import { AnalyzeService } from "@/services/RepoService";
import { useMutation } from "@tanstack/react-query";


export const STEPS = [
  "Validating repository",
  "Scanning files",
  "Chunking code",
  "Analyzing with AI",
  "Generating documentation",
];

export function useAnalyzeRepo(onStepChange: (step: number) => void) {
  return useMutation({
    mutationFn: async ({ repoPath, projectSize }: any) => {
      onStepChange(0);
      await AnalyzeService.validate(repoPath);

      onStepChange(1);
      await AnalyzeService.scan(repoPath);

      onStepChange(2);
      const chunkRes = await AnalyzeService.chunk(repoPath, projectSize);

      onStepChange(3);
      const analyzeRes = await AnalyzeService.analyzeChunks(chunkRes.chunk_preview);

      onStepChange(4);
      const docRes = await AnalyzeService.generateDoc(analyzeRes.summaries);

      return docRes.document;
    },
  });
}
