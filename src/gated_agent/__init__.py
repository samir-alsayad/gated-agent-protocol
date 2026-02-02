"""
GAP (Gated Agent Protocol) - An open standard for governing AI agent work through machine-enforceable checkpoints.
"""

from .registry import Registry, ProtocolManifest, GateSchema, RoleSchema, MetaSchema
from .security import ACLEnforcer
from .session import Session, BaseSessionManager, LocalSessionManager

__version__ = "1.0.0"
__all__ = [
    "Registry",
    "ProtocolManifest",
    "GateSchema",
    "RoleSchema",
    "MetaSchema",
    "ACLEnforcer",
    "Session",
    "BaseSessionManager",
    "LocalSessionManager",
]
