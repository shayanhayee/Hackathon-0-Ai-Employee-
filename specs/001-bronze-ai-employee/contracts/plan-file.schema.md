# Plan File Schema

**Version**: 1.0.0
**Feature**: 001-bronze-ai-employee
**Purpose**: Define the structure and format for AI-generated plan files

## Overview

Plan files are AI-generated markdown documents that provide structured action plans for completing tasks. They are created by Claude Code CLI based on task file content and Company_Handbook.md context.

## File Format

**Extension**: `.md` (Markdown)
**Location**: `/Plans`
**Encoding**: UTF-8
**Naming Convention**: `plan-{task-id}.md`

## Structure

### Complete Example

```markdown
---
task_id: task-001
generated: 2026-02-12T10:35:00Z
status: draft
estimated_duration: 2 hours
ai_model: claude-sonnet-4-5
---

# Plan: Research competitor pricing

**Task**: task-001.md
**Generated**: 2026-02-12 10:35 AM

## Objective

Research and analyze competitor pricing strategies for our product category to inform Q2 pricing review.

## Steps

### 1. Identify Top 5 Competitors

**Actions**:
- Review Company_Handbook.md market analysis section
- Search industry reports for SaaS project management tools
- Compile list of direct competitors

**Deliverable**: List of 5 competitors with company names and URLs

**Duration**: 30 minutes

---

### 2. Document Pricing Tiers

**Actions**:
- Visit each competitor's pricing page
- Screenshot pricing tables
- Extract pricing data into spreadsheet
- Note features included at each tier

**Deliverable**: Comparison spreadsheet with pricing tiers

**Duration**: 45 minutes

---

### 3. Analyze Value Propositions

**Actions**:
- Compare features across competitors
- Identify pricing patterns (per-user, per-project, flat-rate)
- Document competitive advantages
- Note gaps in our current pricing

**Deliverable**: Analysis document with recommendations

**Duration**: 45 minutes

## Resources

### Required
- Company_Handbook.md (market analysis section)
- Spreadsheet software (Excel, Google Sheets)
- Web browser for competitor research

### Optional
- Industry reports (if available)
- Previous pricing analysis documents

## Assumptions

1. Competitor pricing is publicly available on websites
2. Focus on direct competitors (SaaS project management)
3. Analysis covers current pricing only (not historical trends)
4. No need to contact competitors directly

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Pricing not public | Low | Medium | Contact sales for quotes |
| Outdated information | Medium | Low | Verify with recent sources |
| Too many competitors | Low | Medium | Focus on top 5 by market share |

## Success Criteria

- [ ] 5 competitors identified and documented
- [ ] Pricing tiers extracted for all competitors
- [ ] Comparison spreadsheet completed
- [ ] Analysis document with recommendations written
- [ ] Findings ready for Q2 pricing review

## Next Steps

1. Execute research steps in order
2. Document findings in shared folder
3. Schedule review meeting with leadership
4. Mark task as complete in AI Employee system
```

## Frontmatter Schema

**Format**: YAML
**Delimiters**: `---` (three hyphens)
**Required**: Yes (all plan files must have frontmatter)

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `task_id` | string | Yes | Links to source task file (must match filename) | `task-001` |
| `generated` | datetime | Yes | ISO 8601 timestamp of plan creation | `2026-02-12T10:35:00Z` |
| `status` | enum | No | Plan status: `draft`, `in-progress`, `completed` | `draft` |
| `estimated_duration` | string | No | Human-readable time estimate | `2 hours`, `3 days` |
| `ai_model` | string | No | AI model used for generation | `claude-sonnet-4-5` |

### Validation Rules

- `task_id` is required and must match filename pattern
- `generated` is required and must be valid ISO 8601 datetime
- `status` if present must be one of: `draft`, `in-progress`, `completed`
- `estimated_duration` is freeform string (no validation)
- `ai_model` is informational only

## Body Schema

**Format**: Markdown
**Required**: Yes (must contain structured plan)

### Required Sections

1. **Title** (H1): `# Plan: {task title}`
2. **Objective**: Clear statement of what the plan achieves
3. **Steps**: Numbered steps with actions and deliverables
4. **Resources**: Required and optional resources
5. **Assumptions**: Explicit assumptions made during planning

### Recommended Sections

6. **Risks & Mitigations**: Potential issues and how to handle them
7. **Success Criteria**: Checklist of completion criteria
8. **Next Steps**: What to do after completing the plan

### Step Structure

Each step should include:
- **Step Number and Title** (H3): `### 1. Identify Competitors`
- **Actions**: Bullet list of specific actions
- **Deliverable**: What this step produces
- **Duration**: Time estimate for this step

### Markdown Features

- Headings (H1 for title, H2 for sections, H3 for steps)
- Bullet lists for actions
- Numbered lists for sequential steps
- Tables for risks, comparisons
- Checkboxes for success criteria
- Bold for emphasis

## Validation

### Required Validations

