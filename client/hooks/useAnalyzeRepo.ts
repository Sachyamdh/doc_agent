import { AnalyzeService, RepoDownloadService } from "@/services/RepoService";
import { useMutation } from "@tanstack/react-query";


export const STEPS = [
  "Validating repository",
  "Scanning and Chunking",
  "Analyzing with AI",
  "Generating documentation",
];

export function useAnalyzeRepo(onStepChange: (step: number) => void) {
  return useMutation({
    mutationFn: async ({ repoPath, projectSize }: any) => {
      onStepChange(0);
      await AnalyzeService.validate(repoPath);

      onStepChange(1);
      const chunkAndAnalyzeRes = await AnalyzeService.scan(repoPath);
      // onStepChange(2);
      // const chunkRes = await AnalyzeService.chunk(repoPath, projectSize);

      onStepChange(2);
      const analyzeRes = await AnalyzeService.analyzeChunks(chunkAndAnalyzeRes.chunks,chunkAndAnalyzeRes.repo_structure );
      console.log(analyzeRes)
      onStepChange(3);
      const docRes = await AnalyzeService.generateDoc(analyzeRes.analysis_results,chunkAndAnalyzeRes.repo_structure);

      return docRes.documentation;
    },
  });
}

