# Schema Validate Git Repo
A Python utility that validates directory structures and YAML files against JSON schemas. This tool ensures that your repository follows a predefined structure and content schema.
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Environment Variables](#environment-variables)
  - [Configuration File](#configuration-file)
- [Project Structure](#project-structure)
- [Schema Definition](#schema-definition)
- [Examples](#examples)
  - [Basic Usage](#basic-usage)
  - [With Environment Variables](#with-environment-variables)
  - [With Configuration File](#with-configuration-file)
- [Output](#output)
  - [Success Response](#success-response)
  - [Error Response](#error-response)
- [Supported File Types](#supported-file-types)
- [Limitations](#limitations)
- [Contributing](#contributing)
## Overview
This project provides a schema validation tool for repository structures. It scans a directory tree, extracts YAML files, and validates the resulting structure against a JSON schema using JSON Schema Draft 7 standard.
**Use Cases:**
- Validate repository configurations match expected structure
- Ensure YAML configuration files comply with defined schemas
- CI/CD pipeline validation
- Infrastructure-as-code (IaC) structure validation
## Features
✅ **Directory Structure Validation** - Validates directory hierarchies against JSON schemas  
✅ **YAML File Support** - Automatically loads and validates YAML files  
✅ **JSON Schema Draft 7** - Full JSON Schema Draft 7 support for complex validation rules  
✅ **Detailed Error Reporting** - Rich error messages with validation failure locations  
✅ **CLI Integration** - Simple command-line interface with optional flags  
✅ **Environment Variables** - Configuration via environment variables or `.env` file  
✅ **Pydantic Settings** - Type-safe configuration management  
✅ **Exit Codes** - Proper exit codes for integration with scripts
## Installation
### Prerequisites
- Python 3.7+
- pip (Python package manager)
### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd schema-validate-git-repo
```
2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Verify installation:
```bash
cd script
python3 main.py --help
```
## Usage
### Command Line Interface
The primary way to use this tool is through the CLI:
```bash
python3 script/main.py --folder <path-to-folder> --json-schema <path-to-schema> [--raise-error]
```
#### Required Arguments
- `--folder`: Path to the directory to validate
- `--json-schema`: Path to the JSON schema file
#### Optional Arguments
- `--raise-error`: Raise an exception on validation failure instead of returning structured error
### Environment Variables
You can configure the tool using environment variables:
```bash
export FOLDER=/path/to/folder
export JSON_SCHEMA=/path/to/schema.json
export RAISE_ERROR=false
python3 script/main.py
```
### Configuration File
Create a `.env` file in the script directory:
```env
FOLDER=/path/to/folder
JSON_SCHEMA=/path/to/schema.json
RAISE_ERROR=false
```
Then run:
```bash
cd script
python3 main.py
```
## Project Structure
```
schema-validate-git-repo/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── LICENSE                        # License information
├── example/                       # Example schemas and folder structures
└── script/                        # Main application code
    ├── main.py                   # Entry point
    ├── models/                   # Data models
    │   ├── __init__.py
    │   ├── errors.py             # Error classes
    │   ├── settings.py           # Configuration settings
    │   └── structure.py          # Structure validation logic
```
## Schema Definition
Schemas are defined using JSON Schema Draft 7 format. Here's a basic example:
```json
{
  "type": "object",
  "properties": {
    "folder_name": {
      "type": "object",
      "properties": {
        "file.yaml": {
          "type": "object",
          "properties": {
            "key": {
              "type": "string"
            }
          },
          "required": ["key"]
        }
      }
    }
  }
}
```
### Key Schema Concepts
- **type**: Specifies the data type (object, array, string, integer, etc.)
- **properties**: Defines allowed properties and their schemas
- **required**: Lists required properties
- **additionalProperties**: Controls whether extra properties are allowed
- **patternProperties**: Allows properties matching a regex pattern
- **enum**: Restricts values to a specific set
- **$ref**: References other schema definitions for reusability
- **minLength/maxLength**: String length constraints
- **minimum/maximum**: Number constraints
- **minItems/maxItems**: Array length constraints
## Examples
### Basic Usage
Validate a folder structure:
```bash
cd script
python3 main.py \
  --folder ../example/consumers/application \
  --json-schema ../example/schemas/structure_schema.json
```
### With Environment Variables
```bash
export FOLDER="../example/consumers/application"
export JSON_SCHEMA="../example/schemas/structure_schema.json"
python3 script/main.py
```
### With Configuration File
Create `script/.env`:
```env
FOLDER=../example/consumers/application
JSON_SCHEMA=../example/schemas/structure_schema.json
RAISE_ERROR=false
```
Run:
```bash
cd script
python3 main.py
```
### Creating a Custom Schema
Create `schemas/my_schema.json`:
```json
{
  "type": "object",
  "definitions": {
    "Application": {
      "type": "object",
      "patternProperties": {
        "^[a-z]+$": {
          "type": "object",
          "properties": {
            "config.yaml": {
              "type": "object"
            }
          }
        }
      }
    }
  },
  "$ref": "#/definitions/Application"
}
```
Then validate:
```bash
python3 script/main.py \
  --folder ../consumers \
  --json-schema ../schemas/my_schema.json
```
## Output
### Success Response
When validation passes, the tool outputs JSON:
```json
{
  "status": "ok",
  "payload": {
    "folder": "/path/to/folder"
  }
}
```
Exit code: **0**
### Error Response
When validation fails:
```json
{
  "status": "error",
  "type": "structure_validation",
  "errors": [
    {
      "location": "organization -> meta.yaml",
      "message": "'tyks' is a required property",
      "validator": "required",
      "expected": "['tyks']"
    }
  ]
}
```
Exit code: **1**
### Settings Validation Error
When configuration is invalid:
```json
{
  "status": "error",
  "type": "settings_validation",
  "errors": [
    {
      "type": "missing",
      "loc": ["folder"],
      "msg": "Field required"
    }
  ]
}
```
Exit code: **1**
## Supported File Types
### Supported
✅ **YAML Files** (`.yaml`, `.yml`)
- Automatically loaded and converted to JSON structures
✅ **Directories**
- Recursively scanned and represented as objects
✅ **Special Files**
- `.gitkeep` (null values)
### Not Currently Supported
❌ JSON files (`.json`)
❌ YAML Aliases and Anchors (may not resolve correctly)
❌ Non-UTF-8 encoded files
## Limitations
1. **File Types**: Currently only YAML files are loaded. JSON files and other formats are ignored.
2. **YAML Features**: Some advanced YAML features like complex anchors and tags may not work as expected.
3. **Performance**: Large directory trees with thousands of files may take longer to process.
4. **Schema Complexity**: While JSON Schema Draft 7 is fully supported, very deeply nested schemas (100+ levels) may hit recursion limits.
5. **Symlinks**: Symbolic links are not specially handled and may cause loops.
## Contributing
To contribute to this project:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest script/tests/ -v`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a Pull Request
### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt pytest pytest-cov
# Run tests with coverage
pytest script/tests/ --cov=script/models
```
## Troubleshooting
### Missing Configuration Error
**Error**: `Field required` for folder or json-schema
**Solution**: Ensure both `--folder` and `--json-schema` arguments are provided:
```bash
python3 script/main.py --folder /path/to/folder --json-schema /path/to/schema.json
```
### File Not Found Error
**Error**: `FileNotFoundError` for schema file
**Solution**: Verify the schema file path is correct:
```bash
ls -la /path/to/schema.json
```
### Validation Failures
**Error**: Structure validation errors in JSON response
**Solution**: 
1. Check the error message for the exact location of the failure
2. Review the schema definition
3. Ensure YAML files have valid syntax
4. Verify required properties are present
### Import Errors
**Error**: `ModuleNotFoundError: No module named 'pydantic'`
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```
## Performance Tips
1. **Exclude Unnecessary Folders**: Use a schema that only validates relevant paths
2. **Optimize Schema**: Avoid overly complex patterns in patternProperties
3. **Reduce File Count**: Archive or remove unused YAML files from the validation directory
4. **Cache Results**: Consider caching validation results for CI/CD pipelines
## License
See the LICENSE file for details.
## Support
For issues, questions, or suggestions, please refer to the project repository or contact the maintainers.
