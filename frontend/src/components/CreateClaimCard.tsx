import type {FormEvent} from "react";

type CreateClaimCardProps = {
  claimText: string;
  sourceText: string;
  submitting: boolean;
  onClaimTextChange: (value: string) => void;
  onSourceTextChange: (value: string) => void;
  onCreateClaim: (event: FormEvent<HTMLFormElement>) => void;
};

export function CreateClaimCard({
  claimText,
  sourceText,
  submitting,
  onClaimTextChange,
  onSourceTextChange,
  onCreateClaim,
}: CreateClaimCardProps) {
  return (
    <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur">
      <form onSubmit={onCreateClaim} className="space-y-5">
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium text-neutral-700">Claim</label>
          <textarea
            className="min-h-28 resize-none rounded-2xl border border-neutral-200 bg-neutral-50 p-4 text-base outline-none transition focus:border-neutral-400 focus:bg-white"
            value={claimText}
            onChange={(event) => onClaimTextChange(event.target.value)}
            placeholder="Enter a claim to verify"
          />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium text-neutral-700">Source text</label>
          <textarea
            className="min-h-28 resize-none rounded-2xl border border-neutral-200 bg-neutral-50 p-4 text-base outline-none transition focus:border-neutral-400 focus:bg-white"
            value={sourceText}
            onChange={(event) => onSourceTextChange(event.target.value)}
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
  );
} 