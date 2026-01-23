# spec-reader

## Purpose
Read and parse all Spec-Kit Plus files

## Responsibilities
- Locate and read spec files in the project structure
- Parse spec file formats (Markdown, YAML, JSON)
- Extract key information from specs (requirements, acceptance criteria, constraints)
- Validate spec file structure and completeness
- Return structured data representation of spec contents

## Inputs
- Path to spec file or directory containing spec files
- Optional: Specific sections or fields to extract

## Outputs
- Parsed spec data in structured format
- Validation results indicating completeness
- List of extracted requirements and constraints
- Error messages for invalid or incomplete specs

## Rules
- NEVER modify spec files during read operations
- NEVER assume spec file format without verification
- NEVER ignore validation errors silently
- ALWAYS maintain original spec file integrity

## When to use this skill
Use when agents need to understand existing specifications, validate spec completeness, or extract structured information from spec files for further processing.