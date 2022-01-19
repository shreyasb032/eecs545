import pytest

import deep_q.wordle

TESTWORDS = [
    "APPAA",
    "APPAB",
    "APPAC",
    "APPAD",

    "BPPAB",
    "BPPAC",
    "BPPAD",

    "CPPAB",
    "CPPAC",
    "CPPAD",
]

@pytest.fixture
def wordleEnv():
    env = deep_q.wordle.WordleEnvBase(
        words=TESTWORDS
    )
    return env


def test_reset(wordleEnv):
    wordleEnv.reset(seed=13)


def test_guess_win(wordleEnv):
    wordleEnv.reset(seed=13)
    goal = wordleEnv.goal_word
    new_state, reward, done, _ = wordleEnv.step(goal)
    assert done
    assert wordleEnv.done
    assert reward == 0

    try:
        wordleEnv.step(goal)
        raise ValueError("Shouldn't reach here!")
    except ValueError:
        pass


def test_win_reward(wordleEnv):
    wordleEnv.reset(seed=13)
    goal = wordleEnv.goal_word
    new_state, reward, done, _ = wordleEnv.step((goal+1)%len(wordleEnv.words))
    assert not done
    assert not wordleEnv.done
    assert reward == 0

    new_state, reward, done, _ = wordleEnv.step(goal)
    assert done
    assert wordleEnv.done
    assert reward == deep_q.wordle.REWARD

    try:
        wordleEnv.step(goal)
        raise ValueError("Shouldn't reach here!")
    except ValueError:
        pass


def test_lose_reward(wordleEnv):
    wordleEnv.reset(seed=13)
    goal = wordleEnv.goal_word
    for i in range(1, 6):
        new_state, reward, done, _ = wordleEnv.step((goal + i) % len(wordleEnv.words))
        assert not done
        assert not wordleEnv.done
        assert reward == 0

    new_state, reward, done, _ = wordleEnv.step((goal + 6) % len(wordleEnv.words))
    assert done
    assert wordleEnv.done
    assert reward == -deep_q.wordle.REWARD

    try:
        wordleEnv.step(goal)
        raise ValueError("Shouldn't reach here!")
    except ValueError:
        pass


def test_step(wordleEnv):
    wordleEnv.reset(seed=13)
    wordleEnv.goal_word = 0

    new_state, reward, done, _ = wordleEnv.step(1)
    assert new_state[0] == 1
    # Expect B to be all 1,0,0
    offset = 1+3*5*(ord('B')-ord('A'))
    assert tuple(new_state[offset:offset+15]) == tuple([1, 0, 0]*5)

    # Expect A to be right in position 0 4 and maybe otherwise
    offset = 1
    assert tuple(new_state[offset:offset+15]) == (0,0,1,
                                                  1,0,0,
                                                  1,0,0,
                                                  0,0,1,
                                                  0,1,0)

    # Expect P to be right in position 2 3 and maybe otherwise
    offset = 1 + 3*5*(ord('P') - ord('A'))
    assert tuple(new_state[offset:offset+15]) == (1,0,0,
                                                  0,0,1,
                                                  0,0,1,
                                                  1,0,0,
                                                  0,1,0)

    # Expect C to be maybes
    offset = 1 + 3*5*(ord('C') - ord('A'))
    assert tuple(new_state[offset:offset+15]) == (1,0,0,
                                                  1,0,0,
                                                  1,0,0,
                                                  1,0,0,
                                                  0,1,0)
    new_state, reward, done, _ = wordleEnv.step(1)
    assert new_state[0] == 2
    # Expect B to be all 1,0,0
    offset = 1+3*5*(ord('B')-ord('A'))
    assert tuple(new_state[offset:offset+15]) == tuple([1, 0, 0]*5)

    # Expect A to be right in position 0 4 and maybe otherwise
    offset = 1
    assert tuple(new_state[offset:offset+15]) == (0,0,1,
                                                  1,0,0,
                                                  1,0,0,
                                                  0,0,1,
                                                  0,1,0)

    # Expect P to be right in position 2 3 and maybe otherwise
    offset = 1 + 3*5*(ord('P') - ord('A'))
    assert tuple(new_state[offset:offset+15]) == (1,0,0,
                                                  0,0,1,
                                                  0,0,1,
                                                  1,0,0,
                                                  0,1,0)

    new_state, reward, done, _ = wordleEnv.step(2)
    assert new_state[0] == 3
    # Expect B to be all 1,0,0
    offset = 1+3*5*(ord('B')-ord('A'))
    assert tuple(new_state[offset:offset+15]) == tuple([1, 0, 0]*5)

    # Expect C to be all 1,0,0
    offset = 1+3*5*(ord('C')-ord('A'))
    assert tuple(new_state[offset:offset+15]) == tuple([1, 0, 0]*5)

    # Expect A to be right in position 0 4 and maybe otherwise
    offset = 1
    assert tuple(new_state[offset:offset+15]) == (0,0,1,
                                                  1,0,0,
                                                  1,0,0,
                                                  0,0,1,
                                                  0,1,0)

    # Expect P to be right in position 2 3 and maybe otherwise
    offset = 1 + 3*5*(ord('P') - ord('A'))
    assert tuple(new_state[offset:offset+15]) == (1,0,0,
                                                  0,0,1,
                                                  0,0,1,
                                                  1,0,0,
                                                  0,1,0)

    new_state, reward, done, _ = wordleEnv.step(0)
    assert new_state[0] == 4
    assert done
    assert wordleEnv.done
    assert reward == deep_q.wordle.REWARD