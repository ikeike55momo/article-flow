# Serena Context Management for Article Flow

This Serena setup provides efficient context management for the AI-powered article generation workflow, organizing all components needed for maintaining and updating the article generation pipeline.

## Quick Start

### Loading Contexts for Common Tasks

#### Creating a New Article
```bash
serena load article_generation
# Loads: templates, prompts, samples
```

#### Debugging Workflow Issues
```bash
serena load workflow_management  
# Loads: workflow, config, prompts
```

#### Updating Templates
```bash
serena load update_templates
# Loads: templates, samples
```

## Context Overview

### 🔧 Core Contexts

#### `workflow/` - GitHub Actions Automation
- **Purpose**: GitHub Actions workflow files and automation scripts
- **Key Files**: `article-generation-v4.yml`, deployment guides, script documentation
- **Usage**: Workflow debugging, deployment management, automation updates

#### `templates/` - Article Templates & Styling  
- **Purpose**: HTML templates, CSS styling, and structure guidelines
- **Key Files**: Template analysis, style guides, CSS class documentation
- **Usage**: Article format consistency, styling updates, template modifications

#### `prompts/` - AI Prompt Engineering
- **Purpose**: AI prompt files for each workflow phase
- **Key Files**: Prompt evolution history, current production prompts, optimization guides
- **Usage**: Prompt improvements, content quality tuning, workflow phase updates

#### `samples/` - Reference Materials
- **Purpose**: Sample articles, examples, and quality benchmarks
- **Key Files**: Complete example articles, template analysis, best practices
- **Usage**: Quality standards, template validation, content benchmarking

#### `research/` - Data & Research Management
- **Purpose**: Research pipeline, data flow, and quality validation
- **Key Files**: Data flow architecture, source reliability guides, output management
- **Usage**: Research optimization, quality improvement, data pipeline maintenance

#### `config/` - System Configuration
- **Purpose**: Configuration files, rules, and system settings
- **Key Files**: Workflow configuration, fact-checking rules, quality thresholds
- **Usage**: System tuning, rule updates, performance optimization

## Project Architecture

### Article Generation Pipeline (V4)
```
Input → Analysis → Research → Structure → Content → Quality → Output
   ↓        ↓         ↓          ↓         ↓        ↓       ↓
 User    Claude    Gemini     Claude    Claude   Claude  Package
Request Analysis  Parallel   Planning  Writing  Check   Assembly
                  Research
```

### Key Features
- **10-Job Pipeline**: Fully automated article generation
- **Parallel Research**: 3 concurrent Gemini API batches  
- **Quality Scoring**: Numerical fact-checking and validation
- **5 Deliverables**: HTML article, research, factcheck, SEO, images
- **Template-Driven**: Consistent professional output format

### Technology Stack
- **AI**: Claude (Anthropic) for content generation
- **Research**: Gemini API for web research
- **Images**: Imagen4 via MCP servers
- **Deployment**: GitHub Actions
- **Output**: HTML articles with embedded styling

## Usage Patterns

### For Content Creators
- Review sample articles for quality standards
- Understand template structure and requirements
- Monitor research quality and citation standards
- Validate output against template compliance

### For Developers  
- Use workflow context for deployment and debugging
- Reference prompt evolution for AI improvements
- Monitor research data flow for performance optimization
- Update templates and configurations as needed

### for Quality Assurance
- Use config context for quality thresholds and rules
- Review research context for source validation
- Check samples context for consistency standards
- Monitor workflow context for process compliance

## File Organization

### Context Structure
```
.serena/
├── config.yaml                 # Main Serena configuration
└── contexts/
    ├── workflow/               # GitHub Actions & automation
    │   ├── README.md
    │   ├── workflow-files.md
    │   └── deployment-guide.md
    ├── templates/              # HTML templates & styling
    │   ├── README.md
    │   └── style-guide.md
    ├── prompts/                # AI prompt engineering
    │   ├── README.md
    │   └── prompt-evolution.md
    ├── samples/                # Reference materials
    │   ├── README.md
    │   └── template-analysis.md
    ├── research/               # Data management
    │   ├── README.md
    │   └── data-flow.md
    └── config/                 # System configuration
        └── README.md
```

### Quick Reference Files

#### Essential Reading for New Contributors
1. `workflow/README.md` - Understanding the automation pipeline
2. `templates/README.md` - Article structure and styling requirements  
3. `samples/template-analysis.md` - Quality standards and best practices
4. `research/data-flow.md` - How research and validation works

#### Maintenance & Updates
1. `workflow/deployment-guide.md` - Deployment procedures
2. `prompts/prompt-evolution.md` - Prompt development history
3. `config/README.md` - System configuration and rules
4. `templates/style-guide.md` - Template customization guidelines

## Context Groups

### `article_generation` Group
**Purpose**: Essential files for creating new articles
**Includes**: templates, prompts, samples
**Use Case**: AI content generation, template compliance, quality standards

### `workflow_management` Group  
**Purpose**: Workflow automation and configuration
**Includes**: workflow, config  
**Use Case**: Deployment, debugging, system maintenance

### `content_research` Group
**Purpose**: Research and reference materials
**Includes**: research, samples
**Use Case**: Content quality, source validation, research optimization

## Maintenance Guidelines

### Regular Updates
- **Monthly**: Review prompt performance and update if needed
- **Quarterly**: Update sample articles and templates for current best practices
- **Bi-annually**: Review workflow configuration and optimize performance
- **Annually**: Comprehensive review of all contexts and documentation

### Quality Assurance
- All contexts include comprehensive README files
- Examples and templates are kept current
- Documentation reflects actual implementation
- Performance metrics are tracked and documented

### Collaboration
- Each context is self-contained with clear documentation
- Cross-references between contexts are clearly marked
- Usage patterns are documented for different team roles
- Update procedures are standardized and documented

This Serena setup ensures efficient context management for the complex article generation workflow, making it easier to maintain, update, and scale the system while preserving quality and consistency.