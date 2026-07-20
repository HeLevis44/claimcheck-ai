type VerificationMode = "rule_based" | "openai";

type VerificationModeSelectorProps = {
  verificationMode: VerificationMode;
  onVerificationModeChange: (mode: VerificationMode) => void;
};

export function VerificationModeSelector({
  verificationMode,
  onVerificationModeChange,
}: VerificationModeSelectorProps) {
  return (
    <section className="mb-6 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
      <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
        Verification mode
      </p>

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => onVerificationModeChange("rule_based")}
          className={`rounded-full px-4 py-2 text-sm font-medium transition ${
            verificationMode === "rule_based"
              ? "bg-black text-white"
              : "border border-neutral-300 bg-white text-neutral-700 hover:bg-neutral-100"
          }`}
        >
          Rule-based
        </button>

        <button
          type="button"
          onClick={() => onVerificationModeChange("openai")}
          className={`rounded-full px-4 py-2 text-sm font-medium transition ${
            verificationMode === "openai"
              ? "bg-black text-white"
              : "border border-neutral-300 bg-white text-neutral-700 hover:bg-neutral-100"
          }`}
        >
          OpenAI
        </button>
      </div>

      <p className="mt-3 text-sm leading-6 text-neutral-500">
        Rule-based mode works without an API key. OpenAI mode uses the LLM provider when available and falls back to rule-based verification if needed.
      </p>
    </section>
  );
}