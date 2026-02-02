import os
import yaml
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class MetaSchema(BaseModel):
    guards: List[str]
    philosophy: str
    prefixes: Dict[str, str]

class RoleSchema(BaseModel):
    id: str
    capability: str
    focus: List[str]

class PermissionsSchema(BaseModel):
    read: Optional[Union[str, List[str]]] = None
    write: Optional[Union[str, List[str]]] = None
    exec: Optional[Union[str, List[str]]] = None

class GateSchema(BaseModel):
    id: str
    output_artifacts: List[str]
    responsible_role: str
    permissions: Optional[PermissionsSchema] = None
    verification_rule: str
    depends_on: Optional[str] = None
    
    # Logic Fields (Flattened)
    mandatory_sections: List[Union[str, Dict[str, Any]]]
    ears_enforcement: Optional[bool] = False
    formal_verification: Optional[bool] = False
    statistical_rigor: Optional[bool] = False
    traceability_matrix: Optional[bool] = False
    audit_path_enforcement: Optional[bool] = False
    resource_validation: Optional[bool] = False
    consistency_verification: Optional[bool] = False

class ProtocolManifest(BaseModel):
    id: str
    version: str
    meta: MetaSchema
    roles: List[RoleSchema]
    gates: List[GateSchema]

class Registry:
    def __init__(self, root_dir=None):
        if root_dir is None:
            # Default to the directory where the package is installed
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        else:
            self.root_dir = os.path.abspath(root_dir)
        
    def find_all(self) -> Dict[str, Dict[str, Any]]:
        protocols = {}
        # Search in the standard domains directory
        domains_path = os.path.join(self.root_dir, "domains")
        if not os.path.exists(domains_path):
            return protocols

        for root, _, files in os.walk(domains_path):
            if "manifest.yaml" in files:
                path = os.path.join(root, "manifest.yaml")
                try:
                    with open(path, "r") as f:
                        data = yaml.safe_load(f)
                        if data and "id" in data:
                            guards = data.get("meta", {}).get("guards", ["Unknown"])
                            protocols[data["id"]] = {
                                "path": path,
                                "version": data.get("version", "1.0.0"),
                                "primary_guard": guards[0] if guards else "Unknown",
                                "guards": guards,
                                "dir": root
                            }
                except Exception:
                    continue
        return protocols

    def get_manifest(self, protocol_id: str) -> ProtocolManifest:
        protocols = self.find_all()
        if protocol_id not in protocols:
            raise ValueError(f"Protocol '{protocol_id}' not found in registry.")
        
        path = protocols[protocol_id]["path"]
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        
        return ProtocolManifest(**data)
