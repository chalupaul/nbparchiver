#!/usr/bin/env bash
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    git \
    pipx

curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"
echo 'export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc
eval "$(pyenv init --path)"
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
eval "$(pyenv virtualenv-init -)"
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
pyenv install $(cat .python-version)
pipx ensurepath
pipx install poetry
poetry install

exec $SHELL