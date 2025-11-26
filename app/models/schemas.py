from pydantic import BaseModel
from typing import List, Any

class IngestResponse(BaseModel):
    message: str

class TestCase(BaseModel):
    test_id: str
    feature: str
    scenario: str
    expected: str
    grounded_in: List[str]

class GenerateScriptRequest(BaseModel):
    test_case: Any
    checkout_html_path: str
