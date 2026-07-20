import Link from "next/link";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#f5f5f7] px-6 py-10 text-[#1d1d1f]">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(255,255,255,0.95),transparent_28%),radial-gradient(circle_at_80%_18%,rgba(191,219,254,0.55),transparent_30%),radial-gradient(circle_at_50%_95%,rgba(229,231,235,0.9),transparent_34%)]" />
      <div className="pointer-events-none absolute left-1/2 top-24 h-[34rem] w-[34rem] -translate-x-1/2 rounded-full border border-white/70 bg-white/30 shadow-[0_0_120px_rgba(255,255,255,0.95)] blur-2xl" />

      <div className="relative mx-auto max-w-6xl">
        <nav className="mb-8 flex items-center justify-between rounded-full border border-white/80 bg-white/70 px-5 py-3 shadow-sm shadow-neutral-200/70 backdrop-blur-xl ring-1 ring-black/5">
          <Link href="/" className="flex items-center gap-3">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-2xl bg-[#1d1d1f] text-sm font-semibold text-white shadow-lg shadow-neutral-300/80">
              <span className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/20 to-transparent" />
              CC
            </div>
            <div>
              <p className="text-sm font-semibold tracking-tight">ClaimCheck AI</p>
              <p className="text-xs text-neutral-500">Source-grounded verification</p>
            </div>
          </Link>

          <div className="hidden items-center gap-1 rounded-full bg-neutral-100 p-1 text-sm text-neutral-600 sm:flex">
            <Link href="/documents" className="rounded-full px-4 py-2 transition hover:bg-white hover:text-neutral-950 hover:shadow-sm">
              Documents
            </Link>
            <Link href="/claims" className="rounded-full px-4 py-2 transition hover:bg-white hover:text-neutral-950 hover:shadow-sm">
              Claims
            </Link>
          </div>
        </nav>

        <section className="relative mb-6 overflow-hidden rounded-[2.25rem] border border-white/80 bg-white/75 p-8 shadow-[0_24px_80px_rgba(0,0,0,0.08)] backdrop-blur-xl md:p-10 lg:p-12">
          <div className="pointer-events-none absolute -right-28 -top-28 h-80 w-80 rounded-full bg-blue-100/80 blur-3xl" />
          <div className="pointer-events-none absolute -bottom-32 left-1/3 h-80 w-80 rounded-full bg-white blur-3xl" />

          <div className="relative grid gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
            <div>
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white/80 px-4 py-2 text-sm font-medium text-neutral-600 shadow-sm">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                  <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
                </span>
                Full-stack AI verification system
              </div>

              <h1 className="max-w-3xl text-5xl font-semibold tracking-[-0.04em] text-[#1d1d1f] md:text-7xl">
                Evidence-first claim verification.
              </h1>

              <p className="mt-6 max-w-2xl text-lg leading-8 text-neutral-600 md:text-xl">
                Upload PDFs, extract source chunks, create claims, and verify support with transparent reasoning from a rule-based or OpenAI-assisted workflow.
              </p>

              <div className="mt-8 flex flex-wrap gap-3">
                <Link
                  href="/claims"
                  className="rounded-full bg-[#1d1d1f] px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-neutral-300/80 transition hover:-translate-y-0.5 hover:bg-black hover:shadow-xl"
                >
                  Start verifying →
                </Link>
                <Link
                  href="/documents"
                  className="rounded-full border border-neutral-200 bg-white px-6 py-3 text-sm font-semibold text-neutral-800 shadow-sm transition hover:-translate-y-0.5 hover:border-neutral-300 hover:bg-neutral-50 hover:shadow-md"
                >
                  Upload sources
                </Link>
              </div>

              <div className="mt-10 grid max-w-xl grid-cols-3 gap-3">
                <div className="rounded-2xl bg-neutral-50/90 p-4 ring-1 ring-black/5">
                  <p className="text-2xl font-semibold tracking-tight">PDF</p>
                  <p className="mt-1 text-xs text-neutral-500">source ingestion</p>
                </div>
                <div className="rounded-2xl bg-neutral-50/90 p-4 ring-1 ring-black/5">
                  <p className="text-2xl font-semibold tracking-tight">AI</p>
                  <p className="mt-1 text-xs text-neutral-500">verification mode</p>
                </div>
                <div className="rounded-2xl bg-neutral-50/90 p-4 ring-1 ring-black/5">
                  <p className="text-2xl font-semibold tracking-tight">SQL</p>
                  <p className="mt-1 text-xs text-neutral-500">stored results</p>
                </div>
              </div>
            </div>

            <div className="relative min-h-[30rem]">
              <div className="absolute left-8 top-8 h-72 w-72 rounded-full bg-gradient-to-br from-blue-100 to-white blur-2xl" />

              <div className="absolute right-0 top-0 w-[88%] rounded-[2rem] border border-white bg-white/75 p-5 shadow-[0_30px_90px_rgba(0,0,0,0.12)] ring-1 ring-black/5 backdrop-blur-xl">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-medium uppercase tracking-[0.22em] text-neutral-400">
                      Claim analysis
                    </p>
                    <p className="mt-1 text-sm font-medium text-neutral-800">
                      Source-grounded result
                    </p>
                  </div>
                  <div className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 ring-1 ring-emerald-100">
                    Live
                  </div>
                </div>

                <div className="rounded-2xl bg-[#1d1d1f] p-4 text-white shadow-lg shadow-neutral-300/70">
                  <div className="mb-3 flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-white px-3 py-1 text-xs font-medium text-black">
                      likely_supported
                    </span>
                    <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-white/75">
                      confidence 0.8
                    </span>
                  </div>
                  <p className="text-sm leading-6 text-white/70">
                    The selected evidence directly supports the claim.
                  </p>
                </div>

                <div className="mt-4 grid gap-3">
                  <div className="rounded-2xl bg-neutral-50 p-4 ring-1 ring-black/5">
                    <div className="mb-2 flex items-center justify-between">
                      <p className="text-sm font-medium text-neutral-800">Evidence chunk</p>
                      <span className="rounded-full bg-white px-2.5 py-1 text-xs text-neutral-500 ring-1 ring-black/5">score 4</span>
                    </div>
                    <div className="space-y-2">
                      <div className="h-2 w-full rounded-full bg-neutral-200" />
                      <div className="h-2 w-5/6 rounded-full bg-neutral-200" />
                      <div className="h-2 w-2/3 rounded-full bg-neutral-200" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="absolute bottom-8 left-0 w-[58%] rounded-[1.5rem] border border-white bg-white/70 p-4 shadow-xl shadow-neutral-200/70 ring-1 ring-black/5 backdrop-blur-xl">
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-neutral-400">Pipeline</p>
                <div className="mt-4 space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-neutral-900 text-xs font-semibold text-white">1</div>
                    <p className="text-sm text-neutral-700">PDF parsed</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-neutral-200 text-xs font-semibold text-neutral-700">2</div>
                    <p className="text-sm text-neutral-700">Evidence ranked</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-neutral-200 text-xs font-semibold text-neutral-700">3</div>
                    <p className="text-sm text-neutral-700">Result stored</p>
                  </div>
                </div>
              </div>

              <div className="absolute bottom-0 right-10 rounded-2xl border border-white bg-white/80 px-4 py-3 text-sm font-medium text-neutral-700 shadow-xl shadow-neutral-200/80 ring-1 ring-black/5 backdrop-blur-xl">
                FastAPI · PostgreSQL · Next.js
              </div>
            </div>
          </div>
        </section>

        <div className="grid gap-5 md:grid-cols-2">
          <Link
            href="/documents"
            className="group relative overflow-hidden rounded-[1.75rem] bg-white/85 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur-xl transition duration-200 hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(0,0,0,0.08)]"
          >
            <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-blue-100 blur-2xl transition group-hover:bg-blue-200" />
            <div className="relative">
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-neutral-100 text-xl ring-1 ring-black/5">
                ⬡
              </div>
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-neutral-400">
                Documents
              </p>
              <h2 className="mt-3 text-2xl font-semibold tracking-tight text-[#1d1d1f]">
                Upload source PDFs
              </h2>
              <p className="mt-3 text-sm leading-6 text-neutral-600">
                Add documents that will be parsed into chunks and used as evidence for claim verification.
              </p>
              <p className="mt-5 text-sm font-medium text-neutral-900 transition group-hover:translate-x-1">
                Go to Documents →
              </p>
            </div>
          </Link>

          <Link
            href="/claims"
            className="group relative overflow-hidden rounded-[1.75rem] bg-white/85 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur-xl transition duration-200 hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(0,0,0,0.08)]"
          >
            <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-neutral-200 blur-2xl transition group-hover:bg-neutral-300" />
            <div className="relative">
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-neutral-100 text-xl ring-1 ring-black/5">
                ✓
              </div>
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-neutral-400">
                Claims
              </p>
              <h2 className="mt-3 text-2xl font-semibold tracking-tight text-[#1d1d1f]">
                Create and verify claims
              </h2>
              <p className="mt-3 text-sm leading-6 text-neutral-600">
                Create claims, select a verification mode, review results, and inspect supporting evidence chunks.
              </p>
              <p className="mt-5 text-sm font-medium text-neutral-900 transition group-hover:translate-x-1">
                Go to Claims →
              </p>
            </div>
          </Link>
        </div>
      </div>
    </main>
  );
}