import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random
from collections import namedtuple
from attrdict import AttrDict
import time

MAX_EPISODE_LEN = 2000
ROBOT_URDF_PATH = "/home/plaif/Documents/UR5Bullet/UR5/ur_e_description/urdf/ur5e.urdf"
TABLE_URDF_PATH = os.path.join(pybullet_data.getDataPath(), "table/table.urdf")
SPHERE_URDF_PATH = os.path.join(pybullet_data.getDataPath(), "sphere2red.urdf")

class UREnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        cid = p.connect(p.SHARED_MEMORY)
        if (cid < 0):
            p.connect(p.GUI)
        p.resetDebugVisualizerCamera(1.3, 180, -41, [0.52, -0.2, -0.33])
        p.setRealTimeSimulation(True)
        p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])
        self.step_counter = 0

        self.ur5 = self.load_robot()
        self.num_joints = p.getNumJoints(self.ur5)
        
        self.control_joints = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        self.joint_type_list = ["REVOLUTE", "PRISMATIC", "SPHERICAL", "PLANAR", "FIXED"]
        self.joint_info = namedtuple("jointInfo", ["id", "name", "type", "lowerLimit", "upperLimit", "maxForce", "maxVelocity", "controllable"])

        self.joints = AttrDict()
        for i in range(self.num_joints):
            info = p.getJointInfo(self.ur5, i)
            jointID = info[0]
            jointName = info[1].decode("utf-8")
            jointType = self.joint_type_list[info[2]]
            jointLowerLimit = info[8]
            jointUpperLimit = info[9]
            jointMaxForce = info[10]
            jointMaxVelocity = info[11]
            controllable = True if jointName in self.control_joints else False
            info = self.joint_info(jointID, jointName, jointType, jointLowerLimit, jointUpperLimit, jointMaxForce, jointMaxVelocity, controllable)
            if info.type == "REVOLUTE":
                p.setJointMotorControl2(self.ur5, info.id, p.VELOCITY_CONTROL, targetVelocity=0, force=0)
            self.joints[info.name] = info   

        self.end_effector_index = 7

        self.target = np.zeros(3)
        self.action_space = spaces.Box(low=np.full((3), -1.0), high=np.full((3), 1), dtype=np.float32)
        obs = self._get_obs()
        self.observation_space = spaces.Box(np.array([-1]*21), np.array([1]*21))
        self.num = 0

    def step(self, action):
        reward =0
        p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING)
        orientation = [0.,0.,0.]
        dv = 0.05
        dx = action[0] * dv
        dy = action[1] * dv
        dz = action[2] * dv

        currentPose = self.get_current_pose()
        currentPosition = currentPose[0]
        newPosition = [currentPosition[0] + dx,
                       currentPosition[1] + dy,
                       currentPosition[2] + dz]
        joint_angles = self.calculate_ik(newPosition,orientation)

        self.set_joint_angles(joint_angles)

        p.stepSimulation()        
        obs = self._get_obs()
        time.sleep(1. / 60.)

        currentPosition = obs[0:3]
        euclidean_dist_3d = np.linalg.norm(self.target - currentPosition)

        reward = -1 * euclidean_dist_3d


        done = False

        self.step_counter += 1

        if(euclidean_dist_3d < 0.1):
            reward += 2000
            done = True            

        if(self.num > MAX_EPISODE_LEN):
            self.num = 0
            reward -= 200
            done = True
        if(self.check_collisions()):
            print("collision")
            reward -= 2000
            done = True


        info = {'object_position': self.target}
        self.num += 1
        return obs, reward, done, info

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        # p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0) # we will enable rendering after we loaded everything
        urdfRootPath=pybullet_data.getDataPath()
        p.setGravity(0,0,-10)
        self.ur5 = self.load_robot()
        
        rest_poses = [0, -math.pi, -math.pi/2, -math.pi/2, -math.pi/2, 0]
        for i in range(6):
            p.resetJointState(self.ur5,i, rest_poses[i])

        
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

        obs = self._get_obs()

        return obs

    def render(self, mode='human'):
        view_matrix = p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0.7,0,0.05],
                                                            distance=.7,
                                                            yaw=90,
                                                            pitch=-70,
                                                            roll=0,
                                                            upAxisIndex=2)
        proj_matrix = p.computeProjectionMatrixFOV(fov=60,
                                                     aspect=float(960) /720,
                                                     nearVal=0.1,
                                                     farVal=100.0)
        (_, _, px, _, _) = p.getCameraImage(width=960,
                                              height=720,
                                              viewMatrix=view_matrix,
                                              projectionMatrix=proj_matrix,
                                              renderer=p.ER_BULLET_HARDWARE_OPENGL)

        rgb_array = np.array(px, dtype=np.uint8)
        rgb_array = np.reshape(rgb_array, (720,960, 4))

        rgb_array = rgb_array[:, :, :3]
        return rgb_array

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()

    def calculate_ik(self, position, orientation):
        quaternion = p.getQuaternionFromEuler(orientation)
        lower_limits = [-math.pi]*6
        upper_limits = [math.pi]*6
        joint_ranges = [2*math.pi]*6
        rest_poses = [0, -math.pi/2, -math.pi/2, -math.pi/2, -math.pi/2, 0]

        joint_angles = p.calculateInverseKinematics(
            self.ur5, self.end_effector_index, position, quaternion, 
            jointDamping=[0.01]*6, upperLimits=upper_limits, 
            lowerLimits=lower_limits, jointRanges=joint_ranges, 
            restPoses=rest_poses
        )
        return joint_angles

    def set_joint_angles(self, joint_angles):
        poses = []
        indexes = []
        forces = []

        for i, name in enumerate(self.control_joints):
            joint = self.joints[name]
            poses.append(joint_angles[i])
            indexes.append(joint.id)
            forces.append(joint.maxForce)

        p.setJointMotorControlArray(
            self.ur5, indexes,
            p.POSITION_CONTROL,
            targetPositions=joint_angles,
            targetVelocities=[0]*len(poses),
            positionGains=[0.04]*len(poses), forces=forces
        )

    def get_joint_angles(self):
        j = p.getJointStates(self.ur5, [1,2,3,4,5,6])
        joints = [i[0] for i in j]
        return joints

    def get_current_pose(self):
        linkstate = p.getLinkState(self.ur5, self.end_effector_index, computeForwardKinematics=True)
        position, orientation = linkstate[0], linkstate[1]
        return (position, orientation)

    def get_current_velocity(self):
        j = p.getJointStates(self.ur5, [1,2,3,4,5,6])
        joints = [i[1] for i in j]
        return joints

    def load_robot(self):
        flags = p.URDF_USE_SELF_COLLISION
        table = p.loadURDF(TABLE_URDF_PATH, [0.5, 0, -0.6300], [0, 0, 0, 1])
        robot = p.loadURDF(ROBOT_URDF_PATH, [0, 0, 0], [0, 0, 0, 1], flags=flags)
        
        # state_object= [random.uniform(0.3,0.6),random.uniform(-0.2,0.2),random.uniform(0.3,0.6)]
        state_object= [0.4,0.1,0.4]
        self.objectUid = p.loadURDF(SPHERE_URDF_PATH, useMaximalCoordinates=False,globalScaling=0.1,basePosition=state_object,useFixedBase=True)

        collisionFilterGroup = 0
        collisionFilterMask = 0
        p.setCollisionFilterGroupMask(self.objectUid, -1, collisionFilterGroup, collisionFilterMask)

        enableCollision = 0
        p.setCollisionFilterPair(robot, self.objectUid, -1, -1, enableCollision)
       
        return robot

    def check_collisions(self):
        collisions = p.getContactPoints()
        if len(collisions) > 0:
            return True
        return False

    # def _get_observation_space(self):
    #     position, orientation = self.get_current_pose()
    #     position = np.array(position)

    #     joints = self.get_joint_angles()
    #     joints = np.array(joints)

    #     joints_vel = self.get_current_velocity()
    #     joints_vel = np.array(joints_vel)

    #     self.target = np.array([0.1,0.1,0.1])

    #     target_rel_pos = self.target - position
        
    #     obs = np.concatenate([position,self.target,target_rel_pos,joints,joints_vel])

    #     return spaces.Box(low=min_obs, high=max_obs, dtype=np.float32)

    def _get_obs(self):
        position, orientation = self.get_current_pose()
        position = np.array(position)

        joints = self.get_joint_angles()
        joints = np.array(joints)

        joints_vel = self.get_current_velocity()
        joints_vel = np.array(joints_vel)

        state_object, _ = p.getBasePositionAndOrientation(self.objectUid)
        self.target = np.array(state_object[0:3])

        target_rel_pos = self.target - position
        
        obs = np.concatenate([position,self.target,target_rel_pos,joints,joints_vel])
        return obs
