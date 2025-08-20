# Serena Setup Guide for Article Flow

## Quick Setup

### 1. Initialize Serena (if not already installed)
```bash
# Install Serena CLI if needed
npm install -g @anthropic/serena

# Navigate to project root
cd article-flow

# Serena will automatically detect the .serena/ directory
serena init
```

### 2. Verify Setup
```bash
# Check Serena configuration
serena status

# List available contexts
serena list

# Test loading a context group
serena load article_generation
```

## Context Groups & Usage

### For Article Creation
```bash
# Load essential files for new article generation
serena load article_generation
# Includes: templates, prompts, samples

# Alternative: Load specific contexts
serena load templates prompts
```

### For Workflow Debugging
```bash
# Load workflow and configuration files
serena load workflow_management
# Includes: workflow, config

# For detailed debugging
serena load workflow config prompts
```

### For Template Updates
```bash
# Load template and reference files
serena load update_templates  
# Includes: templates, samples

# Alternative for full template work
serena load templates samples config
```

### For Research Optimization
```bash
# Load research and reference materials
serena load content_research
# Includes: research, samples

# For complete research workflow
serena load research config workflow
```

## Individual Context Loading

### Load Single Contexts
```bash
serena load workflow      # GitHub Actions workflow files
serena load templates     # HTML templates and styling  
serena load prompts       # AI prompt files
serena load samples       # Reference articles and examples
serena load research      # Research pipeline and data flow
serena load config        # Configuration and rules
```

### Context Contents Preview
```bash
# See what's included in a context before loading
serena describe templates
serena describe workflow
serena describe research
```

## Working with Contexts

### Efficient Context Switching
```bash
# Switch between different workflow phases
serena load prompts       # For prompt development
serena load templates     # For template updates
serena load workflow      # For deployment issues
```

### Combined Context Loading
```bash
# For comprehensive article development
serena load templates prompts samples

# For full system maintenance
serena load workflow config research

# For quality assurance work
serena load samples research config
```

## Context File Locations

### Reference Quick Access
All contexts point to actual project files:

- **workflow/**: `.github/workflows/`, `github-actions/scripts/`
- **templates/**: `sample/articles/` (templates and styling)
- **prompts/**: `prompts/` directory (all prompt files)
- **samples/**: `sample/articles/` (examples and references)
- **research/**: Research scripts and data flow documentation
- **config/**: `config/` directory (YAML configurations)

### File Organization
```
article-flow/
├── .serena/                    # Serena context definitions
├── .github/workflows/          # → workflow context
├── prompts/                    # → prompts context  
├── sample/articles/            # → templates & samples contexts
├── config/                     # → config context
├── github-actions/scripts/     # → workflow context (scripts)
└── output/                     # Generated articles (not in contexts)
```

## Common Workflows

### Creating a New Article
1. **Load Templates**: `serena load templates samples`
2. **Review Structure**: Read `templates/README.md` and sample articles
3. **Check Prompts**: `serena load prompts` to understand AI generation
4. **Run Workflow**: Use GitHub Actions with proper parameters

### Debugging Workflow Issues
1. **Load Workflow**: `serena load workflow config`
2. **Check Logs**: Review GitHub Actions execution logs
3. **Validate Config**: Check configuration files and rules
4. **Test Changes**: Use test workflows before production

### Updating Templates
1. **Load References**: `serena load templates samples`
2. **Study Examples**: Review `template-analysis.md` for patterns
3. **Update Files**: Modify templates in `sample/articles/`
4. **Test Generation**: Run workflow to validate changes
5. **Update Docs**: Update template documentation if needed

### Improving Content Quality
1. **Load Research**: `serena load research samples config`
2. **Review Standards**: Check quality metrics and benchmarks
3. **Analyze Sources**: Review research data flow and validation
4. **Update Rules**: Modify fact-checking and quality rules
5. **Test Changes**: Validate with test article generation

## Configuration Customization

### Modifying Context Groups
Edit `.serena/config.yaml` to customize context groups:

```yaml
groups:
  my_custom_group:
    contexts: ["templates", "prompts", "config"]
    description: "Custom workflow for my specific needs"
```

### Adding New Contexts
1. Create new directory: `.serena/contexts/my_context/`
2. Add README.md with documentation
3. Update `.serena/config.yaml`:

```yaml
contexts:
  my_context:
    path: "contexts/my_context"
    description: "Description of new context"
    priority: "medium"
```

### Context Priorities
- **high**: Essential for core functionality (workflow, templates, prompts)
- **medium**: Important for quality and maintenance (samples, research, config)
- **low**: Optional or specialized contexts

## Best Practices

### Context Loading Strategy
1. **Start Small**: Load only what you need for current task
2. **Group Related**: Use context groups for common workflows
3. **Progressive Loading**: Add more contexts as needed
4. **Regular Cleanup**: Clear contexts when switching to different tasks

### File Management
1. **Read Documentation**: Each context includes comprehensive README
2. **Follow Patterns**: Use established file organization
3. **Update Documentation**: Keep context docs current with changes
4. **Test Changes**: Validate updates with actual workflow runs

### Performance Tips
1. **Selective Loading**: Don't load all contexts unnecessarily
2. **Use Groups**: Predefined groups are optimized for common tasks
3. **Context Switching**: Switch contexts rather than accumulating
4. **Regular Updates**: Keep Serena and contexts current

## Troubleshooting

### Common Issues

#### Context Not Found
```bash
# Verify context exists
serena list

# Check configuration
cat .serena/config.yaml

# Reinitialize if needed
serena init --force
```

#### File Access Issues
```bash
# Check file permissions
ls -la .serena/

# Verify paths in config
serena describe context_name
```

#### Performance Issues
```bash
# Clear context cache
serena clear

# Reload with minimal contexts
serena load templates
```

### Getting Help
```bash
# General help
serena help

# Context-specific help
serena help load

# Configuration help
serena help config
```

## Integration with Article Workflow

### Pre-Generation Setup
1. `serena load article_generation`
2. Review current templates and samples
3. Check prompt versions for accuracy
4. Verify GitHub Actions workflow status

### During Development
1. `serena load workflow` for deployment debugging
2. `serena load prompts` for content quality tuning
3. `serena load config` for rule adjustments
4. `serena load research` for data flow optimization

### Post-Generation Review
1. `serena load samples` to compare output quality
2. `serena load research` to validate source quality
3. `serena load config` to update quality thresholds
4. `serena load templates` to refine formatting

This setup provides comprehensive context management for the complex article generation workflow, making it significantly easier to maintain, debug, and improve the system while ensuring consistent quality output.