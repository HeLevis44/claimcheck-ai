type PaginationControlsProps = {
  total: number;
  offset: number;
  itemCount: number;
  hasMore: boolean;
  loading: boolean;
  itemLabel: string;
  onPrevious: () => void;
  onNext: () => void;
};

export function PaginationControls({
  total,
  offset,
  itemCount,
  hasMore,
  loading,
  itemLabel,
  onPrevious,
  onNext,
}: PaginationControlsProps) {
  const start = total === 0 ? 0 : offset + 1;
  const end = Math.min(offset + itemCount, total);

  return (
    <section className="mt-6 flex flex-col gap-3 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm text-neutral-500">
        {total === 0
          ? `No ${itemLabel} found`
          : `Showing ${start}-${end} of ${total} ${itemLabel}`}
      </p>

      <div className="flex gap-2">
        <button
          type="button"
          onClick={onPrevious}
          disabled={loading || offset === 0}
          className="rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Previous
        </button>

        <button
          type="button"
          onClick={onNext}
          disabled={loading || !hasMore}
          className="rounded-full bg-black px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </section>
  );
}