1. **File Extension**: Must be `.md`
2. **Naming Convention**: Must match `plan-{task-id}.md`
3. **Encoding**: Must be UTF-8
4. **Frontmatter**: Must be present and valid YAML
5. **Required Fields**: `task_id` and `generated` must be present
6. **Body Content**: Must not be empty

### Optional Validations

1. **Task ID Match**: `task_id` in frontmatter should match filename
2. **Required Sections**: Should include Objective, Steps, Resources, Assumptions
3. **Step Structure**: Steps should follow recommended format

### Error Handling

| Error | Severity | Action |
|-------|----------|--------|
| Missing frontmatter | Error | Cannot create plan, log error |
| Missing task_id | Error | Cannot link to task, log error |
| Empty body | Error | Invalid plan, log error |
| Missing sections | Warning | Plan is valid but incomplete |

## Examples

### Minimal Plan

```markdown
---
task_id: bug-042
generated: 2026-02-12T14:30:00Z
---

# Plan: Fix mobile login button

## Objective
Fix login button that doesn't work on mobile browsers.

## Steps

### 1. Reproduce Bug
- Test on iOS Safari and Android Chrome
- Document exact behavior
- Check browser console for errors

### 2. Identify Root Cause
- Review login button code
- Check CSS for mobile-specific issues
- Test click event handlers

### 3. Implement Fix
- Apply fix to code
- Test on multiple mobile devices
- Deploy to production

## Resources
- Mobile test devices
- Browser developer tools

## Assumptions
- Bug is reproducible
- Fix can be deployed quickly
```

### Detailed Plan with All Sections

```markdown
---
task_id: feature-analytics
generated: 2026-02-12T15:00:00Z
status: draft
estimated_duration: 2 weeks
ai_model: claude-sonnet-4-5
---

# Plan: Build Analytics Dashboard

**Task**: feature-analytics.md
**Generated**: 2026-02-12 3:00 PM

## Objective

Build a comprehensive analytics dashboard that displays key metrics for user engagement, revenue, and system performance.

## Steps

### 1. Define Metrics and Requirements
**Actions**:
- Review Company_Handbook.md for business metrics
- Interview stakeholders for requirements
- Create metrics specification document

**Deliverable**: Metrics specification with data sources

**Duration**: 2 days

---

### 2. Design Dashboard UI
**Actions**:
- Sketch dashboard layout
- Choose visualization types (charts, tables, KPIs)
- Create mockups in design tool

**Deliverable**: Dashboard mockups approved by stakeholders

**Duration**: 3 days

---

### 3. Implement Data Pipeline
**Actions**:
- Set up data collection
- Create aggregation queries
- Build API endpoints for dashboard

**Deliverable**: Working API with test data

**Duration**: 4 days

---

### 4. Build Dashboard Frontend
**Actions**:
- Implement UI components
- Integrate with API
- Add interactivity (filters, date ranges)

**Deliverable**: Functional dashboard

**Duration**: 4 days

---

### 5. Test and Deploy
**Actions**:
- Test with real data
- Gather user feedback
- Deploy to production

**Deliverable**: Live analytics dashboard

**Duration**: 1 day

## Resources

### Required
- Design tool (Figma, Sketch)
- Frontend framework
- Charting library
- Database access

### Optional
- Analytics platform documentation
- Example dashboards from competitors

## Assumptions

1. Data sources are accessible and documented
2. Stakeholders available for requirements gathering
3. Design approval process takes <1 week
4. No major technical blockers

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data quality issues | Medium | High | Validate data sources early |
| Scope creep | High | Medium | Lock requirements after design phase |
| Performance problems | Low | High | Load test with production data |

## Success Criteria

- [ ] All required metrics displayed accurately
- [ ] Dashboard loads in <2 seconds
- [ ] Stakeholders approve design and functionality
- [ ] User feedback is positive (>80% satisfaction)
- [ ] No critical bugs in production

## Next Steps

1. Schedule kickoff meeting with stakeholders
2. Begin metrics definition phase
3. Set up project tracking
4. Mark task as in-progress
```

## Naming Conventions

### Pattern

`plan-{task-id}.md`

### Examples

- Task: `task-001.md` → Plan: `plan-task-001.md`
- Task: `bug-042.md` → Plan: `plan-bug-042.md`
- Task: `feature-analytics.md` → Plan: `plan-feature-analytics.md`

### Collision Handling

If task file has numeric suffix (e.g., `task-001-1.md`), plan follows:
- Task: `task-001-1.md` → Plan: `plan-task-001-1.md`

## Lifecycle

```
1. User triggers AI processing
2. AI reads task from /Needs_Action
3. AI reads Company_Handbook.md for context
4. AI generates structured plan
5. AI writes plan to /Plans/plan-{task-id}.md
6. Plan remains in /Plans (never moved)
7. User references plan during work
8. User marks task complete (plan stays for reference)
```

## Version History

- **1.0.0** (2026-02-12): Initial schema definition
