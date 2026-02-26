#!/usr/bin/env python3
"""
Quick validation script for skills - minimal dependency-free version
"""

import sys
import re
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill without external dependencies"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read frontmatter
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Could not read SKILL.md: {e}"

    if not content.startswith('---'):
        return False, "No YAML frontmatter found (must start with ---)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    
    # Simple parser for "key: value" lines
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Relaxed validation for name (allow any non-empty string)
    name = frontmatter['name']
    if not name:
        return False, "Name cannot be empty"
        
    # Validate description length
    description = frontmatter['description']
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} chars). Max 1024."

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
