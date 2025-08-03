# Contributing to Integration Watchdog

Thank you for your interest in contributing! This document provides guidelines for contributing to this HACS Blueprint package.

## 🎯 Project Overview

Integration Watchdog is a **Blueprint-only HACS package** that:
- Monitors entity health via Watchman integration
- Auto-reloads failing integrations via Spook integration  
- Escalates to Home Assistant restart after retry limit
- Provides user notifications throughout the process

## 🚀 Development Setup

### Prerequisites
- Python 3.11+
- Home Assistant test instance
- [Watchman](https://github.com/dummylabs/thewatchman) integration installed
- [Spook](https://github.com/frenck/spook) integration installed

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/USER/integration-watchdog.git
   cd integration-watchdog
   ```

2. **Set up virtual environment with uv**:
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install development dependencies
   uv pip install homeassistant pyyaml
   ```

3. **Validate setup**:
   ```bash
   # Run validation checks
   ./.github/workflows/validate_local.sh
   ```

## 📝 Making Changes

### Blueprint Modifications

1. **Edit the main blueprint**: `blueprints/automation/integration_watchdog_auto.yaml`
2. **Key areas to consider**:
   - **Inputs**: Add/modify blueprint configuration options
   - **Variables**: Update Jinja2 template logic for entity processing
   - **Actions**: Modify automation behavior and service calls
   - **Error Handling**: Improve robustness and edge case handling

### Documentation Updates

1. **README.md**: Update installation, configuration, or troubleshooting info
2. **Blueprint comments**: Add inline documentation for complex logic
3. **Examples**: Provide additional configuration examples

### Testing Changes

#### Manual Testing Process
1. **Install prerequisites** (Watchman + Spook) in test HA instance
2. **Import modified blueprint** via raw GitHub URL
3. **Create automation** with test configuration
4. **Simulate failures**:
   ```yaml
   # Developer Tools -> States
   # Set entity to "unavailable" manually
   sensor.test_entity: unavailable
   ```
5. **Verify behavior**:
   - Check automation triggers after 5 minutes
   - Confirm reload calls are made
   - Validate notifications are sent
   - Test retry and restart escalation

#### Automated Validation
```bash
# YAML syntax validation
python -c "import yaml; yaml.safe_load(open('blueprints/automation/integration_watchdog_auto.yaml'))"

# HACS validation (requires Docker)
docker run --rm -v $(pwd):/workspace ghcr.io/hacs/action:main --category automation

# Full CI pipeline
./.github/workflows/validate_local.sh
```

## 🔍 Code Style Guidelines

### Blueprint YAML Standards
- **Indentation**: 2 spaces, no tabs
- **Line length**: Max 120 characters
- **Comments**: Document complex Jinja2 templates
- **Variables**: Use descriptive names (`entry_ids` not `eids`)
- **Error handling**: Include fallbacks for missing services/entities

### Jinja2 Templates
- **Filters**: Use built-in HA filters when possible (`config_entry_id`, `reject`, `unique`)
- **Safety**: Always provide fallbacks (`or []`, `| default(0)`)
- **Readability**: Break complex templates across multiple lines
- **Testing**: Validate templates in Developer Tools -> Template

### Documentation
- **Clarity**: Write for users with basic HA knowledge
- **Examples**: Provide concrete configuration examples
- **Troubleshooting**: Include common issues and solutions
- **Links**: Reference external dependencies with version info

## 🚀 Submission Process

### Pull Request Guidelines

1. **Branch naming**: Use descriptive names (`feature/add-retry-delay`, `fix/notification-formatting`)

2. **Commit messages**: Follow conventional commits:
   ```
   feat: add configurable retry delay between reload attempts
   fix: handle missing notify service gracefully  
   docs: update troubleshooting section with common errors
   ```

3. **PR description**: Include:
   - Summary of changes
   - Testing performed
   - Breaking changes (if any)
   - Related issues

4. **Testing checklist**:
   - [ ] Blueprint YAML syntax is valid
   - [ ] Manual testing with real HA instance performed
   - [ ] Documentation updated for changes
   - [ ] CI validation passes

### Review Process

1. **Automated checks**: CI must pass (HACS validate, hassfest, YAML validation)
2. **Manual review**: Maintainer will review for:
   - Code quality and HA best practices
   - Documentation completeness
   - Breaking change assessment
3. **Testing**: Complex changes may require additional testing by maintainer

## 🐛 Reporting Issues

### Bug Reports
Include:
- Home Assistant version
- Watchman integration version  
- Spook integration version
- Blueprint configuration (sanitized)
- Error logs from HA (if applicable)
- Steps to reproduce

### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Impact on existing functionality

## 📚 Resources

- [Home Assistant Blueprint Documentation](https://www.home-assistant.io/docs/blueprint/)
- [Jinja2 Templating in HA](https://www.home-assistant.io/docs/configuration/templating/)
- [HACS Integration Guidelines](https://hacs.xyz/docs/publish/integration)
- [Watchman Integration](https://github.com/dummylabs/thewatchman)
- [Spook Integration](https://github.com/frenck/spook)

## 🏆 Recognition

Contributors will be acknowledged in:
- GitHub contributors list
- Release notes for significant contributions
- README.md acknowledgments section

Thank you for contributing to Integration Watchdog! 🎉