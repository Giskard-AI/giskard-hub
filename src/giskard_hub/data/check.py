from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from ._base import BaseData
from ._entity import Entity


# Backend DTO
@dataclass
class TestCaseCheckConfig(BaseData):
    identifier: str
    assertions: List[Dict[str, Any]]
    enabled: bool


# SDK DTO
@dataclass
class Check(Entity):
    identifier: str
    description: str
    name: str
    params: Dict[str, Any]


@dataclass
class CheckConfig(BaseData):
    identifier: str
    params: Optional[Dict[str, Any]] = None
    enabled: bool = True


def _format_checks_to_backend(
    checks: List[Union[CheckConfig, Dict[str, Any]]],
) -> List[TestCaseCheckConfig]:
    if not checks:
        return []

    checks = [check if isinstance(check, dict) else check.to_dict() for check in checks]

    return [
        TestCaseCheckConfig.from_dict(
            {
                "enabled": True,  # Default value for enabled
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


def extract_check_params(
    check: Dict[str, Any], without_type: bool = False
) -> Dict[str, Any]:
    check_params = (
        {k: v for k, v in check["assertions"][0].items()}
        if check.get("assertions")
        else {}
    )

    if without_type and ("type" in check_params):
        check_params.pop("type")

    return check_params


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
                "params": extract_check_params(check, without_type=True),
            }
        )
        for check in checks
    ]
