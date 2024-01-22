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
docker run --name=codegen-dev -it -v $PWD:/code -w /code -v /host/path/to/data:/data --network=host --ipc=host pytorchignite/codegenerator:dev /bin/bash
```

Inside the container we can install all other project dependencies:

```bash
git config --global --add safe.directory /code

pnpm i --frozen-lockfile --color
pnpm build

bash scripts/run_code_style.sh install
```

- Local app deployment

```bash
pnpm dev
```

- Run ci tests locally

```bash
pnpm dev &
pnpm test

sh ./scripts/run_tests.sh unzip
sh ./scripts/run_tests.sh simple vision-classification
```


## Troubleshooting

### Low Disk Space on Windows

**Issue:** Faced the Issue of Low Space on C Drive, since this is where all the Docker and Linux Distributions of WSL are stored.

**Solution:**
- To shift WSL to D Drive, Followed the instructions: [Is there any way to install WSL on non-C drive?](https://superuser.com/a/1572837)
- To shift Docker and Docker Desktop over to D Drive, Followed the instructions: [How can I change the location of docker images when using Docker Desktop on WSL2 with Windows 10 Home?](https://stackoverflow.com/a/63752264/17397774)

---
After setting up Docker and whatever the issue with space and docker is:

Enable wsl integration with Ububtu in Settings -> Resources -> WSL Integration [Image Here](https://imgur.com/a/t07UovC)

In the WSL Ubuntu terminal, Create a container from the image that we created using:
```bash
docker run -p 3000:3000 -p 5000:5000 --name=codegen-dev -it -v $PWD:/code -w /code -v /path/to/data:/data --ipc=host pytorchignite/codegenerator:dev /bin/bash
```

For Terminal beautification and git branch parsing:
```bash
apt-get upgrade && apt-get update
apt-get install vim
cd
vi .bashrc
```

Insert the script at the end of the `.bashrc`
```bash
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\[\033[0;32m\]\u@\h \[\033[0;33m\]\w\[\033[0;36m\]\$(parse_git_branch)\[\033[0;37m\]\n$ \[\033[0;37m\]"
```

```bash
source .bashrc
```

**The data is stored in `/root/data`**

## Instruction for Debugging:

Inside the container we can install all other project dependencies:

```bash
git config --global --add safe.directory /code

pnpm i --frozen-lockfile --color
pnpm build

bash scripts/run_code_style.sh install
```

Local app deployment, to work in Windows through the layers of docker, wsl and windows, use `--host`

```bash
pnpm dev --host
```

In Project Directory:
```bash
pnpm test:ci

sh ./scripts/run_tests.sh unzip
```

Run sample tests:
```bash
sh ./scripts/run_tests.sh simple vision-classification
```

`pnpm test:ci` would have created the actual code which we can debug! What this does is actually simple in the project directory there exists a directory `__tests__` which contains the `js` code to download the actual code!
What happens is that `pnpm` server is started at `http://localhost:5000` and the scripts accordingly are downloaded using `js` 

>If we want the live changes to be reflected, then we will have to change the line:
>`await page.goto(http://localhost:5000/create)` to `await page.goto(http://localhost:3000/create)`
>Before running this, we will first have to run `pnpm dev` so that the local server is started at port `3000` which will be reflecting the live changes, so as mentioned above, since the `js` at `__tests__` are downloading the actual code hosted at the website, it will download the live changes.

**For Debugging:**
In the file: `.vscode/launch.json`
```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "Python: Remote Attach",
			"type": "python",
			"request": "attach",
			"connect": {
				"host": "localhost",
				"port": 3000
			},
			"pathMappings": [
				{
					"localRoot": "${workspaceFolder}/",
					"remoteRoot": "/code"
				}
			],
			"justMyCode": false
		}
	]
}
```

```bash
pip install debugpy
```

Go to the template and the test you want to run, in the `dist-tests/` directory, from there we can debug using the command: (Modify according to your needs, this is for the simple tests)
```bash
cd dist-tests/vision-segmentation-simple/
python -m debugpy --listen 0.0.0.0:3000 --wait-for-client main.py --data_path /root/data --train_batch_size 2 --eval_batch_size 2 --num_workers 2 --max_epochs 2 --train_epoch_length 4 --eval_epoch_length 4
```

>For vision segmentation, we will first have to download the datasets in the `root/data/` folder
