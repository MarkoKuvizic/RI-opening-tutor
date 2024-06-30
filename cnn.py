import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.feature_extraction = nn.Sequential(
            #ulaz 28x28x1, izlaz 28x28x16
            nn.Conv2d(
                # slike su grayscale pa je broj kanala 1, da je slika RGB broj kanala bi bio 3
                in_channels=1,
                # broj izlaznih kanala, 16 filtera -> 16 mapa osobina (kanala)
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            nn.ReLU(),
            # sloj sažimanja će promeniti prve dve dimenzije mapa osobina (visinu i širinu), ali ne i treću (broj kanala)
            #ulaz 28x28x16, izlaz 14x14x16
            nn.MaxPool2d(kernel_size=2),

            # nije potrebno navođenje naziva argumenata, kao u kodu iznad, moguće je samo proslediti njihove vrednosti
            #ulaz 14x14x16, izlaz 14x14x32
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            #ulaz 14x14x32, izlaz 7x7x32
            nn.MaxPool2d(2),
        )

        self.flatten = nn.Flatten()

        # potpuno povezan sloj
        self.classification_head = nn.Linear(7*7*32, 10)

    def forward(self, x):
        x = self.feature_extraction(x)
        # prebacivanje dimenzija izlaza feature_extraction sloja u (batch_size, 7*7*32) kako bi odgovaralo dimenzijama ulaza klasifikacionog sloja
        x = self.flatten(x)