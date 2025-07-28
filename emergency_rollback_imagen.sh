#!/bin/bash
# Emergency Rollback Script for Imagen4 Migration
# This script quickly reverts to Python-based image generation

set -e

echo "🚨 EMERGENCY ROLLBACK - Imagen4 to Python Image Generation"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f ".github/workflows/article-generation-v2.yml" ]; then
    echo "❌ Error: Not in article-flow root directory"
    echo "Please run from the repository root"
    exit 1
fi

# Get rollback reason
echo -n "Enter rollback reason (brief): "
read ROLLBACK_REASON

# Create rollback branch
ROLLBACK_BRANCH="rollback/imagen4-$(date +%Y%m%d-%H%M%S)"
echo ""
echo "Creating rollback branch: $ROLLBACK_BRANCH"
git checkout -b "$ROLLBACK_BRANCH"

# Revert the workflow file
echo "Reverting workflow file..."
git checkout backup/pre-imagen4-migration -- .github/workflows/article-generation-v2.yml

# Ensure Python scripts are still present
if [ ! -f "github-actions/scripts/generate_images_gpt.py" ]; then
    echo "⚠️  Warning: Python scripts not found, restoring from backup branch"
    git checkout backup/pre-imagen4-migration -- github-actions/scripts/generate_images_gpt.py
    git checkout backup/pre-imagen4-migration -- github-actions/scripts/generate_images_imagen.py
fi

# Create rollback commit
echo "Creating rollback commit..."
git add .github/workflows/article-generation-v2.yml
git add github-actions/scripts/generate_images*.py 2>/dev/null || true

COMMIT_MSG="EMERGENCY ROLLBACK: Revert to Python image generation

Reason: $ROLLBACK_REASON
Rolled back at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Rollback branch: $ROLLBACK_BRANCH"

git commit -m "$COMMIT_MSG"

# Push to origin
echo ""
echo "Pushing rollback to origin..."
git push origin "$ROLLBACK_BRANCH"

# Create PR
echo ""
echo "Creating Pull Request..."
PR_BODY="## Emergency Rollback

**Reason**: $ROLLBACK_REASON

**Changes**:
- Reverted workflow to use Python-based image generation
- Restored gpt-image-1 as primary image generator
- Disabled MCP/Imagen4 integration

**Next Steps**:
1. Merge this PR immediately
2. Verify image generation is working
3. Investigate and fix Imagen4 issues
4. Plan re-migration

**Rollback Time**: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Try to create PR using gh CLI if available
if command -v gh &> /dev/null; then
    gh pr create \
        --title "🚨 EMERGENCY: Rollback Imagen4 to Python image generation" \
        --body "$PR_BODY" \
        --base main \
        --label "emergency,rollback" \
        --assignee "@me"
    
    echo "✅ Pull request created successfully"
else
    echo "⚠️  gh CLI not found. Please create PR manually with this information:"
    echo ""
    echo "Title: 🚨 EMERGENCY: Rollback Imagen4 to Python image generation"
    echo ""
    echo "$PR_BODY"
fi

# Log rollback event
ROLLBACK_LOG="rollback_logs/imagen4_rollback_$(date +%Y%m%d-%H%M%S).log"
mkdir -p rollback_logs
cat > "$ROLLBACK_LOG" << EOF
Rollback Event Log
==================
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Reason: $ROLLBACK_REASON
Branch: $ROLLBACK_BRANCH
Operator: $(git config user.name)

Actions Taken:
1. Created rollback branch
2. Reverted workflow file
3. Restored Python scripts
4. Created rollback commit
5. Pushed to origin
6. Created PR for immediate merge

Next Steps:
1. Merge PR immediately
2. Test image generation
3. Monitor for issues
4. Plan fixes
EOF

echo ""
echo "📝 Rollback logged to: $ROLLBACK_LOG"

# Send notification if webhook configured
if [ ! -z "$SLACK_WEBHOOK" ]; then
    curl -X POST $SLACK_WEBHOOK \
        -H 'Content-type: application/json' \
        -d "{
            \"text\": \"🚨 EMERGENCY ROLLBACK: Imagen4 → Python image generation\",
            \"attachments\": [{
                \"color\": \"danger\",
                \"fields\": [
                    {\"title\": \"Reason\", \"value\": \"$ROLLBACK_REASON\", \"short\": false},
                    {\"title\": \"Branch\", \"value\": \"$ROLLBACK_BRANCH\", \"short\": true},
                    {\"title\": \"Time\", \"value\": \"$(date -u +%H:%M UTC)\", \"short\": true}
                ]
            }]
        }" 2>/dev/null || echo "⚠️  Slack notification failed"
fi

echo ""
echo "✅ ROLLBACK COMPLETE!"
echo ""
echo "REQUIRED ACTIONS:"
echo "1. Go to GitHub and merge the PR immediately"
echo "2. Run a test article generation to verify Python scripts work"
echo "3. Monitor image generation for the next hour"
echo "4. Create incident report"
echo ""
echo "PR URL will be shown above if gh CLI is installed"
echo "Otherwise, create PR manually from branch: $ROLLBACK_BRANCH"