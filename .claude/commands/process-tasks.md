# Process Tasks

Process all task files from the Needs_Action folder and generate structured plans.

## Command Description

This command reads task files from the `/Needs_Action` folder, interprets their content using `Company_Handbook.md` as context, and generates detailed action plans in the `/Plans` folder.

## Workflow

1. **Read Configuration**: Get vault path from environment or config
2. **Read Company Handbook**: Load `Company_Handbook.md` for context (optional)
3. **Read Task Files**: Get all `.md` files from `/Needs_Action`
4. **Process Each Task**:
   - Parse task content and frontmatter
   - Generate structured plan with steps, resources, and assumptions
   - Write plan to `/Plans/plan-{task-id}.md`
   - Log any errors to `errors.md`
5. **Update Dashboard**: Update task counts and recent activity

## Implementation

Read all markdown files from the Needs_Action folder:

```python
from pathlib import Path
import os

vault_path = Path(os.getenv("AI_EMPLOYEE_VAULT", ""))
needs_action_dir = vault_path / "Needs_Action"
task_files = list(needs_action_dir.glob("*.md"))
```

Read Company_Handbook.md for context (if exists):

```python
handbook_path = vault_path / "Company_Handbook.md"
handbook_content = ""

if handbook_path.exists():
    handbook_content = handbook_path.read_text(encoding="utf-8")
else:
    # Log warning but continue processing
    error_msg = f"## {datetime.now().isoformat()} - Missing Reference\n\n"
    error_msg += "Company_Handbook.md not found in vault root.\n"
    error_msg += "AI will process tasks without handbook context.\n\n"
    (vault_path / "errors.md").open('a').write(error_msg)
```

For each task file, generate a structured plan:

**Plan Generation Instructions**:

You are generating an action plan for a task. The plan must follow this structure:

```markdown
---
task_id: {task-id}
generated: {ISO 8601 timestamp}
status: draft
estimated_duration: {human-readable estimate}
ai_model: claude-sonnet-4-5
---

# Plan: {Task Title}

**Task**: {task-filename}
**Generated**: {human-readable timestamp}

## Objective

{Clear statement of what the plan achieves - 1-2 sentences}

## Steps

### 1. {Step Title}

**Actions**:
- {Specific action 1}
- {Specific action 2}
- {Specific action 3}

**Deliverable**: {What this step produces}

**Duration**: {Time estimate}

---

### 2. {Step Title}

**Actions**:
- {Specific action 1}
- {Specific action 2}

**Deliverable**: {What this step produces}

**Duration**: {Time estimate}

---

{Additional steps as needed}

## Resources

### Required
- {Required resource 1}
- {Required resource 2}

### Optional
- {Optional resource 1}

## Assumptions

1. {Assumption 1}
2. {Assumption 2}
3. {Assumption 3}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Risk 1} | {Low/Medium/High} | {Low/Medium/High} | {How to handle} |

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Next Steps

1. {Next step 1}
2. {Next step 2}
3. Mark task as complete in AI Employee system
```

**Context to use**:
- Task content: {task_file_content}
- Company Handbook: {handbook_content if available}

**Requirements**:
- Break down the task into 3-7 actionable steps
- Each step should have clear actions and deliverables
- Include time estimates for each step
- Reference Company Handbook sections when relevant
- Identify assumptions and risks
- Provide concrete success criteria

Write the plan to `/Plans/plan-{task-id}.md` where `{task-id}` is the task filename without extension.

**Error Handling**:

If task file is empty or contains only whitespace:
```python
error_msg = f"## {datetime.now().isoformat()} - Validation Error\n\n"
error_msg += f"Task file {task_file.name} is empty or contains only whitespace.\n"
error_msg += "Action: Add task description and reprocess.\n\n"
(vault_path / "errors.md").open('a').write(error_msg)
# Skip this task and continue with next
continue
```

If task file has malformed markdown (invalid frontmatter):
```python
error_msg = f"## {datetime.now().isoformat()} - Validation Error\n\n"
error_msg += f"Task file {task_file.name} has malformed YAML frontmatter.\n"
error_msg += "Action: Fix YAML syntax or remove frontmatter.\n\n"
(vault_path / "errors.md").open('a').write(error_msg)
# Process body only, ignore frontmatter
```

**Sequential Processing**:

Process tasks one at a time in the order they appear in the directory. Do not process tasks in parallel.

```python
for task_file in sorted(task_files):
    # Process this task
    # Generate plan
    # Write plan file
    # Continue to next task
```

**Dashboard Update** (after all tasks processed):

After generating all plans, update Dashboard.md with:
- Current task counts (count .md files in each folder)
- Recent activity entry for plan generation
- Timestamp of last update

See `.claude/commands/complete-task.md` for Dashboard update logic (will be integrated in T036).

## Usage

```bash
# Process all tasks in Needs_Action
claude process-tasks

# The command will:
# 1. Read all task files from /Needs_Action
# 2. Generate a plan for each task
# 3. Write plans to /Plans
# 4. Update Dashboard.md
# 5. Log any errors to errors.md
```

## Expected Output

For each task processed:
- Plan file created in `/Plans/plan-{task-id}.md`
- Console output: "✓ Generated plan for {task-filename}"

If errors occur:
- Error logged to `errors.md`
- Console output: "✗ Failed to process {task-filename} (see errors.md)"

## Notes

- This is a manual trigger command (user must run it)
- No autonomous processing or background loops
- All state changes visible through file system
- Errors logged to errors.md for transparency
