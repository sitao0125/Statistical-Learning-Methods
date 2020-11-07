from pathlib import Path
import sys
import os
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))
from utils import *

def backward(state2state, state2observation, initial_state, observation):
    """
    Given a HMM with parameter (state2state, state2observation, initial_state)
    and the observation,
    return the probability of the observation generated by this HMM

    state2state is a matrix shaped of [state_size, state_size]
    state2observation is a matrix shaped of [state_size, observation_size]
    initial_state is a tensor shaped of [state_size], whose each dimension means the probability of each state
    observation is a tensor shaped of [sequence_length]
    observation_size is the number of all the possible observations

    the return value consists of two parts:
    the probability of the observation,
    and a sequence of probability of each state of each step
    """
    state_size, _ = state2state.shape
    sequence_length, = observation.shape

    seq_state_prob = np.zeros([sequence_length, state_size])
    state_prob = np.ones_like(initial_state)
    for i in range(sequence_length - 1, -1, -1):
        o = observation[i]
        # given the observation of the following steps, get the probability of this state
        state_prob = state2state @ state_prob
        seq_state_prob[i] = state_prob
        # given the observation of this step, get the probability of this state
        state_prob *= state2observation[:, o]
    state_prob *= initial_state
    return sum(state_prob), seq_state_prob


if __name__ == '__main__':
    A = np.array(
        [[.5, .2, .3],
         [.3, .5, .2],
         [.2, .3, .5]]
        )
    B = np.array(
        [[.5, .5],
         [.4, .6],
         [.7, .3]]
        )
    pi = np.array([.2, .4, .4])
    observation = np.array([0, 1, 0])
    print(backward(A, B, pi, observation)[0])