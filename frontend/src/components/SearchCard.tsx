type SearchCardProps = {
  title: string;
  value: string;
  placeholder: string;
  searching: boolean;
  onValueChange: (value: string) => void;
  onSearch: (event: React.FormEvent<HTMLFormElement>) => void;
  onClear: () => void;
};

export function SearchCard({
  title,
  value,
  placeholder,
  searching,
  onValueChange,
  onSearch,
  onClear,
}: SearchCardProps) {
  return (
    <section className="mb-6 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
      <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
        {title}
      </p>

      <form onSubmit={onSearch} className="mt-4 flex flex-col gap-3 sm:flex-row">
        <input
          type="text"
          value={value}
          onChange={(event) => onValueChange(event.target.value)}
          placeholder={placeholder}
          className="min-h-11 flex-1 rounded-full border border-neutral-200 bg-neutral-50 px-4 text-sm outline-none transition focus:border-neutral-400 focus:bg-white"
        />

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={searching}
            className="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {searching ? "Searching..." : "Search"}
          </button>

          <button
            type="button"
            onClick={onClear}
            disabled={searching}
            className="rounded-full border border-neutral-300 bg-white px-5 py-2.5 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Clear
          </button>
        </div>
      </form>
    </section>
  );
}