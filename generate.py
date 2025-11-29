import yaml
from jinja2 import Environment, FileSystemLoader

# 1. Load the YAML data
with open('routers.yaml') as f:
    devices = yaml.safe_load(f)

# 2. Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('cisco_base.j2')

# 3. Generate a config for each device
for device in devices:
    print(f"Generating config for {device['hostname']}...")
    
    # Render the template with data
    config = template.render(device=device)
    
    # Save to file
    filename = f"{device['hostname']}.cfg"
    with open(filename, "w") as f:
        f.write(config)
        
    print(f" -> Saved to {filename}")

print("\nAll configurations generated successfully!")
