"use client";

import {useEffect, useState} from "react";
import {getClaims} from "@/lib/api";
import type {Claim} from "@/types/api";

export default function Home() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadClaims() {
      try {
        const claims = (await getClaims()).items;
      } catch (err) {
        if(err == Error){
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

  if (loading) {
    return <main>Loading...</main>;
  }

  if (error) {
    return <main>{error}</main>;
  }

  return (
    <main>
      <h1>ClaimCheck AI</h1>

      <h2>Claims</h2>

      {claims.length === 0 ? (
        <p>No claims yet.</p>
      ) : (
        <ul>
          {claims.map((claim) => (
            <li key={claim.id}>
              {claim.claim_text}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}