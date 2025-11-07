# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the Piesors robot.
"""

# from isaaclab_assets.sensors.velodyne import VELODYNE_VLP_16_RAYCASTER_CFG

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg
from isaaclab.assets.articulation import ArticulationCfg
# from isaaclab.sensors import RayCasterCfg
# from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR

##
# Configuration - Actuators.
##

TAU_MAX = 1.61
V_MAX = 5.817764173314432

POWERHD_SERVO_ACTUATOR_CFG = DCMotorCfg(
    joint_names_expr=[".*"],
    saturation_effort=2.0,
    effort_limit=TAU_MAX,
    velocity_limit=V_MAX,
    stiffness={".*": 3.0},
    damping={".*": TAU_MAX / V_MAX},
    armature={".*": 0.01},
)
"""Configuration for PowerHD servo with DC actuator model."""


##
# Configuration - Articulation.
##

PIESORS_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path="/home/carbon/projects/piesors-learn/envs/v1/isaac/piesors_simple.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=0
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.01, rest_offset=0.0),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.2),
        joint_pos={
            ".*_abduction": 0.0,
            ".*_hip": 2.443460952792061,
            ".*_knee": 2.007128639793479,
        },
    ),
    actuators={"legs": POWERHD_SERVO_ACTUATOR_CFG},
    soft_joint_pos_limit_factor=0.9,
)
"""Configuration of Piesors robot."""
