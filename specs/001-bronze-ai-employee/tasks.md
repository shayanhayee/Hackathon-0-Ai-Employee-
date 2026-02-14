# Tasks: Bronze Tier AI Employee

**Input**: Design documents from `/specs/001-bronze-ai-employee/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: No automated tests requested - Bronze Tier uses manual validation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Watcher component**: `watcher/` directory at repository root
- **Vault structure**: User-managed vault (configured in watcher/config.py)
- **Claude commands**: `.claude/commands/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create watcher directory structure at repository root
- [x] T002 Create .claude/commands directory for Claude CLI commands
- [x] T003 Create Python requirements.txt in watcher/requirements.txt with watchdog>=3.0.0 and PyYAML>=6.0

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create watcher/config.py with vault path configuration and folder name constants
- [x] T005 [P] Create vault initialization script to create folder structure (Inbox, Needs_Action, Plans, Done)
- [x] T006 [P] Create watcher/file_handler.py with file copy utility function using pathlib
- [x] T007 Implement collision detection logic in watcher/file_handler.py (numeric suffix for duplicates)
- [x] T008 Implement error logging utility in watcher/file_handler.py (append to errors.md)
- [x] T009 Create vault boundary validation function in watcher/file_handler.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Intake via File Drop (Priority: P1) 🎯 MVP

**Goal**: Implement file system watcher that monitors /Inbox and copies files to /Needs_Action within 5 seconds

**Independent Test**: Create a file in /Inbox and verify it appears in /Needs_Action within 5 seconds

### Implementation for User Story 1

- [x] T010 [P] [US1] Install Python dependencies by running pip install -r watcher/requirements.txt
- [x] T011 [P] [US1] Create watcher/watcher.py with main script structure and imports
- [x] T012 [US1] Implement FileSystemEventHandler subclass in watcher/watcher.py for file creation events
- [x] T013 [US1] Add file extension filter (.md only) in watcher/watcher.py event handler
- [x] T014 [US1] Integrate file_handler.copy_file() in watcher/watcher.py on_created event
- [x] T015 [US1] Add console logging for file detection and copy operations in watcher/watcher.py
- [x] T016 [US1] Implement Observer setup and start logic in watcher/watcher.py main function
- [x] T017 [US1] Add graceful shutdown handling (Ctrl+C) in watcher/watcher.py
- [x] T018 [US1] Add startup validation (check vault path exists, folders exist) in watcher/watcher.py

**Checkpoint**: At this point, User Story 1 should be fully functional - watcher detects files and copies to /Needs_Action

**Manual Validation**:
1. Start watcher: `python watcher/watcher.py`
2. Create test file: `echo "# Test task" > vault/Inbox/test-001.md`
3. Verify file appears in vault/Needs_Action/ within 5 seconds
4. Test collision: Create another test-001.md, verify test-001-1.md created
5. Test empty file: Create empty file, verify it's still copied

---

## Phase 4: User Story 2 - AI Task Planning (Priority: P2)

**Goal**: Implement Claude CLI commands to process tasks from /Needs_Action and generate plans in /Plans

**Independent Test**: Place a task file in /Needs_Action, run Claude CLI command, verify plan file appears in /Plans

### Implementation for User Story 2

- [x] T019 [P] [US2] Create .claude/commands/process-tasks.md with command structure and metadata
- [x] T020 [US2] Write task processing workflow in .claude/commands/process-tasks.md (read /Needs_Action files)
- [x] T021 [US2] Add Company_Handbook.md reading logic to .claude/commands/process-tasks.md
- [x] T022 [US2] Define plan generation instructions in .claude/commands/process-tasks.md (structured format per contracts/plan-file.schema.md)
- [x] T023 [US2] Add plan file writing logic to .claude/commands/process-tasks.md (write to /Plans with naming convention)
- [x] T024 [US2] Add error handling for malformed markdown in .claude/commands/process-tasks.md (log to errors.md)
- [x] T025 [US2] Add error handling for empty task files in .claude/commands/process-tasks.md
- [x] T026 [US2] Add error handling for missing Company_Handbook.md in .claude/commands/process-tasks.md (warning only)
- [x] T027 [US2] Add sequential processing logic for multiple tasks in .claude/commands/process-tasks.md

**Checkpoint**: At this point, User Story 2 should be fully functional - Claude can process tasks and generate plans

**Manual Validation**:
1. Create sample task: `echo "# Research pricing\nAnalyze competitor pricing." > vault/Needs_Action/task-001.md`
2. Create Company_Handbook.md with sample content
3. Run: `claude process-tasks`
4. Verify plan-task-001.md appears in vault/Plans/
5. Verify plan has structured format (Objective, Steps, Resources, Assumptions)
6. Test error handling: Create empty task file, verify error logged to errors.md

---

## Phase 5: User Story 3 - Task Completion and Dashboard Updates (Priority: P3)

**Goal**: Implement task completion command and Dashboard.md updates

**Independent Test**: Mark a task complete via CLI command, verify file moved to /Done and Dashboard.md updated

