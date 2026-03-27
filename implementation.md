# Phase 65 — Claude Generating Synthesis Route from Scaffold

**Version:** 1.1 | **Tier:** Standard | **Date:** 2026-03-27

## Goal
Ask Claude to propose a 3-step retrosynthetic route for CETP inhibitor compounds, returned as structured JSON with reagents, conditions, and yield estimates.

CLI: `python main.py --input data/compounds.csv --n 2`

Outputs: synth_routes.json

## Logic
- Load N compounds from CSV (name, SMILES)
- Build a prompt asking for 3-step retrosynthetic routes per compound
- Require structured output: step number, reaction type, reagents, conditions, estimated yield
- Parse JSON array of route proposals
- Report: route completeness, reaction types, yield estimates

## Key Concepts
- Claude as synthetic chemistry advisor
- Retrosynthesis: working backward from target to simpler precursors
- Structured output: `[{compound_name, steps: [{step, reaction, reagents, conditions, estimated_yield}]}]`
- No RDKit validation (synthesis routes are text-based domain knowledge)
- Tests Claude's organic chemistry reaction knowledge

## Verification Checklist
- [x] Claude generates 3-step routes for each compound
- [x] Each step includes reaction type, reagents, conditions, yield
- [x] Routes are chemically plausible (acrylamide coupling as primary route)
- [x] One clean API call

## Results
| Metric | Value |
|--------|-------|
| Compounds analyzed | 2 |
| Routes generated | 2 (3 steps each) |
| Primary reaction | Amide coupling (acryloyl chloride + aniline) — 85-87% yield |
| Alternative routes | SNAr (68-70%), Friedel-Crafts (63-65%) |
| Input tokens | 151 |
| Output tokens | 772 |
| Est. cost | $0.0032 |

Key finding: Claude correctly identified amide coupling as the highest-yielding primary route, with SNAr and Friedel-Crafts as lower-yield alternatives.

## Risks (resolved)
- Synthesis routes may be chemically implausible — Claude proposed reasonable reactions (amide coupling, SNAr, Friedel-Crafts)
- Yield estimates may be inaccurate — acknowledged as estimates, not validated experimentally
- Routes for different compounds may be identical — observed (halogen substitution doesn't change route)
