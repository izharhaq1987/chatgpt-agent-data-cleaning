from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class Finding(BaseModel):
    row_index: int
    column: str
    issue: str
    rule: Optional[str] = None
    suggest_fix: Optional[str] = None

class ValidateResponse(BaseModel):
    job_id: str
    summary: Dict[str, Any]
    findings: List[Finding]
    suggested_fixes: List[Any]
