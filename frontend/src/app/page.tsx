"use client";

import {useEffect, useState} from "react";
import {getClaims, createClaim, verifyClaim} from "@/lib/api";
import type {Claim} from "@/types/api";

export default function Home() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [claimText, setClaimText] = useState<string>("");
  const [sourceText, setSourceText] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [verificationMessage, setVerificationMessage] = useState<string | null>(null)

  useEffect(() => {
    async function loadClaims() {
      try {
        const data = await getClaims();
        setClaims(data.items);
      } catch (err) {
        if(err instanceof Error){
          setError(err.message);
        }
        else{
          setError("Failed to load claims")
        }
      } finally {
        setLoading(false)
      }
    }

    loadClaims();
  }, []);

  async function handleCreateClaim(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (claimText.trim() === "") {
      return;
    }
    try {
      setSubmitting(true);
      setError(null);

      const new_claim = await createClaim(
        claimText,
        sourceText.trim() === "" ? "": sourceText
      );

      setClaims([new_claim,...claims]);
      setClaimText("");
      setSourceText("");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to create claim");
      }
    } finally {
      setSubmitting(false);
    }
  }

  async function handleVerifyClaim(claim_id: number) {
  try {
    setError(null);
    setVerificationMessage(null);

    const result = await verifyClaim(claim_id, "rule_based")
    setVerificationMessage(`${result.status}, confidence: ${result.confidence}`)

  } catch (err) {
    if (err instanceof Error) {
      setError(err.message);
    } else {
      setError("Failed to verify claim");
    }
  }
}

  if (loading) {
    return <main>Loading...</main>;
  }

  if (error) {
    return <main>{error}</main>;
  }

  return (
    <main>
      <h1>ClaimCheck AI</h1>
      <form onSubmit={handleCreateClaim}>
        <div>
          <label>Claim</label>
          <textarea
            value={claimText}
            onChange={(event) => setClaimText(event.target.value)}
            placeholder="Enter a claim to verify"
          />
        </div>

        <div>
          <label>Source text</label>
          <textarea
            value={sourceText}
            onChange={(event) => setSourceText(event.target.value)}
            placeholder="Optional source text"
          />
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? "Creating..." : "Create Claim"}
        </button>
      </form>

      <h2>Claims</h2>

      {verificationMessage && (
        <p>{verificationMessage}</p>
      )}


      {claims.length === 0 ? (
        <p>No claims yet.</p>
      ) : (
        <ul>
          {claims.map((claim) => (
            <li key={claim.id}>
              <span>{claim.claim_text}</span>
              <button
                type="button"
                onClick={() => handleVerifyClaim(claim.id)}
                style={{ marginLeft: "8px" }}
              >
                Verify
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}