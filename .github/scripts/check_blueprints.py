"""Prüft die Blueprints: gültiges YAML und jedes !input ist definiert."""
import pathlib
import sys

import yaml


class Input(str):
    pass


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor("!input", lambda l, n: Input(l.construct_scalar(n)))


def defined_inputs(inputs: dict) -> set[str]:
    names = set()
    for key, val in inputs.items():
        if isinstance(val, dict) and "input" in val:
            names |= defined_inputs(val["input"])
        else:
            names.add(key)
    return names


def used_inputs(node) -> set[str]:
    if isinstance(node, Input):
        return {str(node)}
    if isinstance(node, dict):
        return set().union(*(used_inputs(v) for v in node.values())) if node else set()
    if isinstance(node, list):
        return set().union(*(used_inputs(v) for v in node)) if node else set()
    return set()


errors = 0
for path in sorted(pathlib.Path("blueprints").rglob("*.yaml")):
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)
    bp = data["blueprint"]
    defined = defined_inputs(bp["input"])
    body = {k: v for k, v in data.items() if k != "blueprint"}
    missing = used_inputs(body) - defined
    unused = defined - used_inputs(body)
    status = "ok"
    if missing:
        status = f"FEHLER: nicht definiert {sorted(missing)}"
        errors += 1
    elif unused:
        status = f"Hinweis: ungenutzt {sorted(unused)}"
    print(f"{path}: {bp['domain']}, {len(defined)} Eingaben – {status}")
sys.exit(1 if errors else 0)
