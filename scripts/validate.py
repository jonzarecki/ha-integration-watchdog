#!/usr/bin/env python3
"""
Validation script for Integration Watchdog blueprint.
Run this script to validate the blueprint YAML and project structure.
"""

import json
import sys
import yaml
from pathlib import Path

# Custom YAML loader that handles Home Assistant tags
class HAYamlLoader(yaml.SafeLoader):
    """YAML loader that handles Home Assistant specific tags like !input."""
    pass

def input_constructor(loader, node):
    """Handle !input tags in Home Assistant blueprints."""
    return f"!input {loader.construct_scalar(node)}"

# Register the !input constructor
HAYamlLoader.add_constructor('!input', input_constructor)

def validate_blueprint_yaml():
    """Validate the main blueprint YAML file."""
    print("🔍 Validating blueprint YAML...")
    
    blueprint_path = Path("blueprints/automation/integration_watchdog_auto.yaml")
    if not blueprint_path.exists():
        print(f"❌ Blueprint file not found: {blueprint_path}")
        return False
        
    try:
        with open(blueprint_path, 'r') as f:
            blueprint = yaml.load(f, Loader=HAYamlLoader)
            
        # Basic structure validation
        required_keys = ['blueprint', 'trigger', 'action']
        for key in required_keys:
            if key not in blueprint:
                print(f"❌ Missing required key: {key}")
                return False
                
        # Blueprint metadata validation
        bp = blueprint['blueprint']
        if bp.get('domain') != 'automation':
            print(f"❌ Blueprint domain must be 'automation', got: {bp.get('domain')}")
            return False
            
        required_bp_keys = ['name', 'input']
        for key in required_bp_keys:
            if key not in bp:
                print(f"❌ Missing required blueprint key: {key}")
                return False
                
        # Input validation
        inputs = bp['input']
        required_inputs = ['issue_sensor', 'notify_service', 'max_reload_attempts']
        for input_key in required_inputs:
            if input_key not in inputs:
                print(f"❌ Missing required input: {input_key}")
                return False
                
        print("✅ Blueprint YAML validation passed")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Blueprint validation failed: {e}")
        return False

def validate_hacs_json():
    """Validate the HACS configuration file."""
    print("🔍 Validating hacs.json...")
    
    hacs_path = Path("hacs.json")
    if not hacs_path.exists():
        print(f"❌ HACS config file not found: {hacs_path}")
        return False
        
    try:
        with open(hacs_path, 'r') as f:
            hacs_config = json.load(f)
            
        # Required fields validation
        required_fields = ['name', 'description', 'domains', 'homeassistant']
        for field in required_fields:
            if field not in hacs_config:
                print(f"❌ Missing required HACS field: {field}")
                return False
                
        # Domain validation
        domains = hacs_config.get('domains', [])
        if 'automation' not in domains:
            print(f"❌ HACS domains must include 'automation', got: {domains}")
            return False
            
        # Content structure validation
        if hacs_config.get('content_in_root', True):
            print("⚠️  Warning: content_in_root should be false for organized structure")
            
        print("✅ HACS configuration validation passed")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ HACS validation failed: {e}")
        return False

def validate_structure():
    """Validate the repository structure."""
    print("🔍 Validating repository structure...")
    
    required_paths = [
        "blueprints/automation/integration_watchdog_auto.yaml",
        "hacs.json", 
        "README.md",
        ".github/workflows/validate.yml"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
            
    if missing_paths:
        print(f"❌ Missing required files/directories:")
        for path in missing_paths:
            print(f"   - {path}")
        return False
        
    print("✅ Repository structure validation passed")
    return True

def main():
    """Run all validations."""
    print("🚀 Starting Integration Watchdog validation...\n")
    
    validations = [
        validate_structure,
        validate_hacs_json,
        validate_blueprint_yaml
    ]
    
    all_passed = True
    for validation in validations:
        if not validation():
            all_passed = False
        print()  # Empty line for readability
        
    if all_passed:
        print("🎉 All validations passed! Ready for release.")
        return 0
    else:
        print("💥 Some validations failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())