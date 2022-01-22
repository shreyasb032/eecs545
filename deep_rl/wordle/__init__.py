from gym.envs.registration import (
    registry,
    register,
    make,
    spec,
    load_env_plugins as _load_env_plugins,
)


# Classic
# ----------------------------------------

register(
    id="WordleEnv10-v0",
    entry_point="wordle.wordle:WordleEnv10",
    max_episode_steps=200,
)

register(
    id="WordleEnv100-v0",
    entry_point="wordle.wordle:WordleEnv100",
    max_episode_steps=500,
)

register(
    id="WordleEnv100Training-v0",
    entry_point="wordle.wordle:WordleEnv100Training",
    max_episode_steps=500,
)

register(
    id="WordleEnv1000-v0",
    entry_point="wordle.wordle:WordleEnv1000",
    max_episode_steps=1000,
)

register(
    id="WordleEnv1000Training-v0",
    entry_point="wordle.wordle:WordleEnv1000Training",
    max_episode_steps=1000,
)

register(
    id="WordleEnv1000Training1000-v0",
    entry_point="wordle.wordle:WordleEnv1000Training1000",
    max_episode_steps=1000,
)

register(
    id="WordleEnv-v0",
    entry_point="wordle.wordle:WordleEnv",
    max_episode_steps=1000,
)