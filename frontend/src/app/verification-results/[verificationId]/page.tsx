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

export default function VerificationDetailPage({
  params,
}: VerificationDetailPageProps) {
  const [detail, setDetail] = useState<VerificationDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

  return (
    <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/claims"
          className="mb-4 inline-flex rounded-full border border-neutral-200 bg-white px-4 py-2 text-sm font-medium text-neutral-700 shadow-sm transition hover:bg-neutral-100"
        >
          ← Back to claims
        </Link>

        <section className="mb-8 rounded-3xl bg-white/90 p-8 shadow-sm ring-1 ring-black/5">
          <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            Verification Detail
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight">
            Evidence-grounded result review
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-neutral-600">
            Review the claim, verification result, reasoning, and selected evidence chunk.
          </p>
        </section>

        <ErrorBanner error={error} />

        {detail !== null && (
          <>
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

            <section className="mb-6 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
              <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                Verification Result
              </p>

              <div className="mt-4 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Status
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    {detail.verification.status}
                  </p>
                </div>

                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Confidence
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    {(detail.verification.confidence * 100).toFixed(0)}%
                  </p>
                </div>

                <div className="rounded-2xl bg-neutral-50 p-4">
                  <p className="text-xs uppercase tracking-wide text-neutral-500">
                    Result ID
                  </p>
                  <p className="mt-2 text-sm font-semibold text-neutral-900">
                    #{detail.verification.id}
                  </p>
                </div>
              </div>

              {detail.verification.reasoning !== null &&
                detail.verification.reasoning.trim() !== "" && (
                  <p className="mt-5 rounded-2xl bg-neutral-50 p-4 text-sm leading-6 text-neutral-600">
                    {detail.verification.reasoning}
                  </p>
                )}
            </section>

            <section className="rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
              <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
                Selected Evidence
              </p>

              {detail.evidence === null ? (
                <p className="mt-4 text-sm text-neutral-500">
                  No evidence chunk was selected for this verification result.
                </p>
              ) : (
                <div className="mt-4 rounded-2xl bg-neutral-50 p-5">
                  <div className="mb-4 flex flex-wrap gap-2 text-xs text-neutral-500">
                    <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                      {detail.evidence.filename}
                    </span>
                    <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                      Page {detail.evidence.page_number ?? "N/A"}
                    </span>
                    <span className="rounded-full bg-white px-3 py-1 ring-1 ring-black/5">
                      Chunk {detail.evidence.chunk_index}
                    </span>
                  </div>

                  <p className="text-sm leading-7 text-neutral-700">
                    {detail.evidence.content}
                  </p>
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </main>
  );
}