import configparser
import requests
import argparse
import os

# Argument Parsing
parser = argparse.ArgumentParser(description='Manage Cloudflare DNS records.')
parser.add_argument('--zone', help='Specifies the zone name as defined in config.ini.', required=True)
parser.add_argument('--numbered', help='Lists all DNS records for a zone with numbers, in a table format, making them easier to manage.', action='store_true')
parser.add_argument('--create', help='Indicates creation of a new DNS record. Use with --type, --domain, and --content.', action='store_true')
parser.add_argument('--delete', help='Deletes the DNS record with the specified number (use --numbered to see numbers).', type=int)
parser.add_argument('--type', help='Specifies the DNS record type (A, AAAA, TXT, CNAME) for creation.')
parser.add_argument('--domain', help='Specifies the domain name for the DNS record.')
parser.add_argument('--content', help='Specifies the content for the DNS record. For TXT records, this can include text strings with spaces.')
args = parser.parse_args()

def create_example_config():
    config = configparser.ConfigParser()
    config['example.com'] = {
        'api_key': 'your_api_key_here_for_example_com',
        'zone_id': 'your_zone_id_here_for_example_com'
    }
    config['another-example.com'] = {
        'api_key': 'your_api_key_here_for_another_example_com',
        'zone_id': 'your_zone_id_here_for_another_example_com'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("""Example config.ini has been created with placeholder values for 'example.com' and 'another-example.com'.
Please replace the placeholder values with your actual Cloudflare API keys and zone IDs.
You can add more zones in similar fashion under different sections.""")

if not os.path.isfile('config.ini'):
    create_example_config()
    exit("Please edit config.ini with your Cloudflare details and rerun the script.")

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

def get_zone_details(zone_name):
    if zone_name in config:
        api_key = config[zone_name]['api_key']
        zone_id = config[zone_name]['zone_id']
        return api_key, zone_id, {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    else:
        print(f"Error: Zone '{zone_name}' not found in configuration.")
        exit(1)

def display_dns_records(zone_name, numbered=False, print_records=True):
    api_key, zone_id, headers = get_zone_details(zone_name)
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    response = requests.get(url, headers=headers)
    records = response.json().get('result', [])
    if print_records:
        header = f"{'#': <4}{'Type': <10} {'Name': <30} {'Content': <40}" if numbered else f"{'Type': <10} {'Name': <30} {'Content': <40}"
        print(header)
        print("-" * 90)
        for i, record in enumerate(records, start=1):
            prefix = f"{i:<3}. " if numbered else ""
            print(f"{prefix}{record['type']: <10} {record['name']: <30} {record['content']: <40}")
    return records

def create_dns_record(zone_name, record_type, domain, content):
    api_key, zone_id, headers = get_zone_details(zone_name)
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    data = {
        'type': record_type,
        'name': domain,
        'content': content,
        'ttl': 1  # Using automatic TTL
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("DNS record successfully created.")
    else:
        print(f"Error creating DNS record. {response.json().get('errors')}")

def delete_dns_record(zone_name, record_number):
    records = display_dns_records(zone_name, numbered=True, print_records=False)
    if 0 < record_number <= len(records):
        api_key, zone_id, headers = get_zone_details(zone_name)
        record_id = records[record_number - 1]['id']
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"DNS record successfully deleted.")
            display_dns_records(zone_name, numbered=True, print_records=True)
        else:
            print(f"Error deleting DNS record. {response.json().get('errors')}")
    else:
        print("Invalid record number.")

if args.create:
    if not all([args.type, args.domain, args.content]):
        print("Error: --create requires --type, --domain, and --content.")
    else:
        create_dns_record(args.zone, args.type, args.domain, args.content)
elif args.delete is not None:
    records = display_dns_records(args.zone, numbered=True)
    delete_dns_record(args.zone, args.delete)
else:
    display_dns_records(args.zone, args.numbered)
