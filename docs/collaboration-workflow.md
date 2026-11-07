# Human–AI Collaboration Workflow v1.0

A local-first, portable workflow for defining projects, tasks, and contributors in the Knowledge Commons.

## Overview

This system enables:
1. **Projects**: Define a problem, affected community, purpose, and status
2. **Tasks**: Describe bounded work with clear acceptance criteria and permissions
3. **Contributors**: Register capabilities and availability (optional)
4. **Handoff Packets**: Export a task with full context for another person or AI
5. **Review Records**: Document what was delivered and the decision

All records are plain JSON, validatable offline, and can be exchanged via git, email, or simple file systems.

## Project Record

```json
{
  "project_id": "PROJ-motion-trace-shape",
  "version": "1.0.0",
  "type": "educational_pathway",
  "title": "Motion → Trace → Shape: A Foundational Lesson in Lissajous Curves",
  "purpose": "Create a beginner-friendly, offline-capable learning pathway for understanding how two oscillating motions combine to form predictable geometric shapes.",
  
  "affected_communities": [
    {
      "community_name": "Students (ages 12+) exploring mathematics and physics",
      "involvement_in_design": "Not yet directly involved; feedback from real learners pending",
      "accessibility_needs": "Keyboard navigation, reduced-motion support, text-based access, screen-reader compatibility"
    },
    {
      "community_name": "Educators in informal settings (museums, community centers)",
      "involvement_in_design": "Not yet directly involved; practical deployment feedback pending",
      "accessibility_needs": "Offline availability, easy setup, clear learning objectives, adaptable materials"
    }
  ],
  
  "problem_statement": "Many learners struggle to visualize how two independent oscillating motions combine. Static diagrams are insufficient; animated visuals require internet and devices. There is a need for a portable, inclusive, offline-capable introduction to Lissajous curves.",
  
  "related_work": [
    {
      "title": "Reality Atlas Appearance",
      "url": "tools/reality-atlas/README.md",
      "relationship": "Addresses visualization of motion and geometry at different scales; complements this lesson"
    },
    {
      "title": "Lumen Commons",
      "url": "tools/lumen-commons/README.md",
      "relationship": "Experimental browser adventure with scientific scaffolding; similar audience but different scope"
    }
  ],
  
  "status": "first_pathway_complete_validation_pending",
  "status_date": "2026-11-07",
  
  "current_state": {
    "completed": [
      "Interactive HTML lab with three presets (line, circle, figure-eight)",
      "18 numerical tests and 14 UI tests passed",
      "Three worked examples and five exercises with solutions",
      "Knowledge module schema and documentation",
      "Offline capability confirmed"
    ],
    "unverified": [
      "Real-browser rendering and download behavior",
      "Mobile and touch interaction",
      "Screen-reader and assistive-technology compatibility",
      "Actual learner feedback on comprehension or engagement"
    ],
    "not_included": [
      "Multiplayer or networked features",
      "Real-time tutoring or AI-graded essays",
      "Adaptation based on learner performance",
      "Integration with learning management systems"
    ]
  },
  
  "license": "CC BY 4.0",
  "contributors": [
    {
      "role": "original_design",
      "attribution": "Jonathan's Creative Archive, 2026"
    }
  ],
  
  "governance": {
    "decision_maker": "Jonathan (project owner)",
    "review_required": "yes",
    "review_criteria": [
      "All acceptance criteria for tasks are met",
      "No new security or privacy risks introduced",
      "Licenses are preserved and correctly attributed",
      "Scientific claims are separated from speculation"
    ]
  },
  
  "resources": {
    "maintainer": "Archive Contributors (volunteer)",
    "hosting": "GitHub (github.com/jonjonjon11/jonathan-creative-archive)",
    "storage": "Static files; no databases, accounts, or persistent services required",
    "budget": "None; all tools and libraries are open-source or built from standard library"
  },
  
  "next_milestones": [
    {
      "name": "Real-device and assistive-technology validation",
      "description": "Test the interactive lab on actual browsers, mobile devices, and screen readers. Document findings.",
      "tasks_required": ["TASK-motion-browser-test", "TASK-motion-a11y-test"],
      "timeline": "Q1 2027 (proposed)"
    },
    {
      "name": "Learner feedback and iteration",
      "description": "Gather feedback from actual learners (students or educators). Identify comprehension barriers and iterate on explanations.",
      "tasks_required": ["TASK-motion-learner-study"],
      "timeline": "Q1 2027 (proposed)"
    },
    {
      "name": "Expand to a second foundational pathway",
      "description": "Once this pathway is validated, create a second pathway (e.g., 'Forces and Motion' or 'Waves and Light') using the same module schema and workflow.",
      "tasks_required": ["TASK-select-next-pathway"],
      "timeline": "Q2 2027 (proposed)"
    }
  ]
}
```

