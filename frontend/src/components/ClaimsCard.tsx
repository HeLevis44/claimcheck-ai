import type {Claim} from "@/types/api";

type ClaimsCardProps = {
  claims: Claim[];
  verifyingClaimId: number | null;
  onVerifyClaim: (claimId: number) => void;
};

export function ClaimsCard({claims, verifyingClaimId, onVerifyClaim}: ClaimsCardProps) {
  return (
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
                <p className="break-words text-sm leading-6 text-neutral-800">
                  {claim.claim_text}
                </p>
                <button
                  type="button"
                  onClick={() => onVerifyClaim(claim.id)}
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
  );
}