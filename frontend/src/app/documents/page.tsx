"use client";

import {useEffect, useState} from "react";
import {ErrorBanner} from "@/components/ErrorBanner";
import {UploadPdfCard} from "@/components/UploadPdfCard";
import {DocumentsCard} from "@/components/DocumentsCard";
import {getDocuments, uploadPdf} from "@/lib/api";
import type {Document} from "@/types/api";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadedDocumentName, setUploadedDocumentName] = useState<string | null>(null);

  useEffect(() => {
    async function loadDocuments() {
      try {
        const documentData = await getDocuments();
        setDocuments(documentData.items);
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

        <DocumentsCard documents={documents} />
      </div>
    </main>
  );
}