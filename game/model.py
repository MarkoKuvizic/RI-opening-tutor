import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessNet(nn.Module):
    def __init__(self, num_classes):
        super(ChessNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(1, 3), stride=1, padding=(0, 1))
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(1, 3), stride=1, padding=(0, 1))
        self.pool = nn.MaxPool2d(kernel_size=(1, 2), stride=(1, 2))
        
        # Adjust the input size for the fully connected layer based on output from conv layers
        self.fc1 = nn.Linear(32 * 1 * 320, 128)  # Adjust this based on your specific needs
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # Shape will be (batch_size, 16, 1, 640)
        x = self.pool(F.relu(self.conv2(x)))  # Shape will be (batch_size, 32, 1, 320)
        x = x.view(x.size(0), -1)  # Flatten the tensor to (batch_size, 32 * 1 * 320)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
