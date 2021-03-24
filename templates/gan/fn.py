import torch


def update(netD, netG, device, optimizerD, optimizerG, loss_fn, config, real_labels, fake_labels):

    # The main function, processing a batch of examples
    def step(engine, batch):

        # unpack the batch. It comes from a dataset, so we have <images, labels> pairs. Discard labels.
        real, _ = batch
        real = real.to(device)

        # -----------------------------------------------------------
        # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
        netD.zero_grad()

        # train with real
        output = netD(real)
        errD_real = loss_fn(output, real_labels)
        D_x = output.mean().item()

        errD_real.backward()

        # get fake image from generator
        noise = torch.randn(config.batch_size, config.z_dim, 1, 1, device=device)
        fake = netG(noise)

        # train with fake
        output = netD(fake.detach())
        errD_fake = loss_fn(output, fake_labels)
        D_G_z1 = output.mean().item()

        errD_fake.backward()

        # gradient update
        errD = errD_real + errD_fake
        optimizerD.step()

        # -----------------------------------------------------------
        # (2) Update G network: maximize log(D(G(z)))
        netG.zero_grad()

        # Update generator. We want to make a step that will make it more likely that discriminator outputs "real"
        output = netD(fake)
        errG = loss_fn(output, real_labels)
        D_G_z2 = output.mean().item()

        errG.backward()

        # gradient update
        optimizerG.step()

        return {"errD": errD.item(), "errG": errG.item(), "D_x": D_x, "D_G_z1": D_G_z1, "D_G_z2": D_G_z2}

    return step
