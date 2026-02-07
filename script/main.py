import json
import sys
from pydantic import ValidationError

from models import Structure, Settings


def fail(payload: dict, exit_code: int = 1):
    print(json.dumps(payload, indent=2))  # stdout
    sys.exit(exit_code)

def success(**data):
    print(json.dumps({"status": "ok", **data}))
    sys.exit(0)



def main():
    try:
        settings = Settings()
    except ValidationError as e:
        e: ValidationError = e
        fail(
            payload={
                "status": "error",
                "type": "settings_validation",
                "errors": e.errors(
                    include_url=False,
                    include_input=False,
                )
            }
        )
        return

    schema = json.loads(settings.json_schema.read_text())

    structure = Structure(
        folder=settings.folder,
        schema=schema
    )

    errors = structure.validate()

    if errors:
        fail(
            payload={
                "status": "error",
                "type": "structure_validation",
                "errors": errors.model_dump().get("errors")
            }
        )

        return

    success(
        payload={
            "folder": str(settings.folder)
        }
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
