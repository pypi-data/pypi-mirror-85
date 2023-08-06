from typing import List, Optional

from mat_server.domain import base_types


class ValidationReport(base_types.Entity):
    def __init__(self, failed_reasons: Optional[List[str]] = None):
        self.failed_reasons = failed_reasons if failed_reasons is not None else []

    @property
    def passed(self) -> bool:
        return len(self.failed_reasons) == 0

    def add_failed_reason(self, failed_reason: str):
        self.failed_reasons.append(failed_reason)

    def __eq__(self, other):
        return set(self.failed_reasons) == set(other.failed_reasons)