## Task Record

```json
{
  "task_id": "TASK-motion-browser-test",
  "version": "1.0.0",
  "project_id": "PROJ-motion-trace-shape",
  "type": "validation_and_testing",
  "title": "Browser rendering and interaction test for Motion → Trace → Shape",
  
  "objective": "Verify that the Motion → Trace → Shape HTML application renders correctly and all interactive controls work as designed across a range of modern browsers and devices.",
  
  "scope": [
    "Test the standalone HTML file (Motion-Trace-Shape.html)",
    "Verify rendering of the layout, graphs, and visual elements",
    "Test all interactive controls: Play, Pause, Step, time slider, parameter selectors",
    "Test JSON download functionality",
    "Document browser versions and device types tested",
    "Identify any rendering issues or broken interactions"
  ],
  
  "restrictions": [
    "Do not modify the HTML or JavaScript code",
    "Do not connect to external services or upload any files to third-party sites",
    "Do not attempt to modify or reverse-engineer compiled assets"
  ],
  
  "inputs": [
    {
      "name": "Motion-Trace-Shape.html",
      "source": "tools/motion-trace-shape/Motion-Trace-Shape.html",
      "how_to_access": "Download from GitHub or clone the repository"
    },
    {
      "name": "Validation template",
      "source": "docs/task-templates/browser-test-template.md",
      "how_to_access": "Included in this repository"
    }
  ],
  
  "deliverables": [
    {
      "name": "Browser test report",
      "format": "Markdown or plain text",
      "required_content": [
        "Browser name and version",
        "Device type (desktop/mobile/tablet)",
        "Operating system",
        "Screen resolution (if available)",
        "All interactive controls tested (yes/no for each)",
        "Any visual rendering issues observed",
        "Any functional issues (controls not responding, data not saving)",
        "Overall assessment (works/partial/does not work)",
        "Recommendations for improvement (if any)"
      ],
      "acceptance_criteria": [
        "Report covers at least two browser/OS combinations",
        "All controls listed in the report",
        "Issues are described specifically (e.g., 'Play button does not start animation on Safari 15.2')",
        "Report is dated and signed by the tester"
      ]
    },
    {
      "name": "Screenshots (optional but helpful)",
      "format": "PNG or JPEG",
      "required_content": [
        "Screenshot of the app in each tested browser (if possible)",
        "Close-ups of any areas with rendering issues"
      ]
    }
  ],
  
  "acceptance_criteria": [
    "The report covers at least two different browser/OS combinations",
    "All interactive controls are documented as tested",
    "Any issues found are described specifically with steps to reproduce",
    "The report is clear, organized, and suitable for sharing with developers",
    "No critical security or data leaks are noted"
  ],
  
  "beneficiaries": [
    {
      "name": "Learners",
      "impact": "Ensures a consistent, working experience across devices"
    },
    {
      "name": "Educators",
      "impact": "Confidence that the tool will work in classrooms and community settings"
    },
    {
      "name": "Developers",
      "impact": "Real-world testing feedback to guide bug fixes and improvements"
    }
  ],
  
  "time_estimate_hours": 4,
  "difficulty": "beginner",
  
  "required_skills": [
    "Browser navigation and basic troubleshooting",
    "Ability to identify and describe what works and what doesn't",
    "Attention to detail (exact browser versions, reproducible steps)"
  ],
  
  "required_permissions": [
    "Read access to the GitHub repository",
    "Ability to download files from GitHub",
    "Access to at least two different browsers or devices"
  ],
  
  "stop_conditions": [
    "If the HTML file is corrupted or inaccessible",
    "If you do not have access to at least two different browsers",
    "If testing requires payment or account creation"
  ],
  
  "resources_available": [
    {
      "type": "template",
      "name": "Browser test report template",
      "path": "docs/task-templates/browser-test-template.md"
    },
    {
      "type": "reference",
      "name": "Motion → Trace → Shape README",
      "path": "tools/motion-trace-shape/README.md"
    }
  ],
  
  "how_to_start": "1. Clone or download the repository. 2. Navigate to tools/motion-trace-shape/. 3. Download Motion-Trace-Shape.html. 4. Open it in your first browser. 5. Use the browser test template to document what works. 6. Repeat in at least one other browser. 7. Submit the report.",
  
  "how_to_submit": "Create a new Markdown file in docs/test-reports/ with the name browser-test-[your-name]-[date].md. Include the test report and any screenshots. Open a pull request or contact @jonjonjon11 directly.",
  
  "related_tasks": [],
  
  "depends_on": [],
  
  "priority": "high",
  "status": "open",
  "created_date": "2026-11-07",
  "created_by": "Archive Contributors"
}
```

