# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass

from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg, RewTerm, SceneEntityCfg, mdp

##
# Pre-defined configs
##
from isaaclab_assets.robots.piesors import PIESORS_CFG  # isort: skip


@configclass
class PiesorsRoughEnvCfg(LocomotionVelocityRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # switch robot to piesors
        self.scene.robot = PIESORS_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        self.scene.num_envs = 2**15
        self.scene.env_spacing = 2.0

        self.events.add_base_mass.params["mass_distribution_params"] = (0.9, 1.1)
        self.events.add_base_mass.params["operation"] = "scale"

        self.events.base_com.params["com_range"] = {"x": (-0.01, 0.01), "y": (-0.01, 0.01), "z": (-0.01, 0.01)}

        self.events.reset_base.params["velocity_range"] = {
            "x": (0.0, 0.0),
            "y": (0.0, 0.0),
            "z": (0.0, 0.0),
            "roll": (0.0, 0.0),
            "pitch": (0.0, 0.0),
            "yaw": (0.0, 0.0),
        }

        self.events.reset_robot_joints.params["position_range"] = (0.9, 1.1)

        self.events.push_robot.params["velocity_range"] = {"x": (-0.1, 0.1), "y": (-0.1, 0.1)}

        self.observations.policy.base_lin_vel = None
        self.observations.policy.base_ang_vel = None
        self.observations.policy.projected_gravity = None
        # self.observations.policy.joint_pos = None
        self.observations.policy.joint_vel = None

        self.commands.base_velocity.ranges.lin_vel_x = (-1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.5, 0.5)
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)

        # self.rewards.track_lin_vel_xy_exp.weight = 40.0
        # self.rewards.track_lin_vel_xy_exp.params["std"] = 0.02

        self.rewards.base_height_l2 = RewTerm(
            func=mdp.base_height_l2,
            weight=-100.0,
            params={
                "asset_cfg": SceneEntityCfg("robot", body_names="base"),
                "target_height": 0.18,
            },
        )

        # self.rewards.feet_slide = RewTerm(
        #     func=mdp.feet_slide,
        #     weight=-0.1,
        #     params={
        #         "sensor_cfg": SceneEntityCfg("contact_forces", body_names=".*FOOT"),
        #         "asset_cfg": SceneEntityCfg("robot", body_names=".*FOOT"),
        #     },
        # )

        self.rewards.stand_still_joint_deviation_l1 = RewTerm(
            func=mdp.stand_still_joint_deviation_l1,
            weight=-0.1,
            params={
                "command_name": "base_velocity",
                "command_threshold": 0.05,
                "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
            },
        )

        # self.actions.joint_pos.scale = 0.5

        # self.events.base_external_force_torque = None
        # self.events.push_robot = None

        self.scene.height_scanner = None
        self.observations.policy.height_scan = None


@configclass
class PiesorsRoughEnvCfg_PLAY(PiesorsRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 16
        self.scene.env_spacing = 2.5
        # spawn the robot randomly in the grid (instead of their terrain levels)
        self.scene.terrain.max_init_terrain_level = None
        # reduce the number of terrains to save memory
        if self.scene.terrain.terrain_generator is not None:
            self.scene.terrain.terrain_generator.num_rows = 5
            self.scene.terrain.terrain_generator.num_cols = 5
            self.scene.terrain.terrain_generator.curriculum = False

        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event
        self.events.base_external_force_torque = None
        self.events.push_robot = None
