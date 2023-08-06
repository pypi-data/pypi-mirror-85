"""
Convenience wrappers to make using the conf system as easy and seamless as possible
"""
from typing import Any
from typing import Dict
from typing import List

import pop.hub


def integrate(
    hub: "pop.hub.Hub",
    imports: List[str] or str,
    override: Dict[str, Any] = None,
    cli: str = None,
    roots: bool = None,
    loader: str = "json",
    logs: bool = True,
):
    """
    Load the conf sub and run the integrate sequence.
    """
    hub.pop.sub.add("pop.mods.conf")
    hub.conf.integrate.load(
        imports, override, cli=cli, roots=roots, loader=loader, logs=logs
    )
