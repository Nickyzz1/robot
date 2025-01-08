# version: Python3
from DobotEDU import *

posY = 70
for i  in range(4):
  m_lite.set_homecmd()
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=posY, z=20, r=0)
  m_lite.set_endeffector_suctioncup(enable=True, on=True)
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=posY, z=-40.5, r=0)
  
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=posY, z=20, r=0)
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=-posY, z=20, r=0)
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=-posY, z=-39.5, r=0)
  m_lite.set_endeffector_suctioncup(enable=False, on=False)
  m_lite.set_ptpcmd(ptp_mode=2, x=270, y=-posY, z=0, r=0)

  if posY > 0:
    posY+=20
  else:
    posY-=20
