import type {FormEvent} from "react";

type UploadPdfCardProps = {
  selectedFile: File | null;
  uploading: boolean;
  uploadedDocumentName: string | null;
  onFileChange: (file: File | null) => void;
  onUploadPdf: (event: FormEvent<HTMLFormElement>) => void;
};

export function UploadPdfCard({
  selectedFile,
  uploading,
  uploadedDocumentName,
  onFileChange,
  onUploadPdf,
}: UploadPdfCardProps) {
  return (
        <section className="mb-8 rounded-3xl bg-white/90 p-6 shadow-sm ring-1 ring-black/5 backdrop-blur">
          <p className="mb-3 text-sm font-medium text-neutral-500">Upload PDF</p>
          <form onSubmit={onUploadPdf} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => {
                const file = event.target.files?.[0] ?? null;
                onFileChange(file);
              }}
              className="text-sm text-neutral-600 file:mr-4 file:rounded-full file:border-0 file:bg-neutral-100 file:px-4 file:py-2 file:text-sm file:font-medium file:text-neutral-700 hover:file:bg-neutral-200"
            />

            <button
              type="submit"
              disabled={uploading || selectedFile === null}
              className="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition duration-200 hover:-translate-y-0.5 hover:bg-neutral-800 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {uploading ? "Uploading..." : "Upload PDF"}
            </button>
          </form>

          {uploadedDocumentName && (
            <p className="mt-4 text-sm text-neutral-500">
              Uploaded: {uploadedDocumentName}
            </p>
          )}
        </section>
  );
}