from gym.envs.registration import register

register(
    id='UR-v0',
    entry_point='bullet_ur_gym_test.envs:UREnv',
)
