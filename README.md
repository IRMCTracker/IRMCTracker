# IRMCTracker

A discord bot  for tracking Iranian Minecraft servers and showing the statistics of them

## Installation

Installation needs a valid installation of **Python > 3.6**

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install *requirments.txt*

```bash
pip install -r requirments.txt
```

### Before running the bot
Copy _storage/config/.env.sample_ to to _storage/config/.env_ and update tokens/prefixes etc as desired

### After running the bot
1. Add servers to tracker database (No need to restart after that, bot will fetch the newly added servers):
  - Directly using database management softwares
  - Through commands (~/cog/admin.py)

## Usage

```bash
# Run the discord bot
python main.py run

# Fetching all servers and updating them in database
python main.py db:update

# Running tests/test_basic.py for testing purposes
python main.py test
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)