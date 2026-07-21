"use client";

import {useEffect, useState} from "react";
import Link from "next/link";
import {ErrorBanner} from "@/components/ErrorBanner";
import {getVerificationDetail} from "@/lib/api";
import type {VerificationDetail} from "@/types/api";

type VerificationDetailPageProps = {
  params: Promise<{
    verificationId: string;
  }>;
};

function getStatusDescription(status: string) {
  if (status === "likely_supported") {
    return "This claim is likely supported by the selected evidence.";
  }

  if (status === "weak_evidence") {
    return "This claim has partial or weak support. The evidence may be related but not strong enough.";
  }

  return "The system did not find enough evidence to support this claim.";
}

function getConfidenceLabel(confidence: number) {
  if (confidence >= 0.75) {
    return "High confidence";
  }

  if (confidence >= 0.45) {
    return "Medium confidence";
  }

  return "Low confidence";
}

function getConfidenceDescription(confidence: number) {
  if (confidence >= 0.75) {
    return "The selected evidence strongly matches the claim.";
  }

  if (confidence >= 0.45) {
    return "The evidence is related, but it may not fully support the claim.";
  }

  return "The system found limited or uncertain evidence for this claim.";
}

function getStatusBadgeClassName(status: string) {
  if (status === "likely_supported") {
    return "bg-emerald-100 text-emerald-800 ring-emerald-200";
  }

  if (status === "weak_evidence") {
    return "bg-amber-100 text-amber-800 ring-amber-200";
  }

  return "bg-rose-100 text-rose-800 ring-rose-200";
}

function getConfidenceColorClassName(confidence: number) {
  if (confidence >= 0.75) {
    return "bg-emerald-500";
  }

  if (confidence >= 0.45) {
    return "bg-amber-500";
  }

  return "bg-rose-500";
}

function countWords(text: string | null) {
  if (text === null || text.trim() === "") {
    return 0;
  }

  return text.trim().split(/\s+/).length;
}

function getBarWidth(value: number, maxValue: number) {
  if (maxValue <= 0) {
    return "0%";
  }

  return `${Math.max(8, Math.round((value / maxValue) * 100))}%`;
}

