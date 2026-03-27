import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse, os, json, re, warnings
warnings.filterwarnings("ignore")
import pandas as pd
from dotenv import load_dotenv
import anthropic

load_dotenv()
os.environ.setdefault("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input", required=True)
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--model", default="claude-haiku-4-5-20251001")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input).head(args.n)
    client = anthropic.Anthropic()
    compound_list = "\n".join(f"- {r['compound_name']}: {r['smiles']}" for _, r in df.iterrows())

    prompt = (
        "You are a synthetic chemist. For each compound below, propose a 3-step retrosynthetic route.\n\n"
        f"Compounds:\n{compound_list}\n\n"
        "Respond as a JSON array:\n"
        '[{"compound_name": "...", "steps": [{"step": 1, "reaction": "...", "reagents": "...", "conditions": "...", "estimated_yield": "...%"}, ...]}, ...]'
    )

    print(f"\nPhase 65 — Synthesis Route Generation")
    print(f"Model: {args.model} | Compounds: {args.n}\n")

    response = client.messages.create(model=args.model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in response.content if hasattr(b, "text"))

    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    routes = json.loads(json_match.group()) if json_match else []

    for r in routes:
        print(f"  {r['compound_name']}:")
        for s in r.get("steps", []):
            print(f"    Step {s['step']}: {s['reaction']} | {s['reagents']} | yield={s.get('estimated_yield','?')}")

    usage = response.usage
    cost = (usage.input_tokens / 1e6 * 0.80) + (usage.output_tokens / 1e6 * 4.0)
    print(f"\nTokens: in={usage.input_tokens} out={usage.output_tokens} | Cost: ${cost:.4f}")

    with open(os.path.join(args.output_dir, "synth_routes.json"), "w") as f:
        json.dump(routes, f, indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
