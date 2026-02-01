import json
from pathlib import Path

from models import Structure

def main(folder_path: str, schema_path: str):
    # Load schema
    with open(schema_path) as f:
        schema = json.load(f)
    
    # Create Structure instance
    structure = Structure(folder=Path(folder_path), schema=schema)
    
    # Validate structure
    errors = structure.validate()
    
    if not errors:
        print("✅ Valid structure")
    else:
        print("❌ Invalid structure:")
        print(errors.model_dump_json(indent=2))
        
if __name__ == "__main__":
    main("..", "../schemas/structure_schema.json")