import type {Claim, Document, VerificationResult, Evidence, PaginatedResponse} from "@/types/api";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function apiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${path}`, options);
    if (!response.ok){
        let message = "API request failed";
        
        try{
            const errorData = await response.json()
            if (errorData.error?.message){
                message = errorData.error.message;
            }
        } catch{
        }
        throw new Error(message)
    }
    return response.json();
}

export async function getClaims(
  q?: string,
  limit: number = 10,
  offset: number = 0
): Promise<PaginatedResponse<Claim>> {
  const params = new URLSearchParams();

  params.set("limit", String(limit));
  params.set("offset", String(offset));

  if (q !== undefined && q.trim() !== "") {
    params.set("q", q.trim());
  }

  return apiRequest<PaginatedResponse<Claim>>(`/claims/?${params.toString()}`);
}

export async function getDocuments(
  q?: string,
  limit: number = 10,
  offset: number = 0
): Promise<PaginatedResponse<Document>> {
  const params = new URLSearchParams();

  params.set("limit", String(limit));
  params.set("offset", String(offset));

  if (q !== undefined && q.trim() !== "") {
    params.set("q", q.trim());
  }

  return apiRequest<PaginatedResponse<Document>>(`/documents/?${params.toString()}`);
}

export async function createClaim(
    claim_text: string,
    source_text: string | null
): Promise<Claim> {
    return apiRequest<Claim>(
        "/claims/",
        {
            method: "POST",
            headers:{
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                claim_text: claim_text,
                source_text: source_text
            }),
        });
}

export async function verifyClaim(
    claim_id: number,
    mode: "rule_based" | "openai"
): Promise<VerificationResult>{
    return apiRequest<VerificationResult>(
        `/claims/${claim_id}/verify`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                mode: mode,
            }),
        });
}

export async function getVerificationResults(): Promise<PaginatedResponse<VerificationResult>>{
    return apiRequest<PaginatedResponse<VerificationResult>>("/verification-results/")
}

export async function uploadPdf(
    file: File
): Promise<Document>{
    const formData = new FormData();
    formData.append("file",file)
    return apiRequest<Document>(
        "/upload/pdf",
        {
            method: "POST",
            body: formData,
        });
}

export async function getClaimEvidence(claim_id: number): Promise<Evidence[]>{
    return apiRequest<Evidence[]>(`/claims/${claim_id}/evidence`)
}