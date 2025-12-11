import sys
from pathlib import Path

import timm
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchmetrics.classification
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from kvasircapsuleloader import KvasirCapsuleDataset


def evaluate(device: torch.device, model, dataloader):
    model.eval()
    acc_multi_micro = torchmetrics.classification.Accuracy(
        task="multiclass", num_classes=14, average="micro"
    ).to(device)
    acc_multi_macro = torchmetrics.classification.Accuracy(
        task="multiclass", num_classes=14, average="macro"
    ).to(device)
    acc_multi_weighted = torchmetrics.classification.Accuracy(
        task="multiclass", num_classes=14, average="weighted"
    ).to(device)
    with torch.no_grad():
        for images, _, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            acc_multi_micro(predicted, labels)
            acc_multi_macro(predicted, labels)
            acc_multi_weighted(predicted, labels)
    print(f"Micro    avg. accuracy: {acc_multi_micro.compute():.4f}")
    print(f"Macro    avg. accuracy: {acc_multi_macro.compute():.4f}")
    print(f"Weighted avg. accuracy: {acc_multi_weighted.compute():.4f}")


def train(
    device: torch.device,
    model,
    dataloader_train,
    dataloader_val,
    criterion,
    optimizer,
    num_epochs=10,
):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, _, labels in tqdm(dataloader_train):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(
            f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader_train):.4f}"
        )
        evaluate(device, model, dataloader_val)


def main():
    num_classes = 14
    model = timm.create_model("resnet50", pretrained=True)

    model.fc = nn.Linear(model.fc.in_features, num_classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    dataset = KvasirCapsuleDataset()

    # TODO random weighted sampling
    train_loader = DataLoader(dataset.train(), batch_size=8, shuffle=True)
    val_loader = DataLoader(dataset.val(), batch_size=32, shuffle=False)
    test_loader = DataLoader(dataset.test(), batch_size=32, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train(device, model, train_loader, val_loader, criterion, optimizer, num_epochs=10)
    print("Test set:")
    evaluate(device, model, test_loader)


if __name__ == "__main__":
    main()
