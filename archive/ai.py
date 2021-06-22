import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable


# Neural Network
class Network(nn.Module):
    def __init__(self, input_size, outputs):
        super(Network, self).__init__()
        self.input_size = input_size
        self.outputs = outputs
        self.hidden_one = nn.Linear(input_size, 30)
        self.hidden_two = nn.Linear(30, outputs)

    def forward(self, state):
        '''Forward propagation method.'''
        x = F.relu(self.hidden_one(state))
        return self.hidden_two(x)  # returning Q-values


# Experience Replay
class ExpReplay(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        '''Adds an event to experience replay memory.'''
        self.memory.append(event)

        if len(self.memory) > self.capacity:
            del self.memory[0]  # remove the first event if memory greater than capacity

    def sample(self, batch_size):
        '''Return samples from the memory as a tensor.'''
        samples = zip(*random.sample(self.memory, batch_size))  # ((1,2,3), (4,5,6)) -> ((1,4), (3,5), (4, 6))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)  # convert each batch (that is now aligned) to a torch variable


# The main class that we will use.
class DeepQLearning:
    def __init__(self, input_size, outputs, gamma):
        self.gamma = gamma
        self.rewards = []
        self.model = Network(input_size, outputs)
        self.memory = ExpReplay(100000)
        self.optimiser = optim.Adam(self.model.parameters(), lr=0.001)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)  # 0 -> fake dimension of the state ~ unsqueeze creates fake dimension
        self.last_action = 0
        self.last_reward = 0

    def select_action(self, state):
        '''Selects the action using the softmax activator.'''
        probs = F.softmax(self.model(Variable(state, volatile=True)) * 100)  # Temperature = 100 -> degree of certainty
        action = probs.multinomial()  # randomly draw from the probabilities of each Q-Value and gives a fake batch
        return action.data[0, 0]  # action is found at [0, 0]

    def learn(self, batch_state, batch_next_state, batch_action, batch_reward):
        '''Conduct Q-learning'''
        # get prediction
        outs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)  # 1 -> fake dimension of the action, squeeze to kill fake dimension to get a tensor

        # calculate target
        next_out = self.model(batch_next_state).detach().max(1)[0]  # needed for target equation -> obtain max Q-value of next state with respect to action
        target = self.gamma * next_out + batch_reward

        # calculate loss, backpropagate and adjust weights
        td_loss = F.smooth_l1_loss(outs, target)
        self.optimiser.zero_grad()  # reinitialise the optimiser at each iteration of loop
        td_loss.backward(retain_variables=True)
        self.optimiser.step()  # adjust weights

    def update(self, reward, new_signal):
        '''Update the valeus of the transitions and the rewards and returns the action.'''
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push((self.last_state, new_state, torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))  # add the transtion into memory
        action = self.select_action(new_state)  # select action based of new_state

        if len(self.memory.memory) > 100:  # if we have more than 100 elements in memory, we need to start learning
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(100)
            self.learn(batch_state, batch_next_state, batch_action, batch_reward)

        # update "last" attributes
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.rewards.append(reward)

        if len(self.rewards) > 1000:
            del self.rewards[0]

        return action

    def score(self):
        '''Compute the mean of all of the rewards'''
        return sum(self.rewards)/(len(self.rewards)) if (len(self.rewards)) != 0 else 0

    def save(self):
        '''Saves our model/network and the optimiser in a file.'''
        torch.save({"state_dict": self.model.state_dict(),
                    "optimiser": self.optimiser.state_dict(),
                   }, "last_brain.pth")

        print("Brain saved!")

    def load(self):
        '''Loads the model/network and the optimiser.'''
        if os.path.isfile("last_brain.pth"):
            checkpoint = torch.load("last_brain.pth")
            self.model.load_state_dict(checkpoint["state_dict"])
            self.optimiser.load_state_dict(checkpoint["optimiser"])
            print("Brain loaded!")

        else:
            print("Brain not found.")
