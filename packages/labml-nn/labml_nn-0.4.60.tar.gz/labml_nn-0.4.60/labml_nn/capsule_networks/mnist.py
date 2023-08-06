"""
# Classify MNIST digits with Capsule Networks

This paper implements the experiment described in paper
[Dynamic Routing Between Capsules](https://arxiv.org/abs/1710.09829).
"""

import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data

from labml import experiment, tracker
from labml.configs import option
from labml.utils.pytorch import get_device
from labml_helpers.datasets.mnist import MNISTConfigs
from labml_helpers.device import DeviceConfigs
from labml_helpers.module import Module
from labml_helpers.train_valid import TrainValidConfigs, BatchStep
from labml_nn.capsule_networks import Squash, Router, MarginLoss


class MNISTCapsuleNetworkModel(Module):
    """
    ## Model for classifying MNIST digits
    """
    def __init__(self):
        super().__init__()
        # First convolution layer has $256$, $9 \times 9$ convolution kernels
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=256, kernel_size=9, stride=1)
        # The second layer (Primary Capsules) s a convolutional capsule layer with $32$ channels
        # of convolutional $8D$ capsules ($8$ features per capsule)
        # That is, each primary capsule contains 8 convolutional units with a 9 × 9 kernel and a stride of 2.
        # In order to implement this we create a convolutional layer with $32 \times 8$ channels and
        # reshapes and permutate it's output to get the capsules of $8$ features each
        self.conv2 = nn.Conv2d(in_channels=256, out_channels=32 * 8, kernel_size=9, stride=2, padding=0)
        self.squash = Squash()

        # Routing layer gets the $32 \times 6 \times 6$ primary capsules and produces $10$ capsules.
        # Each of the primary capsules have $8$ features, while output capsules (Digit Capsules)
        # have $16$ features.
        # The routing algorithm iterates $3$ times.
        self.digit_capsules = Router(32 * 6 * 6, 10, 8, 16, 3)

        # This is the decoder mentioned in the paper.
        # It takes the outputs of the $10$ digit capsules, each with $16$ features to reproduce the
        # image. It goes through linear layers of sizes $512% and $1024$ with $ReLU$ activations.
        self.decoder = nn.Sequential(
            nn.Linear(16 * 10, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 784),
            nn.Sigmoid()
        )

    def forward(self, data: torch.Tensor):
        """
        `data` are the MNIST images, with shape `[batch_size, 1, 28, 28]`
        """
        # Pass through the first convolution layer.
        # Output of this layer has shape `[batch_size, 256, 20, 20]`
        x = F.relu(self.conv1(data))
        # Pass through the second convolution layer.
        # Output of this has shape `[batch_size, 32 * 8, 6, 6]`.
        # *Note that this layer has a stride length of $2$.
        x = self.conv2(x)

        # Resize and permutate to get the capsules
        caps = x.view(x.shape[0], 8, 32 * 6 * 6).permute(0, 2, 1)
        # Squash the capsules
        caps = self.squash(caps)
        # Take them through the router to get digit capsules.
        # This has shape `[batch_size, 10, 16]`.
        caps = self.digit_capsules(caps)

        # Get masks for reconstructioon
        with torch.no_grad():
            # The prediction by the capsule network is the capsule with longest length
            pred = (caps ** 2).sum(-1).argmax(-1)
            # Create a mask to maskout all the other capsules
            mask = torch.eye(10, device=data.device)[pred]

        # Mask the digit capsules to get only the capsule that made the prediction and
        # take it through decoder to get reconstruction
        reconstructions = self.decoder((caps * mask[:, :, None]).view(x.shape[0], -1))
        # Reshape the reconstruction to match the image dimensions
        reconstructions = reconstructions.view(-1, 1, 28, 28)

        return caps, reconstructions, pred


class CapsuleNetworkBatchStep(BatchStep):
    """
    ## Training step
    """
    def __init__(self, *, model, optimizer):
        super().__init__(model=model, optimizer=optimizer, loss_func=None, accuracy_func=None)
        self.reconstruction_loss = nn.MSELoss()
        self.margin_loss = MarginLoss(n_labels=10)

    def calculate_loss(self, batch: any, state: any):
        """
        This method gets called by the trainer
        """
        device = get_device(self.model)

        # Get the images and labels and move them to the model's device
        data, target = batch
        data, target = data.to(device), target.to(device)

        # Collect statistics for logging
        stats = {'samples': len(data)}

        # Run the model
        caps, reconstructions, pred = self.model(data)

        # Calculate the total loss
        loss = self.margin_loss(caps, target) + 0.0005 * self.reconstruction_loss(reconstructions, data)

        stats['correct'] = pred.eq(target).sum().item()
        stats['loss'] = loss.detach().item() * stats['samples']
        tracker.add("loss.", loss)

        return loss, stats, None


class Configs(MNISTConfigs, TrainValidConfigs):
    """
    Configurations with MNIST data and Train & Validation setup
    """
    batch_step = 'capsule_network_batch_step'
    device: torch.device = DeviceConfigs()
    epochs: int = 10
    model = 'capsule_network_model'


@option(Configs.model)
def capsule_network_model(c: Configs):
    """Configure the model"""
    return MNISTCapsuleNetworkModel().to(c.device)


@option(Configs.batch_step)
def capsule_network_batch_step(c: TrainValidConfigs):
    """Configure the training step"""
    return CapsuleNetworkBatchStep(model=c.model, optimizer=c.optimizer)


def main():
    """
    Run the experiment
    """
    conf = Configs()
    experiment.create(name='mnist_latest')
    experiment.configs(conf, {'optimizer.optimizer': 'Adam',
                              'device.cuda_device': 1})
    with experiment.start():
        conf.run()


if __name__ == '__main__':
    main()
