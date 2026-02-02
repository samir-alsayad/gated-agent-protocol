import argparse
import sys
import os
import yaml
import json
from .registry import Registry

def main():
    parser = argparse.ArgumentParser(description="GAP (Gated Agent Protocol) Registry Manager")
    parser.add_argument("--root", help="Root directory of the GAP repository (optional)")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # List command
    subparsers.add_parser("list", help="List all available protocols")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Retrieve a specific protocol manifest")
    get_parser.add_argument("id", help="The protocol ID")
    get_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    # Path command
    path_parser = subparsers.add_parser("path", help="Get the filesystem path to a protocol")
    path_parser.add_argument("id", help="The protocol ID")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a protocol manifest against the GAP schema")
    validate_parser.add_argument("id", help="The protocol ID")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a GAP project")
    init_parser.add_argument("protocol", nargs="?", default="software-development-v1", help="The protocol to use")

    args = parser.parse_args()
    
    registry = Registry(args.root)
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            gap_dir = os.path.join(os.getcwd(), ".gap")
            sessions_dir = os.path.join(gap_dir, "sessions")
            config_path = os.path.join(gap_dir, "gap.yaml")
            
            os.makedirs(sessions_dir, exist_ok=True)
            
            if not os.path.exists(config_path):
                default_config = {
                    "active_session": None,
                    "sessions": []
                }
                with open(config_path, "w") as f:
                    yaml.dump(default_config, f, default_flow_style=False)
                print(f"✅ Initialized GAP project in {gap_dir}")
                print(f"✅ Default protocol: {args.protocol} (ready for first session)")
            else:
                print(f"⚠️ GAP project already exists at {gap_dir}")

        elif args.command == "list":
            protocols = registry.find_all()
            print(f"{'PROTOCOL ID':<30} | {'VERSION':<10} | {'PRIMARY GUARD':<20}")
            print("-" * 65)
            for proto_id, info in sorted(protocols.items()):
                print(f"{proto_id:<30} | {info['version']:<10} | {info['primary_guard']:<20}")
        
        elif args.command == "get":
            manifest = registry.get_manifest(args.id)
            if args.json:
                print(manifest.model_dump_json(indent=2))
            else:
                data = manifest.model_dump()
                print(yaml.dump(data, default_flow_style=False))
        
        elif args.command == "path":
            protocols = registry.find_all()
            if args.id in protocols:
                print(protocols[args.id]["dir"])
            else:
                print(f"Error: Protocol '{args.id}' not found.", file=sys.stderr)
                sys.exit(1)
        
        elif args.command == "validate":
            manifest = registry.get_manifest(args.id)
            print(f"✅ Protocol '{args.id}' is valid according to GAP schema.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
