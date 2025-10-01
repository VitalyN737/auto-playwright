from .config import MAX_TASK_CHARS
from .types import Page, TestInfo, StepOptions, AutoPlaywrightConfig
from .complete_task import complete_task
from .errors import UnimplementedError
from .get_snapshot import get_snapshot

def auto(task: str, config: AutoPlaywrightConfig, options: StepOptions = None) -> any:
    """
    The main entry point for auto-playwright.
    """
    if not config or "page" not in config:
        raise ValueError("The auto() function is missing the required `{ 'page': page }` argument.")

    page = config["page"]
    test = config.get("test")

    def run_and_process_task():
        result = run_task(task, page, options)

        if "errorMessage" in result and result["errorMessage"]:
            raise UnimplementedError(result["errorMessage"])

        if "assertion" in result and result["assertion"] is not None:
            return result["assertion"]

        if "query" in result and result["query"] is not None:
            return result["query"]

        return None

    if not test:
        return run_and_process_task()

    # In python, test.step is a context manager and does not return a value from the wrapped block.
    # We will just run the task and let it raise exceptions or complete.
    # The return value handling will be done outside the step if needed.
    # For simplicity, we will just wrap the execution in a step.
    # Note: pytest-playwright does not have test.step, so this is a placeholder for similar functionality if available.
    # If not, it just calls the function.
    if hasattr(test, 'step'):
        with test.step(f"auto-playwright.ai '{task}'"):
            return run_and_process_task()
    else:
        # Fallback for when test object doesn't support steps
        return run_and_process_task()


def run_task(task: str, page: Page, options: StepOptions | None):
    if len(task) > MAX_TASK_CHARS:
        raise ValueError(f"Provided task string is too long, max length is {MAX_TASK_CHARS} chars.")

    if options is None:
        options = {}

    task_message = {
        "task": task,
        "snapshot": get_snapshot(page),
        "options": {
            "model": options.get("model", "gpt-4o"),
            "debug": options.get("debug", False),
            "openai_api_key": options.get("openai_api_key"),
            "openai_base_url": options.get("openai_base_url"),
            "openai_default_query": options.get("openai_default_query"),
            "openai_default_headers": options.get("openai_default_headers"),
        },
    }

    result = complete_task(page, task_message)
    return result