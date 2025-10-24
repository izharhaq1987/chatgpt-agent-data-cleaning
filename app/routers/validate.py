import os
import tempfile
import uuid
from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse, FileResponse
from app.services import ingest, profiling, rules, llm_agent, fixes
from app.utils import pii, sampling

router = APIRouter()

@router.post("/validate")
async def validate_endpoint(
    file: UploadFile = File(...),
    apply: bool = Query(False)
):
    job_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as td:
        raw_path = os.path.join(td, file.filename)
        with open(raw_path, "wb") as f:
            f.write(await file.read())

        df = ingest.load_csv(raw_path)
        prof = profiling.profile_df(df)
        base_findings = rules.run_all(df, prof)

        # Sampling + PII mask for LLM
        sample_df = sampling.make_sample(df, prof)
        masked_sample = pii.mask_df(sample_df)
        llm_suggestions = llm_agent.review(prof, masked_sample)

        # Merge findings
        report = rules.merge_reports(base_findings, llm_suggestions)

        download_url = None
        cleaned_path = None
        if apply:
            cleaned = fixes.apply_safe(df, report)
            cleaned_path = os.path.join(td, "cleaned.csv")
            cleaned.to_csv(cleaned_path, index=False)
            # return file directly
            return FileResponse(cleaned_path, filename="cleaned.csv")

        return JSONResponse({
    "version": "0.1.0",
    "job_id": job_id,
    "summary": report.get("summary", {}),
    "findings": report.get("findings", []),
    "suggested_fixes": report.get("suggested_fixes", []),
})

