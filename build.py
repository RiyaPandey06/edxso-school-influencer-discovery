
import json
from pathlib import Path

data = json.loads(
    Path("data/profiles.json").read_text(encoding="utf-8")
)

template = Path("src/app.template.html").read_text(encoding="utf-8")

output = template.replace(
    "__DATA__",
    json.dumps(data, separators=(",", ":"), ensure_ascii=False)
)

Path("dist.html").write_text(output, encoding="utf-8")

print("Build successful! dist.html created.")
