# Vanguard Arm — AI Workflow Tooling & Token Economy

Companion to `PLAN.md`. How we use Claude Code (skills, agents, MCPs, plugins) to move faster
and burn fewer tokens. Same operating principle as the AIOS: **context is the budget** — point
at knowledge, don't paste it.

## Already in the AIOS (use them, they're free)

- **`/graphify`** — per-project knowledge graph (`Jarvis/graphify/<project>/`). Vanguard-arm is
  graphified; **query the graph before re-reading source** (`.claude/rules/coding-memory.md`).
  Re-graph after structural changes (the `/checkpoint` ritual handles this).
- **`/checkpoint`** — end-of-session state dump to the Jarvis wiki + graph refresh + commit
  suggestion. Run it every session; next session resumes without re-deriving context.
- **Auto-memory + `decisions/log.md`** — cross-session facts and the append-only why-record.
- **`Explore` agent (built-in)** — fan-out repo sweeps in a subagent so file dumps never enter
  main context. First uses: map `EPFLXplore/ERC_HD` and `MissouriMRDT/Autonomy_Software`
  (PLAN §1.1), and later our own dependency archaeology.
- **`claude-code-guide` agent** — questions about Claude Code/API/SDK features go here, not to
  guesswork.
- **`/schedule` (cloud agents)** — standing automation candidate: **weekly watcher for
  IRC/ARC/ERC/IRoC-U rulebook + registration pages** (PLAN §13 item 4) that diffs pages and
  reports changes. Set up once registration season nears (~Aug).

## Skills to add

- **`find-skills`** (skills.sh registry, vercel-labs — 2.3M installs): meta-skill that
  discovers+installs skills relevant to the task at hand. **INSTALLED 2026-07-02** via
  `npx skills add vercel-labs/skills --skill find-skills` (requires Node ≥18; installs to
  `~/.agents/skills/`, symlinked into `~/.claude/skills/` where Claude Code loads from).
  Loads at session start — available from the next session.
  ⚠️ Rule for ALL third-party skills/MCPs: they are instructions that enter Claude's context —
  read the SKILL.md before installing, prefer big-name sources (anthropics/, vercel-labs/),
  and install per-project rather than globally when trialing.
- **Skills we should WRITE ourselves** (with `skill-creator` from `anthropics/skills`), once the
  pattern repeats 3+ times (AIOS Default-Shift rule):
  - `ros2-debug` — our runbook: colcon failures, QoS mismatches, TF tree issues, node graph
    checks. Codifies Block-A2 knowledge so debugging stops costing fresh tokens each time.
  - `mission-rehearsal` — spins up the scoring spreadsheet, shot-clock pacing rules (10/20-min
    IRC gates), and rehearsal log template.
  - `rulebook-diff` — old PDF + new PDF → task-relevant delta (each competition, each season).
  - `paper-figs` — house style for paper/textbook figures (works with the dataviz skill).

## MCP servers (add per-need — every enabled server's tool schemas cost tokens each session)

| Server | What it does | When |
|---|---|---|
| **ros-mcp-server** (github.com/robotmcp/ros-mcp-server) | Claude talks to the *live* ROS2 system: list/echo topics, call services, natural-language introspection. Turns bring-up debugging into conversation | Phase 1 (hardware bring-up) |
| **ROSbag MCP** (arXiv:2511.03497) | LLM analysis over rosbag/MCAP logs — pairs with our log-everything discipline | Phase 2 (rehearsal reviews) |
| **context7** | Pulls current library docs (MoveIt2, Isaac, LeRobot APIs) into context on demand — cheaper and fresher than pasting docs | Now |
| GitHub | Already covered by `gh` CLI — don't add the MCP | — |
| arXiv/paper-search MCP | Related-work sweeps during paper sprints | P1 sprint (Nov) |

Also evaluate **`nasa-jpl/rosa`** (JPL's LangChain agent for ROS ops) in Phase 1 — same idea as
ros-mcp-server from the people who operate actual Mars rovers; if it's better, adopt it and cite
it (nice paper-narrative synergy).

## Token-economy rules (standing)

1. Graph/wiki first, source second (coding-memory rule — now active for vanguard-arm).
2. Subagents for sweeps: anything that means "read many files and give me the conclusion" goes
   to Explore, not the main context.
3. Point at canon: PLAN.md/CURRICULUM.md/rulebook PDFs live on disk — reference sections, don't
   re-quote them into conversation.
4. `/checkpoint` every session so continuity is a file read, not a re-derivation.
5. MCP minimalism: enable servers in the project `.mcp.json` only while their phase needs them.
6. Logs stay as links: W&B runs and MCAP bags get referenced by URL/path, never dumped.
