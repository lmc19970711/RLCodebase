import rlcodebase
from rlcodebase.env.envs import make_vec_envs
from rlcodebase.agent.ppo_agent import PPOAgent
from rlcodebase.utils.config import PPOConfig, CommonConfig
from rlcodebase.utils import get_action_dim, select_device
from rlcodebase.model.model import CategoricalActorCriticNet
from torch.utils.tensorboard import SummaryWriter

def main():
    config = PPOConfig()
    config.rollout_length = 16
    config.discount = 0.99
    config.max_steps = int(1e4)
    config.num_workers = 4
    config.mini_batch_size = 32
    config.max_grad_norm = 0.5
    config.log_path = './runs/'
    config.game = 'BreakoutNoFrameskip-v4'
    select_device(0)

    env = make_vec_envs(config.game, num_workers = config.num_workers, seed = config.seed)
    model = CategoricalActorCriticNet(input_channels = env.observation_space.shape[0], action_dim = get_action_dim(env.action_space)).to(CommonConfig.DEVICE)
    writer = SummaryWriter(config.log_path)

    agent = PPOAgent(config, env, model, writer)
    agent.run()

if __name__ == '__main__':
    main()
