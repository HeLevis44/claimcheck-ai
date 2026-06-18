def generate_rule_based_verification(evidences):
    if not evidences:
        status = "not_enough_evidence"
        confidence = 0.2
        reasoning = "No relevant evidence chunks were found."
        evidence_chunk_id = None
    else:
        top_evidence = evidences[0]
        evidence_chunk_id = top_evidence.chunk_id
        if top_evidence.score >= 3:
            status = "likely_supported"
            confidence = 0.8
            reasoning = "The top evidence chunk matched multiple claim keywords."
        else:
            status = "weak_evidence"
            confidence = 0.5
            reasoning = "Only limited keyword overlap was found between the claim and evidence."

    
    return {
        "evidence_chunk_id":evidence_chunk_id,
        "status":status,
        "confidence":confidence,
        "reasoning":reasoning
    }