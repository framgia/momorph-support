"""MkDocs build hook: generate llms.txt + per-language llms-full.*.txt.

Produces AI-readable plain-text bundles of the user guide so end users can paste
a single URL into an LLM and ask questions instead of reading the whole site.
Regenerated on every build from the published docs, so it never drifts.

Output (at site root):
  /llms.txt                 master index (all languages) per llmstxt.org
  /llms-full.<lang>.txt     full concatenated guide for one language
"""

import os

SITE_TITLE = "MoMorph User Guide"
SITE_URL = "https://framgia.github.io/momorph-support/"

SUMMARY = (
    "Official support site for MoMorph: usage guide, MCP tools reference, FAQ, "
    "and release notes. The plain-text bundles below are provided for AI assistants."
)

# base name -> human label; order = reading order inside each bundle
PAGES = [
    ("index", "Home"),
    ("general-user-guide", "General User Guide"),
    ("mcp-tools-reference", "MCP Tools Reference"),
    ("faq", "FAQ"),
    ("release-notes", "Release Notes"),
    ("release-archive", "Release Archive"),
]

# locale -> (display label, URL path prefix); ja is default → served at root
LANGS = [
    ("ja", "日本語", ""),
    ("vi", "Tiếng Việt", "vi/"),
    ("en", "English", "en/"),
]


def _read(docs_dir, base, lang):
    path = os.path.join(docs_dir, f"{base}.{lang}.md")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def _page_url(prefix, base):
    return f"{SITE_URL}{prefix}" if base == "index" else f"{SITE_URL}{prefix}{base}/"


def on_post_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    site_dir = config["site_dir"]

    # per-language full-text bundles
    for lang, label, _prefix in LANGS:
        parts = [f"# {SITE_TITLE} ({label})", "", f"> {SUMMARY}"]
        for base, page_label in PAGES:
            text = _read(docs_dir, base, lang)
            if not text:
                continue
            parts.append(f"\n---\n\n# {page_label}\n\n{text}")
        with open(os.path.join(site_dir, f"llms-full.{lang}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(parts).strip() + "\n")

    # master index (llms.txt)
    lines = [f"# {SITE_TITLE}", "", f"> {SUMMARY}", "", "## Full-text bundles (recommended for AI)"]
    for lang, label, _prefix in LANGS:
        lines.append(f"- [{label} — full guide]({SITE_URL}llms-full.{lang}.txt)")
    lines.append("")
    lines.append("## Pages")
    for lang, label, prefix in LANGS:
        for base, page_label in PAGES:
            lines.append(f"- [{label}: {page_label}]({_page_url(prefix, base)})")
    with open(os.path.join(site_dir, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")
