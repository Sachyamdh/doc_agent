import { NextResponse } from "next/server";
import { RepoService } from "@/services/RepoService";

export async function POST(req: Request) {
  try {
    const { repoUrl, projectSize } = await req.json();
    console.log(`Received analysis request for ${repoUrl} with size ${projectSize}`);   
    const service = new RepoService({ repoUrl, projectSize });
    const result = await service.run();

    return NextResponse.json(result);
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
