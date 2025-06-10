from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from ._base import BaseData


# Backend DTO
@dataclass
class TestCaseCheckConfig(BaseData):
    identifier: str
    assertions: List[Dict[str, Any]]
    enabled: bool


# SDK DTO
@dataclass
class CheckConfig(BaseData):
    identifier: str
    params: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = True

    def __post_init__(self):
        if self.enabled is None:
            self.enabled = True


def _format_checks_to_cli(
    checks: List[Union[TestCaseCheckConfig, Dict[str, Any]]],
) -> List[CheckConfig]:
    if not checks:
        return []

    checks = [check if isinstance(check, dict) else check.to_dict() for check in checks]

    return [
        CheckConfig.from_dict(
            {
                "identifier": check["identifier"],
                "enabled": check["enabled"],
                **(
                    {"params": params}
                    if check.get("assertions")
                    and (
                        params := {
                            k: v
                            for k, v in check["assertions"][0].items()
                            if k != "type"
                        }
                    )
                    else {}
                ),
            }
        )
        for check in checks
    ]


def _format_checks_to_backend(
    checks: List[Union[CheckConfig, Dict[str, Any]]],
) -> List[TestCaseCheckConfig]:
    if not checks:
        return []

    checks = [check if isinstance(check, dict) else check.to_dict() for check in checks]

    return [
        TestCaseCheckConfig.from_dict(
            {
                **check,
                **(
                    {"assertions": [{"type": check["identifier"], **check["params"]}]}
                    if check.get("params")
                    else {}
                ),
            }
        )
        for check in checks
    ]
