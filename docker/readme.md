# Docker image for local development

## Build development docker image

```bash
# Assuming the current folder to be code-generator source root folder
cd docker
docker build --tag pytorchignite/codegenerator:dev .
cd ../
```

## Run the image as a container

Assumptions:
- `$PWD` is code-generator source root folder
- To replace `/host/path/to/data` with a path to the input data (for example CIFAR10 and/or VOCdevkit etc), e.g. `/mnt/data`

```bash
# Assuming the current folder to be code-generator source root folder
docker run --name=codegen-dev -it -v $PWD:/code -w /code -v /data:/host/path/to/data --network=host --ipc=host pytorchignite/codegenerator:dev /bin/bash
```

Inside the container we can install all other project related dependencies:
```bash
git config --global --add safe.directory /code

pnpm i --frozen-lockfile --color
pnpm build
npx playwright install
npx playwright install-deps
pnpm test:ci
```