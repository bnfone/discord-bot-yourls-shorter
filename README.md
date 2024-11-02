 # YOURLS Shortener Discord Bot

![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-red)
[![Invite the Bot](https://img.shields.io/badge/Invite%20the%20Bot-Click%20Here-blue)](https://discord.com/oauth2/authorize?client_id=1302371196700069978&permissions=274877925376&integration_type=0&scope=bot)

A simple yet powerful Discord bot for shortening URLs using your YOURLS instance. This bot is designed to be deployed in a Docker environment and includes persistent link statistics tracking and customizable commands.

## Features

- **Shorten Links**: Use `/shorturl` or `/shortlink` to create short URLs directly in Discord.
- **Custom Short Links**: Optionally, enable a `/customurl` command to create short URLs with custom keywords.
- **Statistics**: Track the number of links shortened and user-specific link counts. View these stats using `/stats`.
- **Bot Information**: Get details about the bot, including GitHub link and donation link with the `/info` command.
- **Ephemeral Messages**: Option to make bot responses private to the user.

## Project Structure

```
discord-bot-yourls-shorter/
├── Dockerfile
├── README.md
├── bot.py
├── docker-compose.yml
├── example.env
├── .gitignore
└── requirements.txt
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- A YOURLS instance with API access and a signature token
- A Discord bot token

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/bnfone/discord-bot-yourls-shorter.git
   cd discord-bot-yourls-shorter
   ```

2. **Environment Variables**:

   Copy the `example.env` file and configure it with your own values:

   ```bash
   cp example.env .env
   ```

   In `.env`, set the following variables:

   ```env
   YOURLS_URL=https://your-yourls-instance.com/yourls-api.php
   YOURLS_SIGNATURE_TOKEN=your-secret-signature-token
   DISCORD_TOKEN=your-discord-bot-token
   ENABLE_CUSTOM_URL=true
   ENABLE_INFO_COMMAND=true
   EPHEMERAL_RESPONSE=true
   GITHUB_LINK=https://github.com/bnfone/discord-bot-yourls-shorter
   DONATION_LINK=https://your-donation-link.com
   ```

   - **YOURLS_URL**: URL of your YOURLS API.
   - **YOURLS_SIGNATURE_TOKEN**: Secret signature token for YOURLS API access.
   - **DISCORD_TOKEN**: Your Discord bot token.
   - **ENABLE_CUSTOM_URL**: Enables the `/customurl` command.
   - **ENABLE_INFO_COMMAND**: Enables the `/info` command.
   - **EPHEMERAL_RESPONSE**: If set to `true`, makes bot responses visible only to the user.
   - **GITHUB_LINK** and **DONATION_LINK**: Used in the `/info` command embed.

3. **Build and Run the Bot**:

   Use Docker Compose to build and start the bot:

   ```bash
   docker-compose up --build
   ```

   The bot will run as a service and save link statistics to a persistent `stats.json` file.

## Usage

Once the bot is running, you can use the following commands in Discord:

- **/shorturl [link]**: Shortens a given link.
- **/shortlink [link]**: Alternative command to shorten a link.
- **/customurl [link] [keyword]**: (If enabled) Shortens a link with a custom keyword.
- **/stats**: Displays link statistics, including total links shortened, user-specific counts, and bot ping.
- **/info**: (If enabled) Provides bot details with links to the GitHub repository and donation page.

### Persistent Statistics

The bot saves link statistics in `stats.json`, including:

- **Total Links Shortened**: Total count of all shortened links.
- **User Statistics**: Track links shortened by each user.
- **Top Domains**: Display the most frequently shortened domains.

To persist `stats.json` across container restarts, ensure it’s mounted in `docker-compose.yml`:

```yaml
version: '3'
services:
  discord-bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./stats.json:/usr/src/app/stats.json
    restart: always
```

## Contributing

Feel free to fork this repository and submit pull requests with improvements or new features!

## License

This project is licensed under the MIT License.

---

Made with ❤️ by [Blake](https://github.com/bnfone)