## Contributor Registration (Optional)

```json
{
  "contributor_id": "CONTRIB-you",
  "name": "Your name or pseudonym (optional)",
  "email": "optional@example.com",
  "github_username": "optional_github_handle",
  
  "capabilities": [
    {
      "skill": "browser testing",
      "level": "intermediate",
      "tools": ["Firefox", "Chrome", "Safari"],
      "years_of_experience": 2
    },
    {
      "skill": "scientific writing",
      "level": "beginner",
      "tools": ["Markdown"],
      "years_of_experience": 1
    }
  ],
  
  "availability": {
    "hours_per_week": 5,
    "availability_window": "Evenings and weekends (UTC-5)",
    "can_pair_or_mentor": true
  },
  
  "interests": [
    "Education and learning design",
    "Accessibility",
    "Open-source collaboration"
  ],
  
  "privacy_preferences": {
    "public_attribution": true,
    "share_email_with_other_contributors": false,
    "opt_in_to_newsletter": false
  },
  
  "past_contributions": [
    {
      "project": "PROJ-motion-trace-shape",
      "task": "TASK-motion-browser-test",
      "status": "completed",
      "date": "2026-11-15"
    }
  ]
}
```

## Handoff Packet (Export Format)

When a task is ready for work, export this packet:

```json
{
  "packet_id": "PKT-motion-browser-test-001",
  "packet_date": "2026-11-07",
  "created_by": "Archive Contributors",
  
  "project_summary": {
    "id": "PROJ-motion-trace-shape",
    "title": "Motion → Trace → Shape: A Foundational Lesson in Lissajous Curves",
    "purpose": "Create a beginner-friendly, offline-capable learning pathway..."
  },
  
  "task": {
    "id": "TASK-motion-browser-test",
    "title": "Browser rendering and interaction test",
    "objective": "Verify that the Motion → Trace → Shape HTML application renders correctly...",
    "scope": ["Test rendering", "Test all controls", "Document findings"],
    "time_estimate_hours": 4,
    "difficulty": "beginner"
  },
  
  "deliverables": [
    {
      "name": "Browser test report",
      "format": "Markdown or plain text",
      "required_content": ["Browser/version", "Device type", "All controls tested", "Issues", "Assessment"]
    }
  ],
  
  "acceptance_criteria": [
    "Report covers at least two browser/OS combinations",
    "All controls are documented",
    "Issues are described specifically"
  ],
  
  "resources": {
    "html_file": "tools/motion-trace-shape/Motion-Trace-Shape.html",
    "readme": "tools/motion-trace-shape/README.md",
    "test_template": "docs/task-templates/browser-test-template.md"
  },
  
  "context": {
    "why_this_matters": "Ensures the interactive lesson works across devices and browsers",
    "background": "Motion → Trace → Shape is a new interactive lesson in JavaScript and SVG. Previous testing was limited to Node tests; real-browser rendering was blocked by environment constraints. This task provides that feedback.",
    "known_limitations": "The lab has not been tested on mobile devices, with screen readers, or on older browsers. Testing in at least two different browser/OS combinations would significantly improve confidence in the tool."
  },
  
  "review_and_approval": {
    "reviewer_name": "Jonathan (project owner)",
    "review_criteria": [
      "Report is clear and detailed",
      "All major browsers and OS combinations are covered",
      "Issues are specific and reproducible"
    ],
    "expected_review_time_days": 5,
    "how_to_contact": "@jonjonjon11 on GitHub or via issue comment"
  },
  
  "next_steps": [
    "Reviewer evaluates the test report",
    "If issues found: they are categorized as bugs or enhancements",
    "If no critical issues: the task is marked complete",
    "The next task (e.g., accessibility testing) can then begin"
  ]
}
```

