FROM continuumio/miniconda3:23.3.1-0

# Install nodejs v18
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install pnpm and few python code-generator deps
# Taken from .github/workflows/ci.yml
RUN pip install --upgrade wheel setuptools pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install pytorch-ignite pyyaml albumentations image_dataset_viz pytest transformers datasets tensorboard

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get install -y unzip && \
    npm i -g pnpm && \
    # We may want to match playwright-chromium version from package.json
    npm i -g playwright-chromium@1.33.0 && \
    npx playwright install --with-deps
