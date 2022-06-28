import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):  # defines size and shape of neural net, input layer --> hidden layer, hidden layer --> output layer
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.liner1 = nn.Linear(input_size, hidden_size)
        self.liner2 = nn.Linear(hidden_size, output_size)


    def forward(self, x):  # creates feed forward function
        x = F.relu(self.liner1(x))  # relu is applied each element in a tensor. If n < 0 then: n = 0. If n >= 0 then: do nothing.
        x = self.liner2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)  # implementation of stochastic optimisation algorthim.
        # Stochastic search and optimization pertains to problems where there is randomness noise in the measurements
        # provided to the algorithm and/or there is injected (Monte Carlo) randomness in the algorithm itself.
        self.criterion = nn.MSELoss()
        # the average squared difference between the estimated values and the actual value. MSE is a risk function, corresponding to the expected value of the squared error loss.

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            # .unsqueeze creates a tensor of size 1 at position specified.
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )  # tuple defined with only one value

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                # 2: Q_new = reward + gamma * max(next_predicted Q value) -> only do this if not done
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new


        # pred.clone()
        # preds[argmax(action)] = Q_new
        # sets the next predicted move with the next Q value
        # @ the index specified with the largest value in 'action' (0,0,1)/(0,1,0)/(1,0,0)
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)  # (Qnew, Q)
        loss.backward()

        self.optimizer.step()