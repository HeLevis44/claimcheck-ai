export function HeaderCard() {
  return (
    <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur transition duration-300 hover:-translate-y-0.5 hover:shadow-md">
      <p className="mb-3 text-sm font-medium text-neutral-500">
        AI-assisted claim verification
      </p>
      <h1 className="text-5xl font-semibold tracking-tight">ClaimCheck AI</h1>
      <p className="mx-auto mt-4 max-w-2xl text-lg leading-8 text-neutral-600">
        Create a claim, run a quick rule-based verification, and review the result in one clean workspace.
      </p>
    </section>
  );
}