### Implementation for User Story 3

- [x] T028 [P] [US3] Create .claude/commands/complete-task.md with command structure and metadata
- [x] T029 [US3] Write task completion workflow in .claude/commands/complete-task.md (move file from /Needs_Action to /Done)
- [x] T030 [US3] Add file existence validation in .claude/commands/complete-task.md
- [x] T031 [US3] Add Dashboard.md creation logic in .claude/commands/complete-task.md (if doesn't exist)
- [x] T032 [US3] Implement folder counting logic in .claude/commands/complete-task.md (count .md files in each folder)
- [x] T033 [US3] Implement Dashboard.md update logic in .claude/commands/complete-task.md (task counts table)
- [x] T034 [US3] Add activity logging to Dashboard.md in .claude/commands/complete-task.md (recent activity section)
- [x] T035 [US3] Add timestamp generation (ISO 8601) in .claude/commands/complete-task.md
- [x] T036 [US3] Integrate Dashboard update into process-tasks.md command (update after plan generation)

**Checkpoint**: All user stories should now be independently functional

**Manual Validation**:
1. Complete a task: `claude complete-task task-001`
2. Verify task-001.md moved from /Needs_Action to /Done
3. Verify Dashboard.md created/updated with correct counts
4. Verify recent activity logged in Dashboard.md
5. Process another task, verify Dashboard updates again
6. Test with missing Dashboard.md (delete it), verify recreated

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Create sample Company_Handbook.md template in vault root
- [x] T038 [P] Create sample task template in vault/Templates/ directory (optional)
- [x] T039 Add vault path validation on watcher startup (check absolute path, exists, writable)
- [x] T040 Add concurrent execution prevention in .claude/commands/process-tasks.md (check lock file)
- [x] T041 [P] Create README.md in watcher/ directory with setup and usage instructions
- [x] T042 [P] Add example task files in vault/Inbox/ for testing (optional)
- [x] T043 Test end-to-end workflow: file drop → watcher copy → process → complete → dashboard
- [x] T044 Verify all error cases logged to errors.md with timestamps
- [x] T045 Verify Dashboard.md format matches contracts/dashboard.schema.md
- [x] T046 Run quickstart.md validation (follow setup steps, verify all work)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US2 (Phase 4): Can start after Foundational - No dependencies on US1 (can test independently)
  - US3 (Phase 5): Can start after Foundational - No dependencies on US1/US2 (can test independently)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Fully independent
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Fully independent (doesn't require watcher)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Fully independent (doesn't require watcher or processing)

### Within Each User Story

**User Story 1 (Watcher)**:
- T010-T011 can run in parallel (install deps, create main file)
- T012-T018 must run sequentially (build watcher logic step by step)

**User Story 2 (AI Processing)**:
- T019-T027 can be done sequentially (build command file incrementally)
- Each task adds a section to the command file

**User Story 3 (Completion & Dashboard)**:
- T028-T035 build complete-task.md sequentially
- T036 integrates dashboard into process-tasks.md (depends on T033)

### Parallel Opportunities

- All Setup tasks (T001-T003) can run in parallel
- Foundational tasks T005, T006 can run in parallel (different files)
- Once Foundational completes, all three user stories can start in parallel (if team capacity allows)
- Within US1: T010-T011 can run in parallel
- Polish tasks T037, T038, T041, T042 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch foundational tasks in parallel:
Task T005: "Create vault initialization script"
Task T006: "Create watcher/file_handler.py with file copy utility"

# Launch US1 setup tasks in parallel:
Task T010: "Install Python dependencies"
Task T011: "Create watcher/watcher.py with main script structure"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T009) - CRITICAL
3. Complete Phase 3: User Story 1 (T010-T018)
4. **STOP and VALIDATE**: Test watcher independently
5. Deploy/demo if ready

**MVP Deliverable**: Working file watcher that copies tasks from /Inbox to /Needs_Action

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (AI processing added)
4. Add User Story 3 → Test independently → Deploy/Demo (Full system complete)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done:
   - Developer A: User Story 1 (T010-T018) - Watcher
   - Developer B: User Story 2 (T019-T027) - AI Processing
   - Developer C: User Story 3 (T028-T036) - Completion & Dashboard
3. Stories complete and integrate independently
4. Team collaborates on Phase 6: Polish (T037-T046)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No automated tests - Bronze Tier uses manual validation per constitution
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 3 tasks
- **Phase 2 (Foundational)**: 6 tasks
- **Phase 3 (US1 - Watcher)**: 9 tasks
- **Phase 4 (US2 - AI Processing)**: 9 tasks
- **Phase 5 (US3 - Completion)**: 9 tasks
- **Phase 6 (Polish)**: 10 tasks

**Total**: 46 tasks

**Parallel Opportunities**: 8 tasks can run in parallel (marked with [P])

**MVP Scope**: Phases 1-3 (18 tasks) delivers working file watcher

**Full System**: Phases 1-5 (36 tasks) delivers all three user stories

**Production Ready**: All phases (46 tasks) includes polish and validation
