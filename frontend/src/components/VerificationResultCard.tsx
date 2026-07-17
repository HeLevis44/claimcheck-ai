import type {VerificationResult} from "@/types/api";

type VerificationResultCardProps = {
  verifyingClaimId: number | null;
  verificationResult: VerificationResult | null;
};

export function VerificationResultCard({
  verifyingClaimId,
  verificationResult,
}: VerificationResultCardProps) {
  return (
    <section className="mb-6 min-h-28 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 transition duration-300">
      <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
        Latest verification
      </p>

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
  );
}