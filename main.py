from movePredictor import gameProcessor
from movePredictor import movePredictorCnn
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from pprint import pprint

processor = gameProcessor.GameProcessor()
with open('D:\Marko\Downloads\lichess_db_standard_rated_2016-01.pgn/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
    for i in range(10000):
        processor.read_until_string('Event', file)
processor.filter_games()
processor.separate_game_into_positions()
positions = None
positions = gameProcessor.ChessDataset(processor.games)
confidences = None
#confidences = gameProcessor.ConfidenceDataset(processor.games)

num_epochs = 0
batch_size = 32

net = movePredictorCnn.MoveCNN()
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

for epoch in range(num_epochs):
    running_loss = 0.0
    for i in range(0, len(positions), batch_size):
        # Get the inputs and labels for the current batch
        inputs = positions[i:i+batch_size]
        labels = confidences[i:i+batch_size]

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = net(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimize
        loss.backward()
        optimizer.step()

        # Print statistics
        running_loss += loss.item()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(positions):.10f}')
#torch.save(net.state_dict(), "move_prediction_model3.pth")
print('Finished Training')

from movePredictor import gameProcessor
from movePredictor import movePredictorCnn
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

model = movePredictorCnn.MoveCNN()
model.load_state_dict(torch.load('move_prediction_model2.pth'))
print(positions[3])
print(model(positions[3]))