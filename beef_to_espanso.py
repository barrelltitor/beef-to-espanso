import json
import yaml
import os
import argparse

parser = argparse.ArgumentParser(description="Convert Beeftext backup to Espanso YAML format.")
parser.add_argument('-f', '--file', type=str, default='Beeftext.btbackup',
                    help='The name of the Beeftext backup file (default: Beeftext.btbackup)')
args = parser.parse_args()

with open(args.file, 'r') as file:
    json_data = json.load(file)

data = json_data
groups = {}

output_dir = 'output_groups'
os.makedirs(output_dir, exist_ok=True)

# Replaces some weird characters I got. I don't know if it's my fault they're there, or if it's some weird beeftext issue
def clean_text(text):
    replacements = {
        'ΓÇÿ': '',    # No idea what this is
        'ΓÇ¿': '',    # No idea what this is
        'ΓÇÖ': "'",   # Apostrophe
        '\xE2\u20AC\xA8': '',  # Remove the line separator
        '\u2028': '', 
        '\r': '',
    }
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    
    return text

# Lookup table
group_names = {group['uuid']: group['name'] for group in data['groups']}
#from here https://stackoverflow.com/a/33300001
#because otherwise new lines got converted to literal \n which espanso seems to have sent as literal \n's
#Though if I manually add a \n it seems to work? Maybe this is not needed?
def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


# Set the combos in their specific groups
for combo in data['combos']:
    group_id = combo['group']
    
    trigger = combo['keyword']
    replace = clean_text(combo['snippet'])
    match = {
        "trigger": trigger,
        "replace": replace
    }
    
    # Add combo to the correct group
    if group_id not in groups:
        groups[group_id] = []
    groups[group_id].append(match)

# Write YAML files
for group_id, combos in groups.items():
    group_name = group_names.get(group_id, 'unknown_group')
    matches = {'matches': combos}
    filename = os.path.join(output_dir, f"{group_name}.yml")
    with open(filename, 'w') as file:
        file.write(yaml.dump(matches, sort_keys=False, default_flow_style=False))

print(f"YAML files have been generated in the '{output_dir}' directory.")
