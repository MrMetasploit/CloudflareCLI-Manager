# CloudflareCLI

CloudflareCLI is a command-line tool designed to manage Cloudflare DNS records directly from the console. It provides users with the ability to list, create, and delete DNS records by utilizing the Cloudflare API, making it ideal for administrators and developers who need quick and scriptable access to their DNS configurations.

## Features

- **List DNS Records**: Quickly list all DNS records for a specific zone in a tabular format.
- **Create DNS Records**: Easily create DNS records (A, AAAA, TXT, CNAME) with the ability to define contents directly via command-line parameters.
- **Delete DNS Records**: Safely delete DNS records by specifying the record number provided by the listing function.
- **Multi-Zone Support**: Manage multiple zones through a simple configuration file.

## Installation

### Prerequisites

- Python 3.6 or newer
- `requests` library

### PyInstaller (Optional)

To create an executable file of the tool, you will additionally need:

- PyInstaller

### Setup

1. Clone the repository or download the source files.
2. Install the required dependencies via `pip`:
   ```bash
   pip install requests
   ```
3. (Optional) Create an executable file with PyInstaller:
   ```bash
   pyinstaller --onefile CloudflareCLI.py
   ```

## Configuration

Upon first run, the tool will look for a `config.ini` file in the current directory. If it is not present, an example configuration file will be automatically created. Edit this file to include your Cloudflare API keys and zone IDs:

```ini
[example.com]
api_key = your_api_key_here_for_example_com
zone_id = your_zone_id_here_for_example_com

[another-example.com]
api_key = your_api_key_here_for_another_example_com
zone_id = your_zone_id_here_for_another_example_com
```

## Usage

After setting up your configuration file, you can use the tool as follows:

- **List DNS Records**:
  ```bash
  python3 CloudflareCLI.py --zone example.com
  ```
- **List DNS Records with Numbers**:
  ```bash
  python3 CloudflareCLI.py --zone example.com --numbered
  ```
- **Create DNS Record**:
  ```bash
  python3 CloudflareCLI.py --zone example.com --create --type A --domain subdomain.example.com --content 192.0.2.1
  ```
- **Delete DNS Record**:
  ```bash
  python3 CloudflareCLI.py --zone example.com --delete 3
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
