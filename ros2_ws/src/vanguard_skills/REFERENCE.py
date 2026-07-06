#!/usr/bin/env python3
"""S2 REFERENCE — PanelSkill base class (Fable, 2026-07-07). Krithin types the real package.

Design goals, in priority order:
 1. A new skill = taught configs in YAML + a verify predicate. NOTHING else.
 2. Every hard-won behavior (leg guard, speed scaling, scene box, verify-by-effect,
    exit codes) lives HERE once, inherited by all six skills.
 3. The same class runs under CLI, BT node (S5), and P1's episode generator - three callers,
    one skill. So: no sys.argv inside the class, no rclpy.init inside the class.

configs/taught_poses.yaml (the teach registry - ch.9's harvests, versioned):
  press_button:
    hover:  [5.637, -0.408, -1.041, 4.59, 0.646, 0.0]
    press:  [5.7086, -0.4042, -1.0772, 4.6228, 0.5743, -0.0001]
  switch_flip:
    hover:  [...]   # from S1 harvest
    push_a: [...]
    push_b: [...]
"""
from dataclasses import dataclass
from typing import Callable
import time

@dataclass
class SkillResult:
    ok: bool
    reason: str          # "VERIFIED: button 8.0mm" / "LEG FAILED: hover" / "PREDICATE FAILED: 3.0mm"
    effect: dict         # final panel-state snapshot - the evidence, always returned

class PanelSkill:
    """Base: scene setup + guarded joint-space legs + verify-by-effect."""
    BOARD = dict(id="panel_board", size=[0.62, 0.03, 0.42], position=[0.55, 0.0, 0.72])

    def __init__(self, node, moveit2, panel_state: dict, taught: dict):
        # node: rclpy Node (caller owns lifecycle). moveit2: configured MoveIt2 (caller set
        # max_velocity=0.1 etc - OR set here defensively; ch.8 lesson says defensively: do both).
        self.node, self.m2, self.panel, self.taught = node, moveit2, panel_state, taught
        self.m2.max_velocity = 0.1
        self.m2.max_acceleration = 0.1

    def setup_scene(self):
        self.m2.add_collision_box(quat_xyzw=[0, 0, 0, 1], **self.BOARD)

    def leg(self, name: str, cfg) -> bool:
        self.node.get_logger().info(f"[{self.NAME}] leg: {name}")
        self.m2.move_to_configuration(cfg)
        if not self.m2.wait_until_executed():
            self.node.get_logger().error(f"[{self.NAME}] LEG FAILED: {name}")
            return False
        return True

    def run(self, **kwargs) -> SkillResult:
        """Template method: setup -> sequence() -> verify(). Subclasses define both."""
        self.setup_scene()
        for name, cfg in self.sequence(**kwargs):
            if not self.leg(name, cfg):
                return SkillResult(False, f"LEG FAILED: {name}", dict(self.panel))
        time.sleep(self.SETTLE_S)
        ok, reason = self.verify(dict(self.panel), **kwargs)
        (self.node.get_logger().info if ok else self.node.get_logger().error)(
            f"[{self.NAME}] {reason}")
        return SkillResult(ok, reason, dict(self.panel))

    # subclass contract:
    NAME = "base"; SETTLE_S = 0.5
    def sequence(self, **kw): raise NotImplementedError   # yields (leg_name, config)
    def verify(self, panel, **kw): raise NotImplementedError  # -> (ok, reason)

class PressButton(PanelSkill):
    NAME = "press_button"; SETTLE_S = 0.0  # verify DURING hold, before retreat: see sequence
    def sequence(self):
        t = self.taught[self.NAME]
        yield "hover", t["hover"]
        yield "press", t["press"]
        # verify mid-hold trick: sequence yields a sentinel? simpler: verify() reads the max
        # depression cached by the panel subscriber (caller keeps a running max during run()).
        yield "retreat", t["hover"]
    def verify(self, panel, **kw):
        d = panel.get("button_joint_max", 0.0)   # running max, cached by the state subscriber
        return (d > 0.006, f"{'VERIFIED' if d > 0.006 else 'FAILED'}: button max {d*1000:.1f}mm")

# NOTE the design fix the flat scripts couldn't express: verification uses the RUNNING MAX of
# button depression across the episode (subscriber tracks *_max keys), so verify-after-retreat
# still sees the press. Same pattern scores P1 episodes. Switch uses plain final angle (state
# persists). This asymmetry - momentary vs latching elements - is a nice textbook aside.

# CLI wrapper (thin, per skill or one dispatcher):
#   rclpy.init(); node; moveit2; subscriber updating panel dict + *_max keys;
#   result = PressButton(node, m2, panel, yaml.safe_load(taught_poses)).run()
#   raise SystemExit(0 if result.ok else 1)
