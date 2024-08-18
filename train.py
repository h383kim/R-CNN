import time
import copy
import torch
from torch.utils.data import DataLoader
from torch.optim import Optimizer


def train(model: torch.nn.Module,
          dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module=nn.CrossEntropyLoss()):
    # Put the model into train mode
    model.train()
    train_loss, correct, train_acc = 0, 0, 0

    for batch, (X, y) in enumerate(dataloader):
        # Send X, y into the device
        X, y = X.to(DEVICE), y.to(DEVICE)

        # forward pass
        pred_probs = model(X)

        # Calculate the loss
        loss = loss_fn(pred_probs, y)
        train_loss += loss.item()

        # Optimizer zero_grad
        optimizer.zero_grad()

        # Loss backward
        loss.backward()

        #optimizer step
        optimizer.step()

        pred = torch.argmax(pred_probs, dim=1)
        correct += pred.eq(y.view_as(pred)).sum().item()

    train_loss /= len(dataloader) # (Sum of train_loss for each batch) / (# of batches)
    train_acc = 100. * correct / len(dataloader.dataset)
    return train_loss, train_acc


def train_baseline(model: torch.nn.Module, 
                   train_dataloader: torch.utils.data.DataLoader, 
                   optimizer: torch.optim.Optimizer,
                   loss_fn: torch.nn.Module=nn.CrossEntropyLoss(),
                   num_epochs: int=30):
    best_acc = 0.0
    best_model_wts = copy.deepcopy(model.state_dict())
    
    for epoch in range(1, num_epochs + 1):
        start_time = time.time()
        # Train the model and print save the results
        train_loss, train_acc = train(model=model,
                                      dataloader=train_dataloader, 
                                      optimizer=optimizer,
                                      loss_fn=loss_fn)
        
        if train_acc > best_acc:
            best_acc = train_acc
            best_model_wts = copy.deepcopy(model.state_dict())
            
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"------------ epoch {epoch} ------------")
        print(f"Train loss: {train_loss:.4f} | Train acc: {train_acc:.2f}%")
        print(f"Time taken: {time_elapsed / 60:.0f}min {time_elapsed % 60:.0f}s")
        
    model.load_state_dict(best_model_wts)
    return model 