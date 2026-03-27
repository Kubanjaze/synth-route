# Phase 65 — Claude Generating Synthesis Route from Scaffold
**Version:** 1.0 | **Date:** 2026-03-27
## Goal
Ask Claude to propose a 3-step synthesis route for a given scaffold, return as structured JSON.
CLI: `python main.py --input data/compounds.csv --n 2`
## Key Concepts
- Claude as synthesis route proposer
- Structured output: steps with reagents, conditions, yield estimates
- No RDKit validation (synthesis routes are text-based suggestions)
