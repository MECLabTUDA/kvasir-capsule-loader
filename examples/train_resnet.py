import copy
import sys
from pathlib import Path

import click
import timm
import torch
import torch.nn as nn
import torch.optim as optim
import torchmetrics.classification
from torch.utils.data import DataLoader
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from kvasircapsuleloader import KvasirCapsuleDataset, fix_random_seed


def evaluate(device: torch.device, model: nn.Module, dataloader: DataLoader) -> float:
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
    click.secho(f"  Micro    avg. accuracy: {acc_multi_micro.compute():.4f}", fg="blue")
    click.secho(f"  Macro    avg. accuracy: {acc_multi_macro.compute():.4f}", fg="blue")
    click.secho(
        f"  Weighted avg. accuracy: {acc_multi_weighted.compute():.4f}", fg="blue"
    )
    return acc_multi_macro.compute()


def train(
    device: torch.device,
    model: nn.Module,
    dataloader_train: DataLoader,
    dataloader_val: DataLoader,
    criterion,
    optimizer: optim.Optimizer,
    num_epochs: int = 100,
) -> nn.Module:
    best_acc = 0
    best_model = model
    for epoch in range(num_epochs):
        print()
        click.secho(f"Epoch [{epoch+1}/{num_epochs}]", fg="blue")
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

        click.secho(f"  Loss: {running_loss/len(dataloader_train):.4f}", fg="blue")
        acc = evaluate(device, model, dataloader_val)
        if acc > best_acc:
            best_model = copy.deepcopy(model)
    return best_model


@click.command()
@click.option("--lr", "-L", type=float, default=1e-3)
@click.option(
    "--model-name",
    "-M",
    type=click.Choice(["resnet50", "resnet80", "resnet152"]),
    default="resnet50",
)
@click.option("--epochs", "-E", type=int, default=100)
def main(lr: float, model_name: str, epochs: int):
    fix_random_seed()

    dataset = KvasirCapsuleDataset()
    num_classes = dataset.metadata.num_classes()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = timm.create_model(model_name, pretrained=True, num_classes=num_classes)
    model = model.to(device)

    # TODO random weighted sampling
    train_loader = DataLoader(
        dataset.train(), batch_size=8, shuffle=True, num_workers=4
    )
    val_loader = DataLoader(dataset.val(), batch_size=32, shuffle=False)
    test_loader = DataLoader(dataset.test(), batch_size=32, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    print()
    click.secho(f"Training {model_name}:", fg="blue")
    best_model = train(
        device, model, train_loader, val_loader, criterion, optimizer, num_epochs=epochs
    )

    print()
    click.secho("Test set accuracy of best performing model:", fg="green")
    evaluate(device, best_model, test_loader)


if __name__ == "__main__":
    main()
