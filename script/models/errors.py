from pydantic import BaseModel


class SchemaError(BaseModel):
    location: str
    message: str
    validator: str | None = None
    expected: str | None = None
    
    @classmethod
    def from_jsonschema_errors(cls, errors) -> list["SchemaError"]:
        error_list = []
        for error in errors:
            location = " -> ".join([str(p) for p in error.absolute_path])
            error_record = cls(
                location=location or 'root',
                message=error.message,
                validator=error.validator,
                expected=str(error.validator_value) if error.validator_value else None
            )
            error_list.append(error_record)
        return error_list
    
    def printable(self) -> str:
        parts = [f"Location: {self.location}", f"Message: {self.message}"]
        if self.validator:
            parts.append(f"Validator: {self.validator}")
        if self.expected:
            parts.append(f"Expected: {self.expected}")
        return "\n".join(parts)

class SchemaErrors(BaseModel):
    errors: list[SchemaError]
    
    @classmethod
    def from_jsonschema_errors(cls, errors) -> "SchemaErrors":
        error_list = SchemaError.from_jsonschema_errors(errors)
        return cls(errors=error_list)
    
class InvalidFileError(Exception):
    pass