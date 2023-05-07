FROM continuumio/miniconda3:23.3.1-0

# Install nodejs v18
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install pnpm and few python code-generator deps
# Taken from .github/workflows/ci.yml
RUN pip install wheel setuptools pip -Uqq && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install pytorch-ignite pyyaml albumentations image_dataset_viz pytest transformers datasets tensorboard && \
    npm i -g pnpm
