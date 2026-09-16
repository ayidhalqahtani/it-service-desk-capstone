from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md", "CAPSTONE_DESIGN.md", "DECISIONS.md",
    "EVALUATION_REPORT.md", "BENCHMARKS.md",
    "notebooks/IT_Service_Desk_Capstone.ipynb",
    "config/models.json",
    "data/golden_set.json",
    "data/attacks.json",
    "data/legitimate_guard_cases.json",
    "prompts/router_v1.txt",
    "prompts/guard_inbound_v1.txt",
    "prompts/judge_v1.txt",
]
missing = [x for x in required if not (ROOT/x).exists()]
assert not missing, f"Missing required files: {missing}"

models = json.loads((ROOT/"config/models.json").read_text())
assert models["open_weight"]["model_id"]
assert models["commercial"]["model_id"]
assert models["judge"]["model_id"]

golden = json.loads((ROOT/"data/golden_set.json").read_text())
assert len(golden) >= 40
assert sum(x["language"] == "ar" for x in golden) > sum(x["language"] == "en" for x in golden)
assert all(x.get("owner_approved") is True for x in golden)

for path in (ROOT/"prompts").glob("*.txt"):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("VERSION:"), f"Prompt missing version header: {path.name}"

secret_patterns = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"OPENAI_API_KEY\s*=\s*['\"][^'\"]+['\"]"),
]
for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix in {".py",".md",".json",".txt",".ipynb"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not any(p.search(text) for p in secret_patterns), f"Possible committed secret in {path}"

print("[PASS] Repository preflight complete.")
print("Golden cases:", len(golden))
print("Arabic cases:", sum(x["language"] == "ar" for x in golden))
