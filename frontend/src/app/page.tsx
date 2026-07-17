"use client";

import {useEffect, useState} from "react";
import {HeaderCard} from "@/components/HeaderCard";
import {ErrorBanner} from "@/components/ErrorBanner";
import {UploadPdfCard} from "@/components/UploadPdfCard";
import {DocumentsCard} from "@/components/DocumentsCard";
import {ClaimsCard} from "@/components/ClaimsCard";
import {CreateClaimCard} from "@/components/CreateClaimCard";
import {VerificationResultCard} from "@/components/VerificationResultCard";
import {EvidenceCard} from "@/components/EvidenceCard";
import {
  getClaims,
  createClaim,
  verifyClaim,
  getClaimEvidence,
  uploadPdf,
  getDocuments,
} from "@/lib/api";
import type {Claim, VerificationResult, Evidence, Document} from "@/types/api";

export default function Home() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [claimText, setClaimText] = useState<string>("");
  const [sourceText, setSourceText] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null);
  const [verifyingClaimId, setVerifyingClaimId] = useState<number | null>(null);
  const [evidences, setEvidences] = useState<Evidence[]>([]);
  const [showAllEvidence, setShowAllEvidence] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadedDocumentName, setUploadedDocumentName] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    async function loadInitialData() {
      try {
        const claimData = await getClaims();
        const documentData = await getDocuments();
        setDocuments(documentData.items);
        setClaims(claimData.items);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to load data");
        }
      } finally {
        setLoading(false);
      }
    }

    loadInitialData();
  }, []);

  async function handleCreateClaim(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (claimText.trim() === "") {
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const new_claim = await createClaim(
        claimText,
        sourceText.trim() === "" ? "" : sourceText
      );

      setClaims([new_claim, ...claims]);
      setClaimText("");
      setSourceText("");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to create claim");
      }
    } finally {
      setSubmitting(false);
    }
  }

  async function handleVerifyClaim(claim_id: number) {
    try {
      setError(null);
      setVerificationResult(null);
      setEvidences([]);
      setShowAllEvidence(false);
      setVerifyingClaimId(claim_id);

      const result = await verifyClaim(claim_id, "rule_based");
      setVerificationResult(result);

      const evidenceData = await getClaimEvidence(claim_id);
      setEvidences(evidenceData);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to verify claim");
      }
    } finally {
      setVerifyingClaimId(null);
    }
  }

  async function handleUploadPdf(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (selectedFile === null) {
      return;
    }

    try {
      setUploading(true);
      setError(null);

      const document = await uploadPdf(selectedFile);
      setUploadedDocumentName(document.filename);
      setDocuments((currentDocuments) => [document, ...currentDocuments]);
      setSelectedFile(null);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to upload file");
      }
    } finally {
      setUploading(false);
    }
  }

  const visibleEvidences = showAllEvidence ? evidences : evidences.slice(0, 3);

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
        <div className="mx-auto max-w-4xl rounded-3xl bg-white/80 p-8 shadow-sm ring-1 ring-black/5">
          <div className="flex items-center gap-3">
            <div className="h-3 w-3 animate-pulse rounded-full bg-neutral-900" />
            <p className="text-sm text-neutral-500">Loading ClaimCheck AI...</p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
      <div className="mx-auto max-w-4xl">
        <HeaderCard />

        <ErrorBanner error={error} />
        
        <CreateClaimCard
          claimText={claimText}
          sourceText={sourceText}
          submitting={submitting}
          onClaimTextChange={setClaimText}
          onSourceTextChange={setSourceText}
          onCreateClaim={handleCreateClaim}
        />

        <UploadPdfCard
          selectedFile={selectedFile}
          uploading={uploading}
          uploadedDocumentName={uploadedDocumentName}
          onFileChange={setSelectedFile}
          onUploadPdf={handleUploadPdf}
        />

        <DocumentsCard documents={documents} />

        <VerificationResultCard
          verifyingClaimId={verifyingClaimId}
          verificationResult={verificationResult}
        />

        <EvidenceCard
          evidences={evidences}
          visibleEvidences={visibleEvidences}
          verifyingClaimId={verifyingClaimId}
          verificationResult={verificationResult}
          showAllEvidence={showAllEvidence}
          onToggleShowAllEvidence={() => setShowAllEvidence(!showAllEvidence)}
        />

        <ClaimsCard
          claims={claims}
          verifyingClaimId={verifyingClaimId}
          onVerifyClaim={handleVerifyClaim}
        />

      </div>
      <style jsx global>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(8px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: translateY(8px) scale(0.98);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
      `}</style>
    </main>
  );
}