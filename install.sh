#!/usr/bin/env bash
# Install the pre-deploy-security-review skill(s) for your AI agent.
# Installs both language variants found under skills/ (English + Polish).
#
#   ./install.sh claude   # -> ~/.claude/skills/
#   ./install.sh codex    # -> ~/.agents/skills/
#   ./install.sh gemini   # -> ~/.gemini/skills/  + slash command in ~/.gemini/commands/
#   ./install.sh all      # all of the above
#
# Run with no argument for usage. Copies are non-destructive (asks before overwrite).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$ROOT/skills"
CMD_SRC="$ROOT/adapters/gemini-commands/security-review.toml"

die() { echo "error: $*" >&2; exit 1; }
[ -d "$SKILLS_DIR" ] || die "skills/ not found at $SKILLS_DIR"

copy_skills_to() {
  local dest_root="$1"
  mkdir -p "$dest_root"
  for src in "$SKILLS_DIR"/*/; do
    [ -f "$src/SKILL.md" ] || continue
    local name dest
    name="$(basename "$src")"
    dest="$dest_root/$name"
    if [ -e "$dest" ]; then
      read -r -p "  $dest exists. Overwrite? [y/N] " ans
      [[ "$ans" =~ ^[Yy]$ ]] || { echo "  skipped $name"; continue; }
      rm -rf "$dest"
    fi
    cp -R "${src%/}" "$dest"
    echo "  installed -> $dest"
  done
}

install_claude() { echo "Claude Code:"; copy_skills_to "$HOME/.claude/skills"; }
install_codex()  { echo "Codex:";       copy_skills_to "$HOME/.agents/skills"; }
install_gemini() {
  echo "Gemini CLI:"
  copy_skills_to "$HOME/.gemini/skills"
  mkdir -p "$HOME/.gemini/commands"
  cp "$CMD_SRC" "$HOME/.gemini/commands/security-review.toml"
  echo "  slash command -> ~/.gemini/commands/security-review.toml  (run /security-review)"
}

case "${1:-}" in
  claude) install_claude ;;
  codex)  install_codex ;;
  gemini) install_gemini ;;
  all)    install_claude; install_codex; install_gemini ;;
  *)
    cat <<EOF
Usage: ./install.sh <claude|codex|gemini|all>

  claude   copy skills to ~/.claude/skills/
  codex    copy skills to ~/.agents/skills/
  gemini   copy skills to ~/.gemini/skills/ + /security-review command
  all      install for every agent above

Installs both language variants (pre-deploy-security-review and
pre-deploy-security-review-pl). For a project-scoped install, copy the skill
folder you want into the repo's .claude/skills/ , .agents/skills/ , or
.gemini/skills/ directory instead.
EOF
    exit 1 ;;
esac

echo "Done. Ask your agent: \"run a pre-deploy security review on this repo\"."
