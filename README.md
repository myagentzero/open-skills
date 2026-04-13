# ZeroClaw Skills

## Teach your AI Agent Must-Have Skills — Save 98% of API Calls

Stop wasting tokens on trial-and-error.

Give your AI agent battle-tested, ready-to-use skills that work the first time —
cut token usage by **95–98%**, lower model costs, and make smaller models reliable.

Each subdirectory is a skill. Create a `SKILL.toml` or `SKILL.md` file inside.

## SKILL.toml format

```toml
[skill]
name = "my-skill"
description = "What this skill does"
version = "0.1.0"
author = "your-name"
tags = ["productivity", "automation"]

# Shell tool — runs via sh -c (60s timeout, sandboxed env)
[[tools]]
name = "my_tool"
description = "What this tool does"
kind = "shell"
command = "echo {{message}}"

[tools.args]
message = "The message to echo"

# HTTP tool — makes a GET request (30s timeout)
[[tools]]
name = "check_status"
description = "Check service health"
kind = "http"
command = "https://api.example.com/health"
```

Tools are registered as `skill_name.tool_name` in the agent's tool registry.
Use `{{arg_name}}` placeholders in `command`; each `[tools.args]` key becomes a
required parameter the agent provides at call time.

## SKILL.md format (simpler)

Just write a markdown file with instructions for the agent.
YAML frontmatter is supported for `name`, `description`, `version`, `author`, and `tags`.
The agent will read it and follow the instructions.

## Testing skills

Add a `TEST.sh` file with test cases: `command | exit_code | output_pattern`

## Quick Links

- [Browse Skills](skills/)
- [Skill Template](SKILL_TEMPLATE.md)

**The New Approach:** Separate reasoning from execution knowledge.

- Model handles intent and orchestration
- Open Skills provides tested implementation steps (commands, API patterns, parsing logic)
- Outcome: faster execution, lower token usage, and higher reliability across both cloud and local models
