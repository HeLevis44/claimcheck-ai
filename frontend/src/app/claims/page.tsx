"use client";

import {useEffect, useState} from "react";
import {HeaderCard} from "@/components/HeaderCard";
import {ErrorBanner} from "@/components/ErrorBanner";
import {CreateClaimCard} from "@/components/CreateClaimCard";
import {VerificationModeSelector} from "@/components/VerificationModeSelector";
import {VerificationResultCard} from "@/components/VerificationResultCard";
import {EvidenceCard} from "@/components/EvidenceCard";
import {ClaimsCard} from "@/components/ClaimsCard";
import {
  getClaims,
  createClaim,
  verifyClaim,
  getClaimEvidence,
} from "@/lib/api";
import type {Claim, VerificationResult, Evidence} from "@/types/api";

type VerificationMode = "rule_based" | "openai";

export default function ClaimsPage() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [claimText, setClaimText] = useState<string>("");
  const [sourceText, setSourceText] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [verificationMode, setVerificationMode] = useState<VerificationMode>("rule_based");
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null);
  const [verifyingClaimId, setVerifyingClaimId] = useState<number | null>(null);
  const [evidences, setEvidences] = useState<Evidence[]>([]);
  const [showAllEvidence, setShowAllEvidence] = useState<boolean>(false);

  useEffect(() => {
    async function loadClaims() {
      try {
        const claimData = await getClaims();
        setClaims(claimData.items);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to load claims");
        }
      } finally {
        setLoading(false);
      }
    }

    loadClaims();
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

      const result = await verifyClaim(claim_id, verificationMode);
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

  const visibleEvidences = showAllEvidence ? evidences : evidences.slice(0, 3);
  

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
        <div className="mx-auto max-w-4xl rounded-3xl bg-white/80 p-8 shadow-sm ring-1 ring-black/5">
          <div className="flex items-center gap-3">
            <div className="h-3 w-3 animate-pulse rounded-full bg-neutral-900" />
            <p className="text-sm text-neutral-500">Loading claims...</p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
      <div className="mx-auto max-w-4xl">
        <HeaderCard />
        <section className="mb-8 rounded-3xl bg-white/90 p-8 shadow-sm ring-1 ring-black/5">
          <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            Claims
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight">
            Create and verify claims
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-neutral-600">
            Create claims, choose a verification mode, review the verification result, and inspect the evidence chunks used by the system.
          </p>
        </section>

        <ErrorBanner error={error} />

        <CreateClaimCard
          claimText={claimText}
          sourceText={sourceText}
          submitting={submitting}
          onClaimTextChange={setClaimText}
          onSourceTextChange={setSourceText}
          onCreateClaim={handleCreateClaim}
        />

        <VerificationModeSelector
          verificationMode={verificationMode}
          onVerificationModeChange={setVerificationMode}
        />

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
          onToggleShowAllEvidence={() => setShowAllEvidence((current) => !current)}
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
          }
          to {
            opacity: 1;
          }
        }

        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.98) translateY(4px);
          }
          to {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }
      `}</style>
    </main>
  );
}