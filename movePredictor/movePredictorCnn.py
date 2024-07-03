import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

class MoveCNN(nn.Module):
    def __init__(self):
        super(MoveCNN, self).__init__()
        self.conv1 = nn.Conv1d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 64)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        #x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        #x = F.max_pool2d(x, 2)
        x = F.relu(self.conv3(x))
        x = x.view(-1, 128 * 8 * 8)  
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

