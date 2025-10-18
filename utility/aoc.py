#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# --- Defaults / paths ---------------------------------------------------------
APP_NAME = "aoc-cli"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_BASE_DIR = Path.cwd()  # where to create year/day folders by default
DEFAULT_TEMPLATES_DIR = Path.cwd() / "utility/templates"  # your existing templates/

TZ = "Europe/Copenhagen"  # AoC unlocks ~06:00/07:00 here depending on DST

# Map a language key to (template filename, output filename)
LANG_MAP = {
    "python": ("solution_template.py", "solution.py"),
    "elixir": ("solution_template.ex", "solution.ex"),
    # add more when you add templates:
    "go": ("solution_template.go", "main.go"),
    "rust": ("solution_template.rs", "main.rs"),
    "crystal": ("solution_template.cr", "solution.cr"),
    "ts": ("solution_template.ts", "solution.ts"),
}


# --- Config helpers -----------------------------------------------------------
def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {
        "session": None,
        "base_dir": str(DEFAULT_BASE_DIR),
        "templates_dir": str(DEFAULT_TEMPLATES_DIR),
    }


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


# --- Date utilities -----------------------------------------------------------
def resolve_date(today: bool, year: Optional[int], day: Optional[int]) -> Tuple[int, int]:
    if today:
        # Europe/Copenhagen local date
        try:
            from zoneinfo import ZoneInfo  # py>=3.9
            now = dt.datetime.now(ZoneInfo(TZ))
        except Exception:
            # Fallback: naive local time
            now = dt.datetime.now()
        return now.year, now.day
    if year is None or day is None:
        raise ValueError("Must provide --year and --day, or use --today.")
    if not (1 <= day <= 25):
        raise ValueError("Day must be between 1 and 25.")
    return year, day


# --- Network ------------------------------------------------------------------
def fetch_input(year: int, day: int, session: str) -> bytes:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = Request(url, headers={"Cookie": f"session={session}", "User-Agent": "aoc-cli (+github.com/you)"})
    try:
        with urlopen(req) as resp:
            return resp.read()
    except HTTPError as e:
        if e.code == 400 or e.code == 404:
            raise RuntimeError(f"Failed to fetch input: HTTP {e.code} (check year/day unlock window or URL).")
        if e.code == 500 or e.code == 503:
            raise RuntimeError("AoC is busy/unavailable; try again in a bit.")
        if e.code == 302 or e.code == 403:
            raise RuntimeError("Unauthorized: your session cookie is missing/invalid/expired.")
        raise
    except URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")


# --- Filesystem / scaffolding -------------------------------------------------
def ensure_dirs(base_dir: Path, year: int, day: int, lang: str) -> Path:
    dpath = base_dir / str(year) / f"{day:02d}" / lang
    dpath.mkdir(parents=True, exist_ok=True)
    return dpath


def copy_template(templates_dir: Path, lang: str, target_dir: Path) -> Path:
    if lang not in LANG_MAP:
        raise ValueError(
            f"Unknown language '{lang}'. Supported: {', '.join(LANG_MAP.keys())}. "
            f"Add a template to {templates_dir} and update LANG_MAP to enable more."
        )
    template_name, out_name = LANG_MAP[lang]
    src = templates_dir / template_name
    if not src.exists():
        raise FileNotFoundError(f"Template not found: {src}")
    dst = target_dir / out_name
    if not dst.exists():
        dst.write_text(src.read_text())
    return dst


def write_input(target_dir: Path, data: bytes) -> Path:
    ipath = target_dir / "input"
    ipath.write_bytes(data)
    return ipath


def write_readme(target_dir: Path, year: int, day: int) -> Path:
    r = target_dir / "README.md"
    if not r.exists():
        r.write_text(f"# Advent of Code {year} — Day {day:02d}\n\n"
                     f"- Puzzle: https://adventofcode.com/{year}/day/{day}\n"
                     f"- Input is in `./input`\n")
    return r


