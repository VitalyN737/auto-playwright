from typing import TypedDict, Optional, Any, Dict, List, Literal
from playwright.sync_api import Page, TestInfo

class StepOptions(TypedDict, total=False):
    model: Optional[str]
    debug: Optional[bool]
    openai_api_key: Optional[str]
    openai_base_url: Optional[str]
    openai_default_query: Optional[Dict[str, Any]]
    openai_default_headers: Optional[Dict[str, Any]]

class TaskMessage(TypedDict):
    task: str
    snapshot: Dict[str, Any]
    options: Optional[StepOptions]

class FunctionResult(TypedDict, total=False):
    query: Optional[str]
    assertion: Optional[bool]
    errorMessage: Optional[str]

class AutoPlaywrightConfig(TypedDict):
    page: Page
    test: Optional[TestInfo]

TaskResult = FunctionResult