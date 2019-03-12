"""
    TO-DO
    -----
    - Define visualize function including 2D PCA and 3D PCA with options to export images
"""

import torch
import numpy as np
from tqdm import tqdm

def get_bar(percent, total=30):
    """
        Function Objective
        ------------------
        Utility function for generating progress bar
        
        Non-defaut parameters
        ---------------------
        percent is a number indicates percentage of completion
        
        Default parameters
        ------------------
        total is a number of progress bar length
        
        Returns
        -------
        String of progress bar
        
    """
    
    bar = "["
    for i in range(int(total*percent/100)):
        bar += "="
    if percent != 100:
        bar += ">"
    for i in range(total - int(total*percent/100) -1):
        bar += " "
    bar += "]"
    return bar

def extract_embeddings(dataloader, model, feature_size, device, verbose=False):
    with torch.no_grad():
        model.eval()
        embeddings = np.zeros((len(dataloader.dataset), feature_size))
        labels = np.zeros(len(dataloader.dataset))
        k = 0
        if verbose:
            pbar = tqdm(total=len(dataloader.dataset), position=0)
        for images, target in dataloader:
            images = images.to(device)
            embeddings[k:k + len(images)
                       ] = model.get_embedding(images).data.cpu().numpy()
            labels[k:k + len(images)] = target.numpy()
            k += len(images)
            if verbose:
                pbar.update(len(images))
        if verbose:
            pbar.close()
    return embeddings, labels