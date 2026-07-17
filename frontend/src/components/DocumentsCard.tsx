import type {Document} from "@/types/api";

type DocumentsCardProps = {
  documents: Document[];
};

export function DocumentsCard({documents}: DocumentsCardProps) {
  return (
    <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5">
      <div className="mb-5 flex items-end justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold tracking-tight">Uploaded documents</h2>
          <p className="mt-1 text-sm text-neutral-500">{documents.length} total</p>
        </div>
      </div>

      {documents.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-neutral-200 p-8 text-center text-neutral-500">
          No documents uploaded yet.
        </div>
      ) : (
        <ul className="space-y-3">
          {documents.map((document) => (
            <li
              key={document.id}
              className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 transition duration-200 hover:-translate-y-0.5 hover:bg-white hover:shadow-sm"
            >
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <p className="break-words text-sm font-medium leading-6 text-neutral-800">
                  {document.filename}
                </p>
                <span className="w-fit rounded-full border border-neutral-200 bg-white px-3 py-1 text-xs font-medium text-neutral-500">
                  {document.file_type}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}