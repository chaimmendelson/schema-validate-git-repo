import json
import os
from pathlib import Path
import yaml
from jsonschema import Draft7Validator

from .errors import InvalidFileError, SchemaErrors

def build_structure_strict(root_path):
    """
    Recursively build JSON-like structure from a directory.
    Only allows folders, .gitkeep, and .yaml/.yml files.
    Raises InvalidFileError on any other file.
    """
    def walk_dir(path):
        result = {}
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            
            if os.path.isdir(full_path):
                result[name] = walk_dir(full_path)
            
            elif os.path.isfile(full_path):
                result[name] = None
                if name.endswith(".yaml"):
                    with open(full_path, "r") as f:
                        result[name] = json.loads(json.dumps(yaml.safe_load(f))) or {}
                        
        return result
    
    return walk_dir(root_path)


class Structure:
    
    def __init__(self, folder: Path, schema: dict):
        self.folder = folder
        self.folder_structure = build_structure_strict(folder)
        self.schema = schema
    
    def validate(self):
        validator = Draft7Validator(self.schema)
        errors = sorted(validator.iter_errors(self.folder_structure), key=lambda e: e.path)
        if errors:
            return SchemaErrors.from_jsonschema_errors(errors)
        return None
    
    
    
    