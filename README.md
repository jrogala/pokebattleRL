# PokeBattleRL Repository

A repository for developing and managing RL battle agents.

## Table of Contents
- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project focuses on creating intelligent agents for battling in the RL environment. The main components are:

1. **Bot**: Contains core AI and battle logic.
2. **Server**: Manages game state and communication.
3. **Tests**: Includes test cases for various functionalities.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js (optional, for server components)

### Installation
1. Clone the repository:
```bash
git clone git@github.com:yourusername/pokebattleRL.git
cd pokebattleRL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
npm install  # For server components
```

## Configuration

### Bot Configuration
- Configure your bot settings in `bot/src/config.py`.

### Server Configuration
- Adjust server settings in `server/config.js`.

## Running the Project

### Bot
```bash
python3 bot/src/main.py
```

### Server
```bash
node server/index.js
```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
4. Push to the branch and create a Pull Request.

## License
[Insert your license here, e.g., MIT License]

## Contact
For questions or suggestions, contact [your email].
