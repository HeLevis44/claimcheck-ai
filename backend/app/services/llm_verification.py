from typing import Protocol
from app.services.verification import generate_rule_based_verification
from app.schemas.verification import VerificationStatus
from app.schemas.llm_verification import (
    LLMVerificationInput,
    LLMVerificationOutput,
)
import json
from openai import OpenAI

class LLMVerificationProvider(Protocol):
    def verify(self, input_data: LLMVerificationInput) -> LLMVerificationOutput:
        ...

class RuleBasedFallbackProvider:
    def verify(self, input_data: LLMVerificationInput) -> LLMVerificationOutput:
        result = generate_rule_based_verification(input_data.evidence_candidates)

        return LLMVerificationOutput(
            status=VerificationStatus(result["status"]),
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            evidence_chunk_id=result["evidence_chunk_id"],
        )

class OpenAIVerificationProvider:
    def __init__(self, client = None, model: str = "gpt-4.1-mini"):
        self.client = client if client is not None else OpenAI()
        self.model = model

    def _build_prompt(self, 
        input_data: LLMVerificationInput
        )-> str:
        evidence_payload = []
        for candidate in input_data.evidence_candidates:
            evidence_payload.append(
            {
            "chunk_id": candidate.chunk_id,
            "filename": candidate.filename,
            "page_number": candidate.page_number,
            "chunk_index": candidate.chunk_index,
            "content": candidate.content,
            }
        )
        evidence_json = json.dumps(evidence_payload)
        prompt = f"""
            You are a claim verification assistant.
            
            Tasks:
            Verify whether the claim below is supported by the provided evidence.
            
            Objectives:
            1. Only use the provided evidence to verify the claim.
            2. Do not use any external information.
            3. Do not make up evidence or information.
            4. if the evidence is insufficient, respond with "not_enough_evidence".
            
            Return Format:
            Only return a JSON object with the following fields, Do not return Markdown, code fences, or any text outside the JSON object.
            - status: exactly one of "likely_supported", "weak_evidence", or "not_enough_evidence". More specifically:
                Use "likely_supported" when the evidence directly supports the claim.
                Use "weak_evidence" when the evidence is relevant but only partially supports the claim.
                Use "not_enough_evidence" when no provided evidence sufficiently supports the claim.
            - confidence: a number between 0 and 1 indicating the confidence level of the verification result.
            - reasoning: a brief evidence-grounded explanation of the conclusion.
            - evidence_chunk_id: must be the chunk_id of one provided evidence candidate, or null when no evidence candidate sufficiently supports the claim.
            
            Claim:
            {input_data.claim_text}
            
            Source context:
            {input_data.source_text}
            
            Evidence candidates:
            {evidence_json}
        """
        return prompt
    
    def verify(self,input_data: LLMVerificationInput,) -> LLMVerificationOutput:
        prompt = self._build_prompt(input_data)

        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=LLMVerificationOutput,
        )

        parsed_output = response.output_parsed
        valid_chunk_ids = {candidate.chunk_id for candidate in input_data.evidence_candidates}
        if (
            parsed_output.evidence_chunk_id is not None
            and parsed_output.evidence_chunk_id not in valid_chunk_ids
        ):
            raise ValueError(
                "Invalid evidence_chunk_id: "
                f"{parsed_output.evidence_chunk_id}. "
                f"Must be one of {valid_chunk_ids} or None."
            )

        return parsed_output