export default function VerificationDetailPage({
  params,
}: VerificationDetailPageProps) {
  const [detail, setDetail] = useState<VerificationDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showEvidenceText, setShowEvidenceText] = useState<boolean>(true);
  const [copiedLabel, setCopiedLabel] = useState<string | null>(null);

  useEffect(() => {
    async function loadVerificationDetail() {
      try {
        setLoading(true);
        setError(null);

        const resolvedParams = await params;
        const verificationId = Number(resolvedParams.verificationId);

        if (Number.isNaN(verificationId)) {
          setError("Invalid verification result ID");
          return;
        }

        const detailData = await getVerificationDetail(verificationId);
        setDetail(detailData);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to load verification detail");
        }
      } finally {
        setLoading(false);
      }
    }

    loadVerificationDetail();
  }, [params]);

  async function handleCopy(label: string, text: string) {
    await navigator.clipboard.writeText(text);
    setCopiedLabel(label);

    window.setTimeout(() => {
      setCopiedLabel(null);
    }, 1600);
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
        <div className="mx-auto max-w-4xl rounded-3xl bg-white/80 p-8 shadow-sm ring-1 ring-black/5">
          <div className="flex items-center gap-3">
            <div className="h-3 w-3 animate-pulse rounded-full bg-neutral-900" />
            <p className="text-sm text-neutral-500">
              Loading verification detail...
            </p>
          </div>
        </div>
      </main>
    );
  }

  const claimWordCount = detail === null ? 0 : countWords(detail.claim.claim_text);
  const evidenceWordCount =
    detail === null || detail.evidence === null
        ? 0
        : countWords(detail.evidence.content);
  const reasoningWordCount = detail === null ? 0 : countWords(detail.verification.reasoning);
  const maxWordCount = Math.max(claimWordCount, evidenceWordCount, reasoningWordCount, 1);
  const confidencePercent = detail === null ? 0 : Math.round(detail.verification.confidence * 100);

  return (
    <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
      <div className="mx-auto max-w-5xl">
        <Link
          href="/claims"
          className="mb-4 inline-flex rounded-full border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 shadow-sm transition hover:bg-neutral-100"
        >
          ← Back to claims
        </Link>

        <section className="relative mb-8 overflow-hidden rounded-[2rem] bg-neutral-950 p-8 text-white shadow-[0_24px_80px_rgba(0,0,0,0.18)] ring-1 ring-black/5">
          <div className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-blue-500/30 blur-3xl" />
          <div className="pointer-events-none absolute -bottom-24 left-20 h-72 w-72 rounded-full bg-emerald-400/20 blur-3xl" />

          <div className="relative grid gap-8 lg:grid-cols-[1.4fr_0.8fr] lg:items-end">
            <div>
              <p className="text-sm font-medium uppercase tracking-wide text-neutral-300">
                Verification Detail
              </p>
              <h1 className="mt-3 text-4xl font-semibold tracking-tight md:text-5xl">
                Evidence-grounded result review
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-neutral-300">
                Review the claim, confidence signal, reasoning, evidence coverage, and selected source chunk in one verification report.
              </p>
            </div>

            {detail !== null && (
              <div className="rounded-3xl bg-white/10 p-5 backdrop-blur-xl ring-1 ring-white/15">
                <p className="text-xs uppercase tracking-wide text-neutral-300">
                  Confidence score
                </p>
                <p className="mt-2 text-5xl font-semibold tracking-tight">
                  {confidencePercent}%
                </p>
                <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/15">
                  <div
                    className={`h-full rounded-full ${getConfidenceColorClassName(detail.verification.confidence)}`}
                    style={{width: `${confidencePercent}%`}}
                  />
                </div>
                <p className="mt-3 text-sm text-neutral-300">
                  {getConfidenceLabel(detail.verification.confidence)}
                </p>
              </div>
            )}
          </div>
        </section>

        <ErrorBanner error={error} />

        {detail !== null && (
          <>
            <section className="mb-6 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                    Result Summary
                  </p>
                  <div className="mt-3 flex flex-wrap items-center gap-3">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ring-1 ${getStatusBadgeClassName(detail.verification.status)}`}
                    >
                      {detail.verification.status}
                    </span>
                    <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-800 ring-1 ring-blue-200">
                      {getConfidenceLabel(detail.verification.confidence)}
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    handleCopy(
                      "summary",
                      `${detail.verification.status} (${confidencePercent}%): ${getStatusDescription(detail.verification.status)} ${getConfidenceDescription(detail.verification.confidence)}`
                    )
                  }
                  className="rounded-full border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100"
                >
                  {copiedLabel === "summary" ? "Copied" : "Copy summary"}
                </button>
              </div>

              <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_1fr]">
                <div className="rounded-2xl bg-emerald-50 p-5 ring-1 ring-emerald-100">
                  <p className="text-sm font-semibold text-emerald-950">
                    Status interpretation
                  </p>
                  <p className="mt-2 text-sm leading-6 text-emerald-900">
                    {getStatusDescription(detail.verification.status)}
                  </p>
                </div>

                <div className="rounded-2xl bg-blue-50 p-5 ring-1 ring-blue-100">
                  <p className="text-sm font-semibold text-blue-950">
                    Confidence interpretation
                  </p>
                  <p className="mt-2 text-sm leading-6 text-blue-900">
                    {getConfidenceDescription(detail.verification.confidence)}
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-6 grid gap-4 md:grid-cols-4">
              <div className="rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
                <p className="text-xs uppercase tracking-wide text-neutral-500">
                  Claim words
                </p>
                <p className="mt-3 text-3xl font-semibold tracking-tight">
                  {claimWordCount}
                </p>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-neutral-100">
                  <div
                    className="h-full rounded-full bg-blue-500"
                    style={{width: getBarWidth(claimWordCount, maxWordCount)}}
                  />
                </div>
              </div>

              <div className="rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
                <p className="text-xs uppercase tracking-wide text-neutral-500">
                  Evidence words
                </p>
                <p className="mt-3 text-3xl font-semibold tracking-tight">
                  {evidenceWordCount}
                </p>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-neutral-100">
                  <div
                    className="h-full rounded-full bg-emerald-500"
                    style={{width: getBarWidth(evidenceWordCount, maxWordCount)}}
                  />
                </div>
              </div>

              <div className="rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
                <p className="text-xs uppercase tracking-wide text-neutral-500">
                  Reasoning words
                </p>
                <p className="mt-3 text-3xl font-semibold tracking-tight">
                  {reasoningWordCount}
                </p>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-neutral-100">
                  <div
                    className="h-full rounded-full bg-violet-500"
                    style={{width: getBarWidth(reasoningWordCount, maxWordCount)}}
                  />
                </div>
              </div>

              <div className="rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
                <p className="text-xs uppercase tracking-wide text-neutral-500">
                  Evidence located
                </p>
                <p className="mt-3 text-3xl font-semibold tracking-tight">
                  {detail.evidence === null ? "No" : "Yes"}
                </p>
                <p className="mt-3 text-xs leading-5 text-neutral-500">
                  {detail.evidence === null
                    ? "No selected chunk"
                    : `Page ${detail.evidence.page_number ?? "N/A"}, chunk ${detail.evidence.chunk_index}`}
                </p>
              </div>
            </section>

            <section className="mb-6 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
              <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                Claim
              </p>
              <h2 className="mt-3 text-xl font-semibold tracking-tight">
                {detail.claim.claim_text}
              </h2>

              {detail.claim.source_text !== null &&
                detail.claim.source_text.trim() !== "" && (
                  <p className="mt-4 rounded-2xl bg-neutral-50 p-4 text-sm leading-6 text-neutral-600">
                    {detail.claim.source_text}
                  </p>
                )}
            </section>

            <section className="mb-6 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
              <section className="rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
                <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                  Verification Reasoning
                </p>

                {detail.verification.reasoning !== null &&
                detail.verification.reasoning.trim() !== "" ? (
                  <p className="mt-4 rounded-2xl bg-neutral-50 p-4 text-sm leading-6 text-neutral-600">
                    {detail.verification.reasoning}
                  </p>
                ) : (
                  <p className="mt-4 text-sm text-neutral-500">
                    No reasoning was returned for this verification result.
                  </p>
                )}
              </section>

              <section className="rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                      Evidence Review
                    </p>
                    <h2 className="mt-2 text-xl font-semibold tracking-tight">
                      Source chunk inspection
                    </h2>
                  </div>

                  {detail.evidence !== null && (
                    <button
                      type="button"
                      onClick={() => setShowEvidenceText((current) => !current)}
                      className="rounded-full border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100"
                    >
                      {showEvidenceText ? "Hide text" : "Show text"}
                    </button>
                  )}
                </div>

                {detail.evidence === null ? (
                  <p className="mt-4 text-sm text-neutral-500">
                    No evidence chunk was selected for this verification result.
                  </p>
                ) : (
                  <div className="mt-4 rounded-2xl bg-neutral-50 p-5">
                    <div className="mb-4 flex flex-wrap gap-2 text-xs text-neutral-500">
                      <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                        Source: {detail.evidence.filename}
                      </span>
                      <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                        Page {detail.evidence.page_number ?? "N/A"}
                      </span>
                      <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                        Chunk {detail.evidence.chunk_index}
                      </span>
                    </div>

                    <div className="mb-4 rounded-2xl bg-white p-4 text-sm leading-6 text-neutral-600 ring-1 ring-black/5">
                      <p className="font-medium text-neutral-900">
                        Why this evidence matters
                      </p>
                      <p className="mt-2">
                        This evidence was selected as the closest matching source chunk for the claim. Review the text below to decide whether it directly supports, partially supports, or fails to support the claim.
                      </p>
                    </div>

                    {showEvidenceText && (
                      <>
                        <div className="mb-3 flex items-center justify-between gap-3">
                          <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                            Evidence text
                          </p>
                          <button
                            type="button"
                            onClick={() =>
                                handleCopy("evidence", detail.evidence?.content ?? "")
                            }
                            className="rounded-full border border-neutral-200 bg-white px-3 py-1.5 text-xs font-medium text-neutral-700 transition hover:bg-neutral-100"
                            >
                            {copiedLabel === "evidence" ? "Copied" : "Copy evidence"}
                          </button>
                        </div>
                        <p className="text-sm leading-7 text-neutral-700">
                          {detail.evidence.content}
                        </p>
                      </>
                    )}
                  </div>
                )}
              </section>
            </section>

            <section className="rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
              <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                Technical Metadata
              </p>

              <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Result ID
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    #{detail.verification.id}
                  </p>
                </div>

                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Claim ID
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    #{detail.claim.id}
                  </p>
                </div>

                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Evidence chunk
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    {detail.evidence === null ? "N/A" : `#${detail.evidence.id}`}
                  </p>
                </div>

                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Document ID
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    {detail.evidence === null ? "N/A" : `#${detail.evidence.document_id}`}
                  </p>
                </div>
              </div>
            </section>
          </>
        )}
      </div>
    </main>
  );
}