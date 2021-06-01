from torch import nn


class Net(nn.Module):
    """A base class for both generator and the discriminator.
    Provides a common weight initialization scheme.
    """

    def weights_init(self):
        for m in self.modules():
            classname = m.__class__.__name__

            if "Conv" in classname:
                m.weight.data.normal_(0.0, 0.02)

            elif "BatchNorm" in classname:
                m.weight.data.normal_(1.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, x):
        return x


class Generator(Net):
    """Generator network.
    Args:
        nf (int): Number of filters in the second-to-last deconv layer
    """

    def __init__(self, z_dim, nf, nc):
        super(Generator, self).__init__()

        self.net = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(
                in_channels=z_dim,
                out_channels=nf * 8,
                kernel_size=4,
                stride=1,
                padding=0,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 8),
            nn.ReLU(inplace=True),
            # state size. (nf*8) x 4 x 4
            nn.ConvTranspose2d(
                in_channels=nf * 8,
                out_channels=nf * 4,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 4),
            nn.ReLU(inplace=True),
            # state size. (nf*4) x 8 x 8
            nn.ConvTranspose2d(
                in_channels=nf * 4,
                out_channels=nf * 2,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 2),
            nn.ReLU(inplace=True),
            # state size. (nf*2) x 16 x 16
            nn.ConvTranspose2d(
                in_channels=nf * 2,
                out_channels=nf,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf),
            nn.ReLU(inplace=True),
            # state size. (nf) x 32 x 32
            nn.ConvTranspose2d(
                in_channels=nf,
                out_channels=nc,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

        self.weights_init()

    def forward(self, x):
        return self.net(x)


class Discriminator(Net):
    """Discriminator network.
    Args:
        nf (int): Number of filters in the first conv layer.
    """

    def __init__(self, nc, nf):
        super(Discriminator, self).__init__()

        self.net = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(
                in_channels=nc,
                out_channels=nf,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nf) x 32 x 32
            nn.Conv2d(
                in_channels=nf,
                out_channels=nf * 2,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nf*2) x 16 x 16
            nn.Conv2d(
                in_channels=nf * 2,
                out_channels=nf * 4,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nf*4) x 8 x 8
            nn.Conv2d(
                in_channels=nf * 4,
                out_channels=nf * 8,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(nf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nf*8) x 4 x 4
            nn.Conv2d(
                in_channels=nf * 8,
                out_channels=1,
                kernel_size=4,
                stride=1,
                padding=0,
                bias=False,
            ),
            nn.Sigmoid(),
        )

        self.weights_init()

    def forward(self, x):
        output = self.net(x)
        return output.view(-1, 1).squeeze(1)
