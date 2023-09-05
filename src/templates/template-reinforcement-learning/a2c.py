from pprint import pformat
from shutil import copy
from typing import Any

import ignite.distributed as idist
import torch
from ignite.engine import Events
from ignite.handlers import LRScheduler

from ignite.utils import manual_seed

from utils import *

from a2c_model_env import make_a2c_models, make_collector, make_loss, make_optim, make_test_env


def main():
    config = setup_config()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    config.device = f"{device}"

    rank = idist.get_rank()
    manual_seed(config.seed + rank)
    config.output_dir = setup_output_dir(config, rank)
    if rank == 0:
        save_config(config, config.output_dir)

    actor, critic = make_a2c_models(config)
    actor = actor.to(device)
    critic = critic.to(device)

    collector = make_collector(config, policy=actor)
    loss_module, adv_module = make_loss(config, actor_network=actor, value_network=critic)
    optim = make_optim(config, actor_network=actor, value_network=critic)

    batch_size = config.total_frames * config.num_envs
    total_network_updates = config.total_frames // batch_size

    scheduler = None
    if config.lr_scheduler:
        scheduler = torch.optim.lr_scheduler.LinearLR(optim, total_iters=total_network_updates)
        scheduler = LRScheduler(scheduler)

    test_env = make_test_env(config)

    def run_single_timestep(engine, _):
        frames_in_batch = engine.state.data.numel()
        trainer.state.collected_frames += frames_in_batch * config.frame_skip
        data_view = engine.state.data.reshape(-1)

        with torch.no_grad():
            batch = adv_module(data_view)

        # Normalize advantage
        adv = batch.get("advantage")

        # mean of the advantage values
        loc = adv.mean().item()
        # standard deviation of the advantage values
        scale = adv.std().clamp_min(1e-6).item()
        # normalizing the advantage values
        adv = (adv - loc) / scale
        batch.set("advantage", adv)

        # Forward pass A2C loss
        batch = batch.to(device)
        loss = loss_module(batch)
        loss_sum = loss["loss_critic"] + loss["loss_objective"] + loss["loss_entropy"]

        # Backward pass + learning step
        loss_sum.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(list(actor.parameters()) + list(critic.parameters()), max_norm=0.5)
        engine.state.metrics = {
            "loss_sum": loss_sum.item(),
        }
        optim.step()
        optim.zero_grad()

    trainer = Engine(run_single_timestep)

    logger = setup_logging(config)
    logger.info("Configuration: \n%s", pformat(vars(config)))
    trainer.logger = logger

    if config.lr_scheduler:
        trainer.add_event_handler(Events.ITERATION_COMPLETED, scheduler)

    trainer.add_event_handler(
        Events.ITERATION_COMPLETED(every=config.log_every_episodes),
        log_metrics,
        tag="train",
    )

    @trainer.on(Events.ITERATION_STARTED)
    def update_data():
        # print(f"New iteration started")
        trainer.state.data = next(iter(collector))
        trainer.state.collected_frames = 0

    @trainer.on(Events.ITERATION_COMPLETED)
    def log2():
        collector.update_policy_weights_()

    # timesteps = range(config.steps_per_episode)
    trainer.run(epoch_length=int(config.total_frames / config.frames_per_batch), max_epochs=1)


if __name__ == "__main__":
    main()
