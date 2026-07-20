"use client";

import {useEffect, useState} from "react";
import {ErrorBanner} from "@/components/ErrorBanner";
import {UploadPdfCard} from "@/components/UploadPdfCard";
import {DocumentsCard} from "@/components/DocumentsCard";
import {getDocuments, uploadPdf} from "@/lib/api";
import type {Document} from "@/types/api";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [documentTotal, setDocumentTotal] = useState<number>(0);
  const [documentLimit] = useState<number>(10);
  const [documentOffset, setDocumentOffset] = useState<number>(0);
  const [documentHasMore, setDocumentHasMore] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadedDocumentName, setUploadedDocumentName] = useState<string | null>(null);
  const [documentSearch, setDocumentSearch] = useState<string>("");
  const [searchingDocuments, setSearchingDocuments] = useState<boolean>(false);

  useEffect(() => {
    async function loadDocuments() {
      try {
        const documentData = await getDocuments(undefined, documentLimit, 0);
        setDocuments(documentData.items);
        setDocumentTotal(documentData.total);
        setDocumentOffset(documentData.offset);
        setDocumentHasMore(documentData.has_more);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to load documents");
        }
      } finally {
        setLoading(false);
      }
    }

    loadDocuments();
  }, []);

  async function handleUploadPdf(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (selectedFile === null) {
      return;
    }

    try {
      setUploading(true);
      setError(null);

      const document = await uploadPdf(selectedFile);
      setUploadedDocumentName(document.filename);
      setDocuments((currentDocuments) => [document, ...currentDocuments]);
      setDocumentTotal((currentTotal) => currentTotal + 1);
      setSelectedFile(null);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to upload file");
      }
    } finally {
      setUploading(false);
    }
  }

  async function handleSearchDocuments(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      setSearchingDocuments(true);
      setError(null);

      const documentData = await getDocuments(documentSearch, documentLimit, 0);
      setDocuments(documentData.items);
      setDocumentTotal(documentData.total);
      setDocumentOffset(documentData.offset);
      setDocumentHasMore(documentData.has_more);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to search documents");
      }
    } finally {
      setSearchingDocuments(false);
    }
  }

  async function handleClearDocumentSearch() {
    try {
      setSearchingDocuments(true);
      setError(null);
      setDocumentSearch("");

      const documentData = await getDocuments(undefined, documentLimit, 0);
      setDocuments(documentData.items);
      setDocumentTotal(documentData.total);
      setDocumentOffset(documentData.offset);
      setDocumentHasMore(documentData.has_more);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load documents");
      }
    } finally {
      setSearchingDocuments(false);
    }
  }

  async function handleChangeDocumentPage(nextOffset: number) {
    try {
      setSearchingDocuments(true);
      setError(null);

      const documentData = await getDocuments(documentSearch, documentLimit, nextOffset);
      setDocuments(documentData.items);
      setDocumentTotal(documentData.total);
      setDocumentOffset(documentData.offset);
      setDocumentHasMore(documentData.has_more);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load documents");
      }
    } finally {
      setSearchingDocuments(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
        <div className="mx-auto max-w-4xl rounded-3xl bg-white/80 p-8 shadow-sm ring-1 ring-black/5">
          <div className="flex items-center gap-3">
            <div className="h-3 w-3 animate-pulse rounded-full bg-neutral-900" />
            <p className="text-sm text-neutral-500">Loading documents...</p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f5f5f7] px-6 py-12 text-[#1d1d1f]">
      <div className="mx-auto max-w-4xl">
        <section className="mb-8 rounded-3xl bg-white/90 p-8 shadow-sm ring-1 ring-black/5">
          <p className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            Documents
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight">
            Upload and manage source PDFs
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-neutral-600">
            Uploaded PDFs are parsed into text chunks and used as source evidence for claim verification.
          </p>
        </section>

        <ErrorBanner error={error} />

        <UploadPdfCard
          selectedFile={selectedFile}
          uploading={uploading}
          uploadedDocumentName={uploadedDocumentName}
          onFileChange={setSelectedFile}
          onUploadPdf={handleUploadPdf}
        />

        <section className="mb-6 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5">
          <p className="text-xs font-medium uppercase tracking-wide text-neutral-500">
            Search documents
          </p>
          <form onSubmit={handleSearchDocuments} className="mt-4 flex flex-col gap-3 sm:flex-row">
            <input
              type="text"
              value={documentSearch}
              onChange={(event) => setDocumentSearch(event.target.value)}
              placeholder="Search uploaded documents"
              className="min-h-11 flex-1 rounded-full border border-neutral-200 bg-neutral-50 px-4 text-sm outline-none transition focus:border-neutral-400 focus:bg-white"
            />
            <div className="flex gap-2">
              <button
                type="submit"
                disabled={searchingDocuments}
                className="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {searchingDocuments ? "Searching..." : "Search"}
              </button>
              <button
                type="button"
                onClick={handleClearDocumentSearch}
                disabled={searchingDocuments}
                className="rounded-full border border-neutral-300 bg-white px-5 py-2.5 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Clear
              </button>
            </div>
          </form>
        </section>

        <DocumentsCard documents={documents} />

        <section className="mt-6 flex flex-col gap-3 rounded-3xl bg-white/90 p-5 shadow-sm ring-1 ring-black/5 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-neutral-500">
            {documentTotal === 0
              ? "No documents found"
              : `Showing ${documentOffset + 1}-${Math.min(documentOffset + documents.length, documentTotal)} of ${documentTotal} documents`}
          </p>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => handleChangeDocumentPage(Math.max(documentOffset - documentLimit, 0))}
              disabled={searchingDocuments || documentOffset === 0}
              className="rounded-full border border-neutral-300 bg-white px-4 py-2 text-sm font-medium text-neutral-700 transition hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Previous
            </button>

            <button
              type="button"
              onClick={() => handleChangeDocumentPage(documentOffset + documentLimit)}
              disabled={searchingDocuments || !documentHasMore}
              className="rounded-full bg-black px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}