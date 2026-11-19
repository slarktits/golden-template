.PHONY: agents-sync agents-check

# .cursor/rules/*.mdc is the source. This rewrites .agents/rules
# (Antigravity, OpenCode) and .claude/rules (Claude Code) from those files.
agents-sync:
	python3 scripts/sync_agent_config.py

agents-check:
	python3 scripts/sync_agent_config.py --check
