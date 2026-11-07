#!/usr/bin/env python3
"""
Validate knowledge modules, projects, and tasks.
Runs offline; no external dependencies.
"""

import json
import sys
from pathlib import Path

def validate_module(module_file):
    """Validate a module record."""
    try:
        with open(module_file) as f:
            data = json.load(f)
        module = data.get("module", {})
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    
    required_fields = [
        "id", "version", "title", "license",
        "learning_objectives", "prerequisites",
        "content"
    ]
    
    errors = []
    for field in required_fields:
        if field not in module:
            errors.append(f"Missing required field: {field}")
    
    # Validate worked examples (may be in content section)
    content = module.get("content", {})
    examples = content.get("worked_examples", module.get("worked_examples", []))
    if len(examples) < 3:
        errors.append(f"Module should have at least 3 worked examples; found {len(examples)}")
    
    for i, example in enumerate(examples):
        if "id" not in example and "title" not in example:
            errors.append(f"Worked example {i} missing 'id' or 'title'")
    
    # Validate exercises (may be in content section)
    exercises = content.get("exercises", module.get("exercises", []))
    if len(exercises) < 5:
        errors.append(f"Module should have at least 5 exercises; found {len(exercises)}")
    
    for i, exercise in enumerate(exercises):
        if "id" not in exercise and "prompt" not in exercise:
            errors.append(f"Exercise {i} missing 'id' or 'prompt'")
    
    return errors
    
    return errors

def validate_project(project_file):
    """Validate a project record."""
    try:
        with open(project_file) as f:
            project = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    
    required_fields = [
        "project_id", "version", "title", "purpose",
        "status", "license"
    ]
    
    errors = []
    for field in required_fields:
        if field not in project:
            errors.append(f"Missing required field: {field}")
    
    valid_statuses = [
        "planning", "in_progress", "first_pathway_complete_validation_pending",
        "complete", "paused", "archived"
    ]
    if project.get("status") not in valid_statuses:
        errors.append(f"Invalid status: {project.get('status')}. Must be one of: {', '.join(valid_statuses)}")
    
    return errors

def validate_task(task_file):
    """Validate a task record."""
    try:
        with open(task_file) as f:
            task = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    
    required_fields = [
        "task_id", "project_id", "title", "objective",
        "scope", "deliverables", "status"
    ]
    
    errors = []
    for field in required_fields:
        if field not in task:
            errors.append(f"Missing required field: {field}")
    
    valid_statuses = ["open", "in_progress", "pending_review", "approved", "blocked", "cancelled"]
    if task.get("status") not in valid_statuses:
        errors.append(f"Invalid status: {task.get('status')}. Must be one of: {', '.join(valid_statuses)}")
    
    if not task.get("time_estimate_hours"):
        errors.append("Missing time_estimate_hours")
    
    if not task.get("difficulty"):
        errors.append("Missing difficulty (beginner/intermediate/advanced)")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Validate knowledge commons records")
        print("Usage: python3 validate.py <module|project|task> <file.json> [<file2.json> ...]")
        print()
        print("Examples:")
        print("  python3 validate.py module data/modules.json")
        print("  python3 validate.py project data/projects/*.json")
        print("  python3 validate.py task data/tasks/*.json")
        sys.exit(0)
    
    record_type = sys.argv[1]
    files = sys.argv[2:]
    
    if not files:
        print("Error: no files specified")
        sys.exit(1)
    
    if record_type == "module":
        validator = validate_module
    elif record_type == "project":
        validator = validate_project
    elif record_type == "task":
        validator = validate_task
    else:
        print(f"Unknown record type: {record_type}")
        sys.exit(1)
    
    all_passed = True
    for file_path in files:
        errors = validator(file_path)
        if errors:
            print(f"✗ {file_path}")
            for error in errors:
                print(f"    {error}")
            all_passed = False
        else:
            print(f"✓ {file_path}")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
