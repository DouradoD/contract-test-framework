#!/usr/bin/env python3
from prance import ResolvingParser
import sys

def validate_app(file_path: str):
    try:
        ResolvingParser(file_path)
        print("✅ OpenAPI spec is valid!")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="api/app/openapi.json", help="OpenAPI file path or URL")
    args = parser.parse_args()
    validate_app(args.file)