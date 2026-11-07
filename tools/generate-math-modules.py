#!/usr/bin/env python3
"""
Generate complete K-12 to postgraduate mathematics curriculum.
Uses progressive scaffolding and pattern templates to build 38 modules efficiently.
"""

import json
import os

# Base template that all modules follow
MODULE_TEMPLATE = {
    "schema_version": "1.0",
    "module": {
        "version": "1.0.0",
        "license": "CC BY 4.0",
        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Jonathan's Creative Archive Mathematics Curriculum",
        "last_reviewed": "2026-11-07",
        "review_status": "structure_defined_content_pending",
    }
}

# Define all 38 modules with metadata
MODULES = [
    # K-2
    {"id": "MOD-math-count-001", "grade": "K-2", "title": "Counting and Number Recognition (0-20)", "prereqs": [], "difficulty": "beginner"},
    {"id": "MOD-math-add-001", "grade": "K-2", "title": "Basic Addition and Subtraction", "prereqs": ["MOD-math-count-001"], "difficulty": "beginner"},
    {"id": "MOD-math-shape-001", "grade": "K-2", "title": "Shapes and Spatial Reasoning", "prereqs": [], "difficulty": "beginner"},
    {"id": "MOD-math-measure-001", "grade": "K-2", "title": "Measurement (length, weight, time)", "prereqs": ["MOD-math-count-001"], "difficulty": "beginner"},
    {"id": "MOD-math-pattern-001", "grade": "K-2", "title": "Patterns and Sorting", "prereqs": [], "difficulty": "beginner"},
    
    # 3-4
    {"id": "MOD-math-add-multi-001", "grade": "3-4", "title": "Multi-digit Addition and Subtraction", "prereqs": ["MOD-math-add-001"], "difficulty": "beginner"},
    {"id": "MOD-math-mult-intro-001", "grade": "3-4", "title": "Introduction to Multiplication", "prereqs": ["MOD-math-add-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-div-intro-001", "grade": "3-4", "title": "Introduction to Division", "prereqs": ["MOD-math-mult-intro-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-frac-simple-001", "grade": "3-4", "title": "Fractions (halves, thirds, quarters)", "prereqs": ["MOD-math-add-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-money-time-001", "grade": "3-4", "title": "Money and Time", "prereqs": ["MOD-math-count-001", "MOD-math-measure-001"], "difficulty": "beginner"},
    
    # 5-6
    {"id": "MOD-math-mult-master-001", "grade": "5-6", "title": "Multiplication and Division Mastery", "prereqs": ["MOD-math-mult-intro-001", "MOD-math-div-intro-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-frac-ops-001", "grade": "5-6", "title": "Fractions (operations, comparison)", "prereqs": ["MOD-math-frac-simple-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-decimal-001", "grade": "5-6", "title": "Decimals", "prereqs": ["MOD-math-frac-ops-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-ratio-percent-001", "grade": "5-6", "title": "Introduction to Ratios and Percentages", "prereqs": ["MOD-math-frac-ops-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-geom-basics-001", "grade": "5-6", "title": "Geometry (area, perimeter, volume)", "prereqs": ["MOD-math-shape-001", "MOD-math-measure-001"], "difficulty": "intermediate"},
    
    # 7-8
    {"id": "MOD-math-integers-001", "grade": "7-8", "title": "Integers and Rational Numbers", "prereqs": ["MOD-math-decimal-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-alg-expr-001", "grade": "7-8", "title": "Algebraic Expressions and Equations", "prereqs": ["MOD-math-integers-001"], "difficulty": "intermediate"},
    {"id": "MOD-math-linear-eq-001", "grade": "7-8", "title": "Linear Equations and Graphing", "prereqs": ["MOD-math-alg-expr-001"], "difficulty": "advanced"},
    {"id": "MOD-math-sys-eq-001", "grade": "7-8", "title": "Systems of Equations", "prereqs": ["MOD-math-linear-eq-001"], "difficulty": "advanced"},
    {"id": "MOD-math-prob-stat-001", "grade": "7-8", "title": "Probability and Statistics Basics", "prereqs": ["MOD-math-pattern-001"], "difficulty": "intermediate"},
    
    # 9-12 (High School)
    {"id": "MOD-math-quad-001", "grade": "9-12", "title": "Quadratic Equations and Functions", "prereqs": ["MOD-math-linear-eq-001"], "difficulty": "advanced"},
    {"id": "MOD-math-poly-001", "grade": "9-12", "title": "Polynomial Functions", "prereqs": ["MOD-math-quad-001"], "difficulty": "advanced"},
    {"id": "MOD-math-exp-log-001", "grade": "9-12", "title": "Exponential and Logarithmic Functions", "prereqs": ["MOD-math-poly-001"], "difficulty": "advanced"},
    {"id": "MOD-math-trig-001", "grade": "9-12", "title": "Trigonometry (unit circle, trig functions)", "prereqs": ["MOD-math-linear-eq-001"], "difficulty": "advanced"},
    {"id": "MOD-math-seq-series-001", "grade": "9-12", "title": "Sequences and Series", "prereqs": ["MOD-math-exp-log-001"], "difficulty": "advanced"},
    {"id": "MOD-math-comb-prob-001", "grade": "9-12", "title": "Combinatorics and Probability", "prereqs": ["MOD-math-prob-stat-001"], "difficulty": "advanced"},
    {"id": "MOD-math-stat-001", "grade": "9-12", "title": "Introductory Statistics", "prereqs": ["MOD-math-prob-stat-001"], "difficulty": "advanced"},
    {"id": "MOD-math-matrix-001", "grade": "9-12", "title": "Basic Matrices and Linear Systems", "prereqs": ["MOD-math-sys-eq-001"], "difficulty": "advanced"},
    
    # College/Postgraduate
    {"id": "MOD-math-calc1-001", "grade": "Undergrad", "title": "Calculus I (Limits, Derivatives, Applications)", "prereqs": ["MOD-math-poly-001"], "difficulty": "advanced"},
    {"id": "MOD-math-calc2-001", "grade": "Undergrad", "title": "Calculus II (Integration, Techniques, Series)", "prereqs": ["MOD-math-calc1-001"], "difficulty": "advanced"},
    {"id": "MOD-math-multicalc-001", "grade": "Undergrad", "title": "Multivariable Calculus", "prereqs": ["MOD-math-calc2-001"], "difficulty": "advanced"},
    {"id": "MOD-math-linalg-001", "grade": "Undergrad", "title": "Linear Algebra", "prereqs": ["MOD-math-matrix-001"], "difficulty": "advanced"},
    {"id": "MOD-math-diffeq-001", "grade": "Undergrad", "title": "Differential Equations", "prereqs": ["MOD-math-calc2-001"], "difficulty": "advanced"},
    {"id": "MOD-math-abstract-001", "grade": "Graduate", "title": "Abstract Algebra I (Groups, Rings, Fields)", "prereqs": ["MOD-math-linalg-001"], "difficulty": "expert"},
    {"id": "MOD-math-realanalysis-001", "grade": "Graduate", "title": "Real Analysis", "prereqs": ["MOD-math-calc2-001"], "difficulty": "expert"},
    {"id": "MOD-math-complex-001", "grade": "Graduate", "title": "Complex Analysis", "prereqs": ["MOD-math-calc2-001"], "difficulty": "expert"},
    {"id": "MOD-math-topology-001", "grade": "Graduate", "title": "Topology", "prereqs": ["MOD-math-realanalysis-001"], "difficulty": "expert"},
    {"id": "MOD-math-numtheory-001", "grade": "Graduate", "title": "Number Theory", "prereqs": ["MOD-math-abstract-001"], "difficulty": "expert"},
]

def create_module_skeleton(mod_def):
    """Create a complete module skeleton with all required fields."""
    mod = json.loads(json.dumps(MODULE_TEMPLATE))  # Deep copy
    
    mod["module"]["id"] = mod_def["id"]
    mod["module"]["title"] = mod_def["title"]
    mod["module"]["grade_level"] = mod_def["grade"]
    mod["module"]["expected_level"] = mod_def["difficulty"]
    
    # Learning objectives (5 generic + subject-specific)
    mod["module"]["learning_objectives"] = [
        f"Understand the core concepts of {mod_def['title'].split('(')[0].strip()}",
        "Apply this knowledge to solve real-world problems",
        "Communicate mathematical reasoning clearly",
        "Connect this topic to other mathematical areas",
        "Build confidence and fluency with this skill"
    ]
    
    # Prerequisites
    mod["module"]["prerequisites"] = [
        {"id": p, "title": f"See {p}"} for p in mod_def.get("prereqs", [])
    ]
    
    # Time estimate based on level
    time_map = {"beginner": 30, "intermediate": 45, "advanced": 60, "expert": 90}
    mod["module"]["time_estimate_minutes"] = time_map.get(mod_def["difficulty"], 45)
    
    # Content structure
    mod["module"]["content"] = {
        "introduction": {
            "plain_text": f"# {mod_def['title']}\n\nThis module teaches the foundations and applications of {mod_def['title'].lower()}.",
            "estimated_reading_minutes": 3
        },
        "core_lesson": {
            "sections": [
                {
                    "title": f"Section 1: Foundations of {mod_def['title']}",
                    "content": f"[Complete lesson content for {mod_def['title']} will be added here with explanations, definitions, and visual descriptions]",
                    "estimated_reading_minutes": 15,
                    "key_terms": []
                },
                {
                    "title": f"Section 2: Applications and Problem-Solving",
                    "content": f"[Application section showing how {mod_def['title']} is used in real contexts]",
                    "estimated_reading_minutes": 15,
                    "key_terms": []
                }
            ]
        },
        "worked_examples": [
            {
                "id": f"{mod_def['id']}-EX-{i}",
                "title": f"Example {i}: {['Basic scenario', 'Intermediate application', 'Advanced case'][i-1]}",
                "difficulty": ["beginner", "intermediate", "advanced"][i-1],
                "scenario": f"[Scenario {i} for {mod_def['title']}]",
                "parameters": {},
                "prediction": "[Student prediction]",
                "step_by_step": ["[Step 1]", "[Step 2]", "[Step 3]"],
                "explanation": f"[Explanation of {mod_def['title']} concept]",
                "mathematical_form": f"[Mathematical notation for concept]"
            }
            for i in range(1, 4)
        ],
        "exercises": [
            {
                "id": f"{mod_def['id']}-EXER-{i}",
                "title": f"Exercise {i}",
                "difficulty": ["beginner", "intermediate", "advanced"][i % 3],
                "problem_statement": f"[Problem statement for exercise {i}]",
                "hint": "[Hint for solving]",
                "solution": "[Complete solution]",
                "answer": "[Final answer]"
            }
            for i in range(1, 6)
        ],
        "interactive_experience": "[Link to interactive HTML lab if applicable]",
        "text_only_path": "[Complete text-only version of lesson]"
    }
    
    # Sources and licensing
    mod["module"]["sources"] = [
        {"title": "OpenStax Mathematics Textbooks", "url": "https://openstax.org/"},
        {"title": "Khan Academy", "url": "https://www.khanacademy.org/"},
        {"title": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/"}
    ]
    
    mod["module"]["content_status"] = "structure_complete_content_pending"
    
    return mod

def main():
    """Generate all 38 math modules."""
    modules_list = []
    
    for mod_def in MODULES:
        mod = create_module_skeleton(mod_def)
        modules_list.append(mod)
    
    # Write to file
    output_path = "/root/archive/data/modules-math-curriculum.json"
    with open(output_path, "w") as f:
        json.dump({"modules": modules_list, "total_count": len(modules_list)}, f, indent=2)
    
    print(f"✓ Generated {len(modules_list)} mathematics modules")
    print(f"✓ Output: {output_path}")
    print(f"✓ Status: All modules have structure; content pending")
    print(f"✓ Each module has:")
    print(f"  - Learning objectives (5)")
    print(f"  - Prerequisites linked")
    print(f"  - Core lesson sections (2)")
    print(f"  - Worked examples (3)")
    print(f"  - Exercises (5)")
    print(f"  - Source citations")
    print(f"  - License (CC BY 4.0)")

if __name__ == "__main__":
    main()
