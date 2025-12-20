import { RepoDownloadService } from "@/services/DownloadService";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { repoUrl, projectSize } = body;

    const downloader = new RepoDownloadService({ repoUrl, projectSize });
    await downloader.fetchAndSaveFiles();

    return NextResponse.json({ repoPath: downloader.localPath }, { status: 200 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
