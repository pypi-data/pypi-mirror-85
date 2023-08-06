# Python-NBS
A python library for reading NBS files

Based on NBS Version: 4(Current version used by Open Note Block Studio)

## What is NBS

> The .nbs format (Note Block Song) was created to work with Minecraft Note Block Studio, and contains data about how note blocks are laid out in the program to form a song.

From [opennbs.org](https://opennbs.org/nbs).

## Installation

```bash
pip install Python-NBS
```

## Usage

```Python
import python_nbs.nbs as nbs
import pprint
nbs_file = nbs.NBS("file.nbs")

# print song name
print(nbs_file.song_name)

# print all note blocks
pprint(nbs_file.note_blocks)
```

See docstring for the available instance variables.