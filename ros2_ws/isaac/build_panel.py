# IDMO panel v0.2 — lowered for floor-mounted stand-in reach (true height returns with Phase-1 rover deck)
from pxr import Usd, UsdGeom, UsdPhysics, Gf
import omni.usd

stage = omni.usd.get_context().get_stage()
PANEL = "/World/IDMOPanel"
if stage.GetPrimAtPath(PANEL):
    stage.RemovePrim(PANEL)  # clean rebuild every run

def cube(path, size, pos, color):
    c = UsdGeom.Cube.Define(stage, path)
    c.GetSizeAttr().Set(1.0)
    xf = UsdGeom.Xformable(c)
    xf.ClearXformOpOrder()
    xf.AddTranslateOp().Set(Gf.Vec3d(*pos))
    xf.AddScaleOp().Set(Gf.Vec3f(*size))
    c.GetDisplayColorAttr().Set([Gf.Vec3f(*color)])
    UsdPhysics.CollisionAPI.Apply(c.GetPrim())
    return c.GetPrim()

# board: kinematic (immovable, collidable), center z=0.72
board = cube(f"{PANEL}/board", (0.6, 0.02, 0.4), (0.55, 0.0, 0.72), (0.35, 0.35, 0.4))
rb = UsdPhysics.RigidBodyAPI.Apply(board)
rb.CreateKinematicEnabledAttr().Set(True)

# push button: prismatic, 8mm travel, spring return — now at z=0.82
btn = cube(f"{PANEL}/button", (0.04, 0.02, 0.04), (0.43, -0.02, 0.82), (0.8, 0.1, 0.1))
UsdPhysics.RigidBodyAPI.Apply(btn)
bj = UsdPhysics.PrismaticJoint.Define(stage, f"{PANEL}/button_joint")
bj.CreateBody0Rel().SetTargets([board.GetPath()])
bj.CreateBody1Rel().SetTargets([btn.GetPath()])
bj.CreateAxisAttr().Set("Y")
bj.CreateLowerLimitAttr().Set(0.0)
bj.CreateUpperLimitAttr().Set(0.008)
bj.CreateLocalPos0Attr().Set(Gf.Vec3f(-0.2, -0.5, 0.25))
bj.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.5, 0.0))
drv = UsdPhysics.DriveAPI.Apply(bj.GetPrim(), "linear")
drv.CreateTargetPositionAttr().Set(0.0)
drv.CreateStiffnessAttr().Set(200.0)
drv.CreateDampingAttr().Set(10.0)

# toggle switch: revolute ±25°, light damping — now at z=0.82
sw = cube(f"{PANEL}/switch", (0.015, 0.05, 0.05), (0.67, -0.03, 0.82), (0.9, 0.7, 0.1))
UsdPhysics.RigidBodyAPI.Apply(sw)
sj = UsdPhysics.RevoluteJoint.Define(stage, f"{PANEL}/switch_joint")
sj.CreateBody0Rel().SetTargets([board.GetPath()])
sj.CreateBody1Rel().SetTargets([sw.GetPath()])
sj.CreateAxisAttr().Set("X")
sj.CreateLowerLimitAttr().Set(-25.0)
sj.CreateUpperLimitAttr().Set(25.0)
sj.CreateLocalPos0Attr().Set(Gf.Vec3f(0.2, -0.5, 0.25))
sj.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.4, -0.4))
sdrv = UsdPhysics.DriveAPI.Apply(sj.GetPrim(), "angular")
sdrv.CreateStiffnessAttr().Set(0.0)
sdrv.CreateDampingAttr().Set(0.5)

print("IDMO panel v0.2 built (lowered):", PANEL)

