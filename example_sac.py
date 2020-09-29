import rlcodebase
from rlcodebase.env import make_vec_envs
from rlcodebase.agent import SACAgent
from rlcodebase.utils import get_action_dim, init_parser, Config, Logger
from rlcodebase.model import ConStoSGADCLinearNet
from torch.utils.tensorboard import SummaryWriter
from argparse import ArgumentParser
import pybullet_envs

parser = ArgumentParser()
parser.add_argument('--game', default='HalfCheetah-v2', type=str)
parser.add_argument('--seed', default=0, type=int)
args = parser.parse_args()

def main():
    # create config with basic parameters for sac
    config = Config()
    config.game = 'HalfCheetah-v2'
    config.algo = 'sac'
    config.max_steps = int(1e6)
    config.num_envs = 1
    config.optimizer = 'Adam'
    config.lr = 0.001
    config.discount = 0.99
    config.replay_size = int(1e6)
    config.replay_batch = 100
    config.warmup_steps = 10000
    config.soft_update_rate = 0.005
    config.sac_alpha = 0.2
    config.automatic_alpha = False
    config.intermediate_eval = True
    config.eval_interval = int(1e4)
    config.use_gpu = True
    config.seed = 0

    # update config with argparse object (pass game and seed from command line)
    config.update(args)
    config.tag = '%s-%s-%d' % (config.game, config.algo, config.seed)
    config.after_set()
    print(config)

    # prepare env, model and logger
    env = make_vec_envs(config.game, num_envs = config.num_envs, seed = config.seed)
    eval_env = make_vec_envs(config.game, num_envs = 1, seed = config.seed)
    model = ConStoSGADCLinearNet(input_dim = env.observation_space.shape[0], action_dim = get_action_dim(env.action_space)).to(config.device)
    target_model = ConStoSGADCLinearNet(input_dim = env.observation_space.shape[0], action_dim = get_action_dim(env.action_space)).to(config.device)
    logger =  Logger(SummaryWriter(config.save_path), config.num_echo_episodes)

    # create agent and run
    agent = SACAgent(config, env, eval_env, model, target_model, logger)
    agent.run()

if __name__ == '__main__':
    main()
