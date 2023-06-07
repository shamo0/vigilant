# Vigilant

![vigilant](https://github.com/shamo0/vigilant/assets/48299520/69687ae3-18c8-4591-aae3-7bb26191dc79)

Vigilant is a Python-based tool designed to monitor online forums and websites for mentions of a specific domain. It helps you keep track of any instances where your company domain might be exposed or discussed in potentially compromising contexts.

## Features

- Surface web search: Monitors popular surface web forums and websites for mentions of the specified domain.
- Darknet search (optional): Allows searching for mentions of the domain in onion websites on the darknet (TOR network).
- Depth limit (optional): Allows specifying the depth limit for crawling the websites (default is 5 levels).
- Notification system: Sends notifications to Discord or Slack when the specified domain is found.

## Requirements

- Python 3.x
- pip package manager

## Installation


```
git clone https://github.com/shamo0/brechtector.git
cd vigilant
pip install -r requirements.txt
```

## Usage

```
python vigilant.py -d <domain> [options]
```

- `-d, --domain`: Specify the domain to monitor in the forums.
- `--surface`: Enable surface web search (default).
- `--dark`: Enable onion search (requires TOR service to be started).
- `--dark-only`: Enable onion-only search (requires TOR service to be started).
- `-l, --limit`: Set the depth limit for crawling the websites (default is 5).

## Examples

Search for mentions of the domain "example.com" in surface web forums:
```
python vigilant.py -d example.com
```
Enable darknet search for the domain "example.com":
```
python vigilant.py -d example.com --dark
```
Enable onion-only search for the domain "example.com":
```
python vigilant.py -d example.com --dark-only
```

## Notifications

To enable notifications, set up a Discord webhook and update the `discord_webhook` global variables in the `vigilant.py` with the respective webhook URLs. And uncomment `send_notification` function call lines

## Contribution

Contributions are welcome and greatly appreciated. If you have any ideas, suggestions, or improvements for Vigilant, feel free to contribute to the project.

## License

[MIT License](LICENSE)
