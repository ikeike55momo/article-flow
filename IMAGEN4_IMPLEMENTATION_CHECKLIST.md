# Imagen4 MCP Migration - Implementation Checklist

## Pre-Migration Checklist

### 1. Prerequisites
- [ ] GEMINI_API_KEY added to GitHub Secrets
- [ ] Backup branch created: `backup/pre-imagen4-migration`
- [ ] Current metrics documented (cost per image, success rate, generation time)
- [ ] Team notified of migration schedule
- [ ] Rollback plan reviewed and approved

### 2. Code Preparation
- [ ] `prompts/image_generation_mcp.md` created and reviewed
- [ ] Workflow changes prepared but not committed
- [ ] Test workflow created and validated
- [ ] Documentation updated

### 3. Testing Complete
- [ ] Local MCP testing successful
- [ ] GitHub Actions test workflow passes
- [ ] Image quality validated
- [ ] Performance benchmarks met
- [ ] Error handling tested

## Migration Day Checklist

### Morning (9:00 AM - 10:00 AM)
- [ ] Check system status - no ongoing article generations
- [ ] Create migration tracking issue in GitHub
- [ ] Final backup of current workflow file
- [ ] Notify team - migration starting

### Phase 1: Parallel Run (10:00 AM - 12:00 PM)
- [ ] Deploy new workflow with MCP job disabled
- [ ] Enable MCP job for single test article
- [ ] Compare outputs with Python-generated images
- [ ] Verify metadata compatibility
- [ ] Check downstream processes (Google Drive upload)

### Phase 2: Gradual Rollout (1:00 PM - 3:00 PM)
- [ ] Enable MCP for 25% of new runs
- [ ] Monitor error rates and performance
- [ ] Collect initial feedback
- [ ] Address any immediate issues

### Phase 3: Full Migration (3:00 PM - 4:00 PM)
- [ ] Enable MCP for 100% of new runs
- [ ] Disable Python image generation job
- [ ] Update default configuration
- [ ] Monitor closely for issues

### Phase 4: Cleanup (4:00 PM - 5:00 PM)
- [ ] Archive Python scripts (don't delete yet)
- [ ] Update documentation
- [ ] Close migration tracking issue
- [ ] Send migration success notification

## Post-Migration Monitoring (Next 7 Days)

### Day 1
- [ ] Monitor all image generation runs
- [ ] Check error logs every 2 hours
- [ ] Verify cost reduction
- [ ] Document any issues

### Day 2-3
- [ ] Daily performance report
- [ ] User feedback collection
- [ ] Fine-tune prompts if needed
- [ ] Update error handling

### Day 4-7
- [ ] Weekly metrics comparison
- [ ] Cost analysis report
- [ ] Performance optimization
- [ ] Plan for Python script removal

## Rollback Triggers

Initiate rollback if ANY of these occur:
- [ ] Error rate > 20% for 1 hour
- [ ] Image generation time > 5 minutes consistently
- [ ] Critical production failure
- [ ] Security concerns identified
- [ ] API quota exhaustion

## Rollback Procedure

### Immediate Rollback (< 15 minutes)
```bash
# 1. Revert workflow file
git checkout backup/pre-imagen4-migration -- .github/workflows/article-generation-v2.yml

# 2. Commit and push
git commit -m "ROLLBACK: Revert to Python image generation due to [REASON]"
git push origin main

# 3. Verify Python generation works
# Run test article generation

# 4. Notify team
# Send rollback notification with reason
```

### Communication Templates

**Migration Start**:
```
🚀 Image Generation Migration Starting
- Migrating from Python/gpt-image-1 to MCP/Imagen4
- Expected completion: 5:00 PM
- Impact: Minimal - gradual rollout
- Contact: [Your Name] for issues
```

**Migration Success**:
```
✅ Image Generation Migration Complete
- Successfully migrated to MCP + Imagen4
- Cost reduction: ~80% per image
- Performance: 3x faster generation
- All systems operational
```

**Rollback Notification**:
```
⚠️ Image Generation Rollback Initiated
- Issue: [Specific reason]
- Action: Reverted to Python implementation
- Impact: No service disruption
- Next steps: Investigation and fix
```

## Success Metrics Tracking

### Cost Metrics
| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| Cost per image | $0.04 | $0.008 | ___ |
| Cost per article (5 images) | $0.20 | $0.04 | ___ |
| Monthly image cost | $600 | $120 | ___ |

### Performance Metrics
| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| Time per image | 60s | 20s | ___ |
| Total generation time | 5 min | 2 min | ___ |
| Success rate | 95% | 99% | ___ |

### Quality Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Resolution compliance | 100% | ___ |
| Style consistency | 95% | ___ |
| Alt text quality | 100% | ___ |

## Lessons Learned (To be filled post-migration)

### What Went Well
- 
- 
- 

### Challenges Faced
- 
- 
- 

### Improvements for Next Time
- 
- 
- 

## Sign-offs

- [ ] Technical Lead: _________________ Date: _______
- [ ] DevOps Lead: _________________ Date: _______
- [ ] Product Owner: _________________ Date: _______

---

**Remember**: The goal is zero-downtime migration with improved performance and reduced costs. Take time to validate each step!