import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model import ChessNet
from dataset import ChessDataset
from torchvision import transforms
from game_processor import GameProcessor

# Define hyperparameters
batch_size = 32
learning_rate = 0.001
epochs = 10
max_moves_per_game = 10

# Initialize dataset and model
processor = GameProcessor()
with open('C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
    for i in range(1000):  # Adjust the number of games to read as needed
        processor.read_until_string('Event', file)
processor.filter_games()
processor.separate_game_into_positions()

# Split the dataset into training and validation sets
train_games = processor.games[:700]
val_games = processor.games[300:]

print(f"Number of training games: {len(train_games)}")
print(f"Number of validation games: {len(val_games)}")

train_dataset = ChessDataset(train_games, max_moves_per_game)
val_dataset = ChessDataset(val_games, max_moves_per_game)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


num_classes = len(train_dataset.opening_to_label)
model = ChessNet(num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
model.train()
for epoch in range(epochs):
    running_loss = 0.0
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        # Optionally, print loss or other metrics
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}')

# Save trained model
torch.save(model.state_dict(), 'chess_model.pth')

# Evaluation
def evaluate(model, data_loader, criterion):
    model.eval()
    correct = 0
    total = 0
    total_loss = 0.0
    with torch.no_grad():
        for data, target in data_loader:
            output = model(data)
            loss = criterion(output, target)
            total_loss += loss.item()
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    accuracy = correct / total
    avg_loss = total_loss / len(data_loader)
    return accuracy, avg_loss

val_accuracy, val_loss = evaluate(model, val_loader, criterion)
print(f'Validation Accuracy: {val_accuracy:.4f}, Validation Loss: {val_loss:.4f}')
