# P2 evidence plan — collect from rehearsal #1 (Fable, 2026-07-07; IROS ddl ~1 Mar 2027)

P2 = the field-systems paper: the open stack + IRC 2027 deployment results. Field papers die
from *retroactive data hunger* — you can't re-measure a competition. This plan defines what
every rehearsal and the competition itself must log, starting with Gate G0 (TASKS S6).

## The tables the paper needs (design the logging backward from these)
1. **Skill reliability table**: per skill × per environment (sim / lab-hardware / field):
   attempts, successes, failure taxonomy. → Requires: every skill run logs
   `{skill, env, result.ok, result.reason, timestamp, config_version}` to a CSV/sqlite —
   ONE logging line in PanelSkill.run() (add it in S2; it's 5 lines).
2. **Operator performance curve**: task times across rehearsal sessions (learning curve =
   great figure). → the S6 scorecards, kept consistently: date, op, task, time, interventions.
3. **Comms degradation results**: task success/time vs injected latency+loss (also seeds P5!).
   → build the latency injector early (tc netem on the base-station link is 10 lines).
4. **Failure taxonomy** (the reviewers' favorite in field papers): every failure binned
   {perception, planning, execution, comms, operator, hardware} with counts. → the reason
   strings from (1) + a 1-line human tag per failure in the rehearsal log.
5. **Competition-day narrative table**: per IRC mission — points scored, autonomy usage,
   interventions, anomalies. → assign a scribe role on comp day (a recruit); template sheet NOW.

## Standing rules
- MCAP bag EVERY hardware/rehearsal session (already doctrine) + the CSV above (new, cheap).
- `config_version` = git SHA in every log row — reviewers ask "which version did what".
- Photos/video at every rehearsal: the paper needs figures of the real rig; competition
  photography is uncontrollable, rehearsal photography isn't.
- After EACH rehearsal: 15-min log triage while memory is fresh (tag failures) — feeds both
  P2 and the next week's fixes. This ritual IS the paper being written incrementally.

## Skeleton (write Feb from filled tables): Intro (deployment>evaluation gap, cite RADAR) →
System (stack paper, mostly exists in textbook ch.1-9!) → Sim-to-field methodology (one
interface three bottoms) → Results (tables 1-5) → Failure analysis → Lessons (the textbook's
mistake logs, curated) → Release notes. Half this paper is ALREADY WRITTEN in the textbook —
P2 is largely an act of curation, IF the tables above exist.
