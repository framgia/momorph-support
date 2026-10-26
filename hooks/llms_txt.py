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
    "Official support site for MoMorph: the V2 usage guide, the V1 to V2 migration guide, "
    "and the archived V1 docs (usage guide, MCP tools reference, FAQ, release notes). "
    "The plain-text bundles below are provided for AI assistants."
)

# base name -> human label; order = reading order inside each bundle
PAGES = [
    ("index", "Home"),
    ("v2-user-guide", "MoMorph V2 User Guide"),
    ("v1-to-v2-migration", "Migrating from V1 to V2"),
    ("archived/general-user-guide", "V1 General User Guide (archived)"),
    ("archived/mcp-tools-reference", "V1 MCP Tools Reference (archived)"),
    ("archived/faq", "V1 FAQ (archived)"),
    ("archived/release-notes", "V1 Release Notes (archived)"),
    ("archived/release-archive", "V1 Release Archive (archived)"),
]

# locale -> (display label, URL path prefix); ja is default → served at root
LANGS = [
    ("ja", "日本語", ""),
    ("vi", "Tiếng Việt", "vi/"),
]


V2_PAGES = PAGES[1:3]
V2_SUMMARY = "MoMorph V2 only: the usage guide and the V1 to V2 migration guide."


def _read(docs_dir, base, lang):
    # A page missing in one language falls back to ja, as the site's i18n plugin does.
    for code in (lang, "ja"):
        path = os.path.join(docs_dir, f"{base}.{code}.md")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return f.read().strip()
    return None


def _write_bundle(docs_dir, site_dir, name, title, summary, pages, lang):
    parts = [f"# {title}", "", f"> {summary}"]
    for base, page_label in pages:
        text = _read(docs_dir, base, lang)
        if text:
            parts.append(f"\n---\n\n# {page_label}\n\n{text}")
    with open(os.path.join(site_dir, f"{name}.{lang}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts).strip() + "\n")


def _page_url(prefix, base):
    return f"{SITE_URL}{prefix}" if base == "index" else f"{SITE_URL}{prefix}{base}/"


def on_post_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    site_dir = config["site_dir"]

    # per-language bundles: V2 only, and everything including the archived V1 docs
    for lang, label, _prefix in LANGS:
        _write_bundle(docs_dir, site_dir, "llms-v2", f"{SITE_TITLE}: MoMorph V2 ({label})", V2_SUMMARY, V2_PAGES, lang)
        _write_bundle(docs_dir, site_dir, "llms-full", f"{SITE_TITLE} ({label})", SUMMARY, PAGES, lang)

    # master index (llms.txt)
    lines = [f"# {SITE_TITLE}", "", f"> {SUMMARY}", "", "## Full-text bundles (recommended for AI)"]
    for lang, label, _prefix in LANGS:
        lines.append(f"- [{label} — MoMorph V2 guide]({SITE_URL}llms-v2.{lang}.txt)")
    for lang, label, _prefix in LANGS:
        lines.append(f"- [{label} — full guide, V1 archive included]({SITE_URL}llms-full.{lang}.txt)")
    lines.append("")
    lines.append("## Pages")
    for lang, label, prefix in LANGS:
        for base, page_label in PAGES:
            lines.append(f"- [{label}: {page_label}]({_page_url(prefix, base)})")
    with open(os.path.join(site_dir, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")
