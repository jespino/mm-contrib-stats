## Mattermost Contributors Stats

This repository contains a set of scripts to get stats and summarize
information about the contributions made to mattermost by the open source
community.

### Installation

To install it you need to have python and pip properly installed in your
system, and this repo cloned, after that you only need to execute:

```sh
pip install -r requirements.txt
```

### Usage example

First of all you need to have a github access token, you can see how to obtain one in [the github help page for create personal tokens](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line). The token must have at least the `repo` permissions and the `read:org` persission.

Then you have to extract the contributions from the repositories that you want to take into consideration. For example:

```sh
python main.py contributors --token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
    --org mattermost \
    --repo desktop \
    --repo mattermost-redux \
    --repo mattermost-webapp \
    --repo mattermost-server \
    --repo mattermost-mobile \
    --json > contributions.json
```

Then you have to get the staff (you can include or exclude members based on the members obtained by github, for example exclude ex-staff and include core commiters that are from the community). To do that you can execute the following command:

```sh
python main.py staff --token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
    --org mattermost \
    --json > staff.json
```

Finally you can generate a summary of the contributions using the following command:

```sh
python summary.py --staff-json staff.json --contributions-json contributions.json
```
