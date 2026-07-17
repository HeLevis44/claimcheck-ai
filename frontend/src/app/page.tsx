"use client";

import {useEffect, useState} from "react";
import {HeaderCard} from "@/components/HeaderCard";
import {ErrorBanner} from "@/components/ErrorBanner";
import {UploadPdfCard} from "@/components/UploadPdfCard";
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
        
        <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur">
          <form onSubmit={handleCreateClaim} className="space-y-5">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-neutral-700">Claim</label>
              <textarea
                className="min-h-28 resize-none rounded-2xl border border-neutral-200 bg-neutral-50 p-4 text-base outline-none transition focus:border-neutral-400 focus:bg-white"
                value={claimText}
                onChange={(event) => setClaimText(event.target.value)}
                placeholder="Enter a claim to verify"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-neutral-700">Source text</label>
              <textarea
                className="min-h-28 resize-none rounded-2xl border border-neutral-200 bg-neutral-50 p-4 text-base outline-none transition focus:border-neutral-400 focus:bg-white"
                value={sourceText}
                onChange={(event) => setSourceText(event.target.value)}
                placeholder="Optional source text"
              />
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={submitting}
                className="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition duration-200 hover:-translate-y-0.5 hover:bg-neutral-800 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {submitting ? "Creating..." : "Create Claim"}
              </button>
            </div>
          </form>
        </section>

        <UploadPdfCard
          selectedFile={selectedFile}
          uploading={uploading}
          uploadedDocumentName={uploadedDocumentName}
          onFileChange={setSelectedFile}
          onUploadPdf={handleUploadPdf}
        />

        <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight">Uploaded documents</h2>
              <p className="mt-1 text-sm text-neutral-500">{documents.length} total</p>
            </div>
          </div>

          {documents.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-neutral-200 p-8 text-center text-neutral-500">
              No documents uploaded yet.
            </div>
          ) : (
            <ul className="space-y-3">
              {documents.map((document) => (
                <li
                  key={document.id}
                  className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 transition duration-200 hover:-translate-y-0.5 hover:bg-white hover:shadow-sm"
                >
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                    <p className="break-words text-sm font-medium leading-6 text-neutral-800">
                      {document.filename}
                    </p>
                    <span className="w-fit rounded-full border border-neutral-200 bg-white px-3 py-1 text-xs font-medium text-neutral-500">
                      {document.file_type}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="mb-6 min-h-28 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 transition duration-300">
          <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">Latest verification</p>
          {verifyingClaimId !== null ? (
            <div className="mt-3 flex animate-[fadeIn_0.2s_ease-out] items-center gap-3 text-sm text-neutral-500">
              <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-neutral-900" />
              <span>Checking claim...</span>
            </div>
          ) : verificationResult ? (
            <div
              key={verificationResult.id}
              className="mt-3 animate-[fadeInScale_0.35s_ease-out] rounded-2xl bg-neutral-50 p-4"
            >
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <span className="rounded-full bg-black px-3 py-1 text-xs font-medium text-white">
                  {verificationResult.status}
                </span>

                <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-xs font-medium text-neutral-600">
                  confidence {verificationResult.confidence}
                </span>
              </div>

              <p className="text-sm leading-6 text-neutral-700">
                {verificationResult.reasoning || "No reasoning returned."}
              </p>
            </div>
          ) : (
            <p className="mt-3 text-sm text-neutral-400">
              Select a claim and click Verify to see the result.
            </p>
          )}
        </section>

        <section className="mb-6 min-h-28 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 transition duration-300">
          <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">Evidence used</p>
          {verifyingClaimId !== null ? (
            <div className="mt-3 flex animate-[fadeIn_0.2s_ease-out] items-center gap-3 text-sm text-neutral-500">
              <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-neutral-900" />
              <span>Retrieving evidence...</span>
            </div>
          ) : verificationResult ? (
            evidences.length === 0 ? (
              <p className="mt-3 text-sm text-neutral-400">No evidence found for this claim.</p>
            ) : (
              <>
                <ul className="mt-3 space-y-3">
                  {visibleEvidences.map((evidence) => (
                    <li
                      key={evidence.chunk_id}
                      className="animate-[fadeInScale_0.35s_ease-out] rounded-2xl bg-neutral-50 p-4"
                    >
                      <div className="mb-2 flex flex-wrap items-center gap-2">
                        <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-xs font-medium text-neutral-600">
                          score {evidence.score}
                        </span>
                        <span className="rounded-full border border-neutral-200 bg-white px-3 py-1 text-xs font-medium text-neutral-600">
                          page {evidence.page_number ?? "N/A"}
                        </span>
                      </div>
                      <p className="line-clamp-4 text-sm leading-6 text-neutral-700">
                        {evidence.content}
                      </p>
                    </li>
                  ))}
                </ul>

                {evidences.length > 3 && (
                  <button
                    type="button"
                    onClick={() => setShowAllEvidence(!showAllEvidence)}
                    className="mt-4 rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:border-neutral-500 hover:bg-neutral-100"
                  >
                    {showAllEvidence ? "Show less" : `Show all ${evidences.length} evidence chunks`}
                  </button>
                )}
              </>
            )
          ) : (
            <p className="mt-3 text-sm text-neutral-400">
              Evidence will appear here after verification.
            </p>
          )}
        </section>

        <section className="rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight">Claims</h2>
              <p className="mt-1 text-sm text-neutral-500">{claims.length} total</p>
            </div>
          </div>

          {claims.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-neutral-200 p-8 text-center text-neutral-500">
              No claims yet.
            </div>
          ) : (
            <ul className="space-y-3">
              {claims.map((claim) => (
                <li
                  key={claim.id}
                  className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 transition duration-200 hover:-translate-y-0.5 hover:bg-white hover:shadow-sm"
                >
                  <div className="flex items-start justify-between gap-4">
                    <p className="break-words text-sm leading-6 text-neutral-800">{claim.claim_text}</p>
                    <button
                      type="button"
                      onClick={() => handleVerifyClaim(claim.id)}
                      disabled={verifyingClaimId === claim.id}
                      className="shrink-0 rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-medium transition duration-200 hover:-translate-y-0.5 hover:border-neutral-500 hover:bg-neutral-100 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {verifyingClaimId === claim.id ? "Verifying..." : "Verify"}
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
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