export type Document = {
  id: number;
  filename: string;
  file_type: string;
  created_at: string;
};

export type Claim = {
  id: number;
  claim_text: string;
  source_text: string | null;
  created_at: string;
};

export type VerificationStatus =
  | "likely_supported"
  | "weak_evidence"
  | "not_enough_evidence";

export type VerificationResult = {
  id: number;
  claim_id: number;
  evidence_chunk_id: number | null;
  status: VerificationStatus;
  confidence: number;
  reasoning: string | null;
  created_at: string;
};

export type Evidence = {
    chunk_id: number;
    document_id: number;
    page_number: number | null;
    chunk_index: number;
    content: string;
    score: number
};

export type PaginatedResponse<T> = {
  items: T[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
};

