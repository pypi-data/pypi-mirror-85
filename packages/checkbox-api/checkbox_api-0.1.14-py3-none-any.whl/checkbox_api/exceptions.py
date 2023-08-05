from typing import Any, Dict


class CheckBoxError(Exception):
    pass


class CheckBoxNetworkError(CheckBoxError):
    pass


class CheckBoxAPIError(CheckBoxError):
    def __init__(self, status: int, content: Dict[str, Any]):
        self.status = status
        self.content = content
        self.message = content.get("message", content)

    def __str__(self):
        return f"{self.message} [status={self.status}]"


class CheckBoxAPIValidationError(CheckBoxAPIError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = self.content.get("detail", [])

    def __str__(self):
        validations = []
        for item in self.detail:
            location = " -> ".join(map(str, item["loc"]))
            error_type = item["type"]
            description = item["msg"]
            validations.append(f"{location}:\n    {description} (type={error_type})")
        validations_str = "\n".join(validations)
        return f"{self.message} [status={self.status}]\n{validations_str}"


class StatusException(CheckBoxError):
    pass