## Review Record

After a task is completed, record the decision:

```json
{
  "review_id": "REV-motion-browser-test-001",
  "task_id": "TASK-motion-browser-test",
  "task_title": "Browser rendering and interaction test",
  "review_date": "2026-11-15",
  
  "submitted_by": "Test contributor name",
  "reviewer": "Jonathan",
  
  "deliverable_received": "browser-test-[name]-[date].md",
  "deliverable_summary": "Tested on Firefox 122, Chrome 130, Safari 17.1 on macOS 14.1 and Windows 11. All controls rendered and responded correctly. One minor issue: time slider thumb is slightly cut off on Safari at 100% zoom.",
  
  "acceptance_decision": "approved_with_minor_note",
  
  "notes": "Excellent, thorough testing. The Safari issue is minor and affects only the visual polish, not functionality. This is a known Safari rendering quirk with range inputs; no code change needed.",
  
  "recommended_next_steps": [
    "Mark task as complete",
    "Move to the next priority task (mobile device testing or accessibility testing)"
  ],
  
  "follow_up_tasks": [
    {
      "task_id": "TASK-motion-a11y-test",
      "title": "Accessibility and screen-reader testing",
      "rationale": "Now that browser rendering is confirmed, we can validate that screen-reader users can navigate and understand the lab"
    }
  ]
}
```

## Validation Script

```python
#!/usr/bin/env python3
"""
Validate project, task, and contributor records against the schema.
Runs offline; no external services required.
"""

import json
import sys
from pathlib import Path

def validate_project(project_file):
    """Validate a project record."""
    with open(project_file) as f:
        project = json.load(f)
    
    required_fields = [
        "project_id", "version", "title", "purpose",
        "affected_communities", "status", "license", "governance"
    ]
    
    errors = []
    for field in required_fields:
        if field not in project:
            errors.append(f"Missing required field: {field}")
    
    if project.get("status") not in [
        "planning", "in_progress", "first_pathway_complete_validation_pending",
        "complete", "paused", "archived"
    ]:
        errors.append(f"Invalid status: {project.get('status')}")
    
    return errors

def validate_task(task_file):
    """Validate a task record."""
    with open(task_file) as f:
        task = json.load(f)
    
    required_fields = [
        "task_id", "project_id", "title", "objective",
        "scope", "deliverables", "acceptance_criteria"
    ]
    
    errors = []
    for field in required_fields:
        if field not in task:
            errors.append(f"Missing required field: {field}")
    
    if task.get("status") not in [
        "open", "in_progress", "pending_review", "approved", "blocked", "cancelled"
    ]:
        errors.append(f"Invalid status: {task.get('status')}")
    
    if not task.get("time_estimate_hours"):
        errors.append("Missing time estimate in hours")
    
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_workflow.py <project|task> <file.json>")
        sys.exit(1)
    
    record_type = sys.argv[1]
    file_path = sys.argv[2]
    
    if record_type == "project":
        errors = validate_project(file_path)
    elif record_type == "task":
        errors = validate_task(file_path)
    else:
        print(f"Unknown record type: {record_type}")
        sys.exit(1)
    
    if errors:
        print(f"Validation failed for {file_path}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✓ {file_path} is valid")
        sys.exit(0)
```

## Workflow Summary

1. **Define a Project**: Create a project record with clear purpose, affected communities, and current status.
2. **Create Tasks**: Break the project into bounded tasks with clear deliverables and acceptance criteria.
3. **Register Contributors** (optional): Document skills, availability, and privacy preferences.
4. **Export a Handoff Packet**: When a task is ready, export it with all context needed by another person or AI.
5. **Complete and Submit**: Deliver the agreed-upon deliverables.
6. **Review and Record**: The reviewer documents their decision and next steps.
7. **Learn and Iterate**: Use the review record to improve future task design.

This workflow respects:
- **Autonomy**: Contributors choose which tasks to work on
- **Transparency**: All decisions and criteria are documented
- **Accountability**: Every task has an explicit reviewer and acceptance criteria
- **Accessibility**: No APIs, accounts, or background services required
