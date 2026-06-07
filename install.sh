#!/usr/bin/env bash
# Install the pre-deploy-security-review skill for your AI agent.
#
#   ./install.sh claude   # -> ~/.claude/skills/
#   ./install.sh codex    # -> ~/.agents/skills/
#   ./install.sh gemini   # -> ~/.gemini/skills/  + slash command in ~/.gemini/commands/
#   ./install.sh all      # all of the above
#
# Run with no argument for usage. Copies are non-destructive (asks before overwrite).
set -euo pipefail

SKILL="pre-deploy-security-review"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/$SKILL"
CMD_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/adapters/gemini-commands/security-review.toml"

die() { echo "error: $*" >&2; exit 1; }
[ -d "$SRC" ] || die "skill source not found at $SRC"

copy_to() {
  local dest_root="$1" dest="$1/$SKILL"
  mkdir -p "$dest_root"
  if [ -e "$dest" ]; then
    read -r -p "  $dest exists. Overwrite? [y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || { echo "  skipped"; return; }
    rm -rf "$dest"
  fi
  cp -R "$SRC" "$dest"
  echo "  installed -> $dest"
}

install_claude() { echo "Claude Code:"; copy_to "$HOME/.claude/skills"; }
install_codex()  { echo "Codex:";       copy_to "$HOME/.agents/skills"; }
install_gemini() {
  echo "Gemini CLI:"
  copy_to "$HOME/.gemini/skills"
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

  claude   copy skill to ~/.claude/skills/$SKILL
  codex    copy skill to ~/.agents/skills/$SKILL
  gemini   copy skill to ~/.gemini/skills/$SKILL + /security-review command
  all      install for every agent above

For project-scoped installs, copy skills/$SKILL into the repo's
.claude/skills/ , .agents/skills/ , or .gemini/skills/ directory instead.
EOF
    exit 1 ;;
esac

echo "Done. Ask your agent: \"run a pre-deploy security review on this repo\"."
