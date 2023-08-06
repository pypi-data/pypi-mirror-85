import os
from stable_baselines import PPO2
from pyniel.python_tools.path_tools import make_dir_if_not_exists

from navrep.tools.commonargs import parse_common_args
from navrep.envs.e2eenv import E2E1DIANEnv
from navrep.tools.custom_policy import Custom1DPolicy
from cross_test_navreptrain_in_ianenv import run_test_episodes

class E2E1DCPolicy(object):
    """ wrapper for gym policies """
    def __init__(self, model=None):
        if model is not None:
            self.model = model
        else:
            self.model_path = os.path.expanduser(
                "~/navrep/models/gym/e2e1dnavreptrainenv_latest_PPO_ckpt")
            self.model = PPO2.load(self.model_path, policy=Custom1DPolicy)
            print("Model '{}' loaded".format(self.model_path))

    def act(self, obs):
        action, _states = self.model.predict(obs, deterministic=True)
        return action


if __name__ == '__main__':
    args, _ = parse_common_args()

    if args.n is None:
        args.n = 1000
    collect_trajectories = False

    env = E2E1DIANEnv(silent=True, collect_trajectories=collect_trajectories)
    policy = E2E1DCPolicy()

    S = run_test_episodes(env, policy, render=args.render, num_episodes=args.n)

    DIR = os.path.expanduser("~/navrep/eval/crosstest")
    if args.dry_run:
        DIR = "/tmp/navrep/eval/crosstest"
    make_dir_if_not_exists(DIR)
    if collect_trajectories:
        NAME = "e2e1dnavreptrain_in_ianenv_{}.pckl".format(len(S))
        PATH = os.path.join(DIR, NAME)
        S.to_pickle(PATH)
    else:
        NAME = "e2e1dnavreptrain_in_ianenv_{}.csv".format(len(S))
        PATH = os.path.join(DIR, NAME)
        S.to_csv(PATH)
    print("{} written.".format(PATH))