# --- Commands ----------------------------------------------------------------
def cmd_config(args: argparse.Namespace) -> None:
    cfg = load_config()
    changed = False

    if args.session:
        cfg["session"] = args.session
        changed = True

    if args.base_dir:
        cfg["base_dir"] = str(Path(args.base_dir).expanduser().resolve())
        changed = True

    if args.templates_dir:
        cfg["templates_dir"] = str(Path(args.templates_dir).expanduser().resolve())
        changed = True

    if changed:
        save_config(cfg)
        print(f"Saved config to {CONFIG_FILE}")
    else:
        print(json.dumps(cfg, indent=2))


def cmd_fetch(args: argparse.Namespace) -> None:
    cfg = load_config()
    session = args.session or cfg.get("session") or os.environ.get("AOC_SESSION")
    if not session:
        raise SystemExit(
            "No session cookie found. Set it via:\n"
            f"  {Path(sys.argv[0]).name} config --session <token>\n"
            "or export AOC_SESSION=...\n"
            "Find it in your browser cookies for adventofcode.com (name: session)."
        )

    year, day = resolve_date(args.today, args.year, args.day)

    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else Path(cfg["base_dir"])
    target_lang = args.lang or "python"  # default language for folder path if you want
    target_dir = ensure_dirs(base_dir, year, day, target_lang)

    data = fetch_input(year, day, session)
    ipath = write_input(target_dir, data)
    print(f"Wrote input → {ipath}")


def cmd_new(args: argparse.Namespace) -> None:
    cfg = load_config()
    session = args.session or cfg.get("session") or os.environ.get("AOC_SESSION")
    if not session:
        raise SystemExit(
            "No session cookie found. Set it via:\n"
            f"  {Path(sys.argv[0]).name} config --session <token>\n"
            "or export AOC_SESSION=...\n"
        )

    year, day = resolve_date(args.today, args.year, args.day)
    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else Path(cfg["base_dir"])
    templates_dir = Path(args.templates_dir).expanduser().resolve() if args.templates_dir else Path(cfg["templates_dir"])
    lang = args.lang or "python"

    target_dir = ensure_dirs(base_dir, year, day, lang)
    # Fetch input first
    data = fetch_input(year, day, session)
    ipath = write_input(target_dir, data)

    # Copy template
    spath = copy_template(templates_dir, lang, target_dir)

    # README with links
    rpath = write_readme(target_dir, year, day)

    print(f"Scaffolded {year}/day{day:02d} [{lang}]")
    print(f" - input   → {ipath}")
    print(f" - solution→ {spath}")
    print(f" - readme  → {rpath}")


# --- CLI ---------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aoc", description="Advent of Code helper CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    # config
    pc = sub.add_parser("config", help="Show or set configuration")
    pc.add_argument("--session", help="Set AoC session cookie token")
    pc.add_argument("--base-dir", help="Default base dir for scaffolds")
    pc.add_argument("--templates-dir", help="Default templates dir")
    pc.set_defaults(func=cmd_config)

    # fetch
    pf = sub.add_parser("fetch", help="Fetch input for a day")
    pf.add_argument("-y", "--year", type=int, help="Year, e.g. 2025")
    pf.add_argument("-d", "--day", type=int, help="Day (1..25)")
    pf.add_argument("--today", action="store_true", help="Use today in Europe/Copenhagen")
    pf.add_argument("-l", "--lang", help="Folder language (only influences path)")
    pf.add_argument("--session", help="Override session cookie for this call")
    pf.add_argument("--base-dir", help="Override base dir")
    pf.set_defaults(func=cmd_fetch)

    # new
    pn = sub.add_parser("new", help="Fetch input and scaffold solution from template")
    pn.add_argument("-y", "--year", type=int, help="Year, e.g. 2025")
    pn.add_argument("-d", "--day", type=int, help="Day (1..25)")
    pn.add_argument("--today", action="store_true", help="Use today in Europe/Copenhagen")
    pn.add_argument("-l", "--lang", choices=list(LANG_MAP.keys()), default="python", help="Language key")
    pn.add_argument("--session", help="Override session cookie for this call")
    pn.add_argument("--base-dir", help="Override base dir")
    pn.add_argument("--templates-dir", help="Override templates dir")
    pn.set_defaults(func=cmd_new)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
