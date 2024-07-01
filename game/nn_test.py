from train import train, evaluate
import torch
from model import ChessNet
from dataset import ChessDataset

if __name__ == "__main__":
    # Training phase
    train()

    # Evaluation phase
    evaluate()