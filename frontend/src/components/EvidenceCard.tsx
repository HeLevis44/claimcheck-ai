import type {Evidence, VerificationResult} from "@/types/api";

type EvidenceCardProps = {
  evidences: Evidence[];
  visibleEvidences: Evidence[];
  verifyingClaimId: number | null;
  verificationResult: VerificationResult | null;
  showAllEvidence: boolean;
  onToggleShowAllEvidence: () => void;
};

export function EvidenceCard({
  evidences,
  visibleEvidences,
  verifyingClaimId,
  verificationResult,
  showAllEvidence,
  onToggleShowAllEvidence,
}: EvidenceCardProps) {
  return (
    <section className="mb-6 min-h-28 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 transition duration-300">
      <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
        Evidence used
      </p>

      {verifyingClaimId !== null ? (
        <div className="mt-3 flex animate-[fadeIn_0.2s_ease-out] items-center gap-3 text-sm text-neutral-500">
          <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-neutral-900" />
          <span>Retrieving evidence...</span>
        </div>
      ) : verificationResult ? (
        evidences.length === 0 ? (
          <p className="mt-3 text-sm text-neutral-400">
            No evidence found for this claim.
          </p>
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
                onClick={onToggleShowAllEvidence}
                className="mt-4 rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:border-neutral-500 hover:bg-neutral-100"
              >
                {showAllEvidence
                  ? "Show less"
                  : `Show all ${evidences.length} evidence chunks`}
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
  );
}