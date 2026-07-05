# IDMO panel v0.1 — board (kinematic) + push button (prismatic+spring) + toggle switch (revolute)
# Run in Isaac Script Editor with the VanguardArm stage open (sim STOPPED). Re-runnable: deletes old panel.
# NOTE on joint anchors: UsdPhysics joint localPos is expressed in the body's LOCAL frame and is
# multiplied by the prim's scale. Anchors below are written in pre-scale units on purpose.

from pxr import Usd, UsdGeom, UsdPhysics, Gf
import omni.usd

stage = omni.usd.get_context().get_stage()
PANEL = "/World/IDMOPanel"
if stage.GetPrimAtPath(PANEL):
    stage.RemovePrim(PANEL)  # clean rebuild every run

def cube(path, size, pos, color):
    c = UsdGeom.Cube.Define(stage, path)
    c.GetSizeAttr().Set(1.0)                      # unit cube: spans -0.5..+0.5
    xf = UsdGeom.Xformable(c)
    xf.ClearXformOpOrder()
    xf.AddTranslateOp().Set(Gf.Vec3d(*pos))
    xf.AddScaleOp().Set(Gf.Vec3f(*size))          # scale = FULL dimensions
    c.GetDisplayColorAttr().Set([Gf.Vec3f(*color)])
    UsdPhysics.CollisionAPI.Apply(c.GetPrim())
    return c.GetPrim()

# ---- board: 0.6 wide x 0.4 tall, face toward the arm, centered 1.0 m up, 0.55 m out ----
# Kinematic rigid body: immovable but collidable - no joint-to-world needed.
board = cube(f"{PANEL}/board", (0.6, 0.02, 0.4), (0.55, 0.0, 1.0), (0.35, 0.35, 0.4))
rb = UsdPhysics.RigidBodyAPI.Apply(board)
rb.CreateKinematicEnabledAttr().Set(True)

# ---- push button: 8 mm prismatic travel along Y (into the board), spring return ----
# Anchor on board face: board-local (-0.2, -0.5, 0.25) * scale(0.6,0.02,0.4) = (-0.12, -0.01, +0.10)
btn = cube(f"{PANEL}/button", (0.04, 0.02, 0.04), (0.43, -0.02, 1.10), (0.8, 0.1, 0.1))
UsdPhysics.RigidBodyAPI.Apply(btn)
bj = UsdPhysics.PrismaticJoint.Define(stage, f"{PANEL}/button_joint")
bj.CreateBody0Rel().SetTargets([board.GetPath()])
bj.CreateBody1Rel().SetTargets([btn.GetPath()])
bj.CreateAxisAttr().Set("Y")
bj.CreateLowerLimitAttr().Set(0.0)
bj.CreateUpperLimitAttr().Set(0.008)
bj.CreateLocalPos0Attr().Set(Gf.Vec3f(-0.2, -0.5, 0.25))   # on the board's front face
bj.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.5, 0.0))      # button's back face
drv = UsdPhysics.DriveAPI.Apply(bj.GetPrim(), "linear")
drv.CreateTargetPositionAttr().Set(0.0)
drv.CreateStiffnessAttr().Set(200.0)
drv.CreateDampingAttr().Set(10.0)

# ---- toggle switch: revolute about X, +/-25 deg, pivot at its base ----
# Anchor: board-local (0.2, -0.5, 0.25) -> world (+0.12, -0.01, +0.10) on the face
sw = cube(f"{PANEL}/switch", (0.015, 0.05, 0.05), (0.67, -0.03, 1.10), (0.9, 0.7, 0.1))
UsdPhysics.RigidBodyAPI.Apply(sw)
sj = UsdPhysics.RevoluteJoint.Define(stage, f"{PANEL}/switch_joint")
sj.CreateBody0Rel().SetTargets([board.GetPath()])
sj.CreateBody1Rel().SetTargets([sw.GetPath()])
sj.CreateAxisAttr().Set("X")
sj.CreateLowerLimitAttr().Set(-25.0)
sj.CreateUpperLimitAttr().Set(25.0)
sj.CreateLocalPos0Attr().Set(Gf.Vec3f(0.2, -0.5, 0.25))
sj.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.4, -0.4))     # pivot at switch base-back
# light drive = detent-ish resistance so it holds position instead of flopping
sdrv = UsdPhysics.DriveAPI.Apply(sj.GetPrim(), "angular")
sdrv.CreateStiffnessAttr().Set(0.0)
sdrv.CreateDampingAttr().Set(0.5)

print("IDMO panel v0.1 built:", PANEL)
