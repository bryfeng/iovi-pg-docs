#!/usr/bin/env python3
"""Generate checked-in OpenAPI schemas from local EON FastAPI apps."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "eon-docs" / "src" / "content" / "openapi"


def add_path(path: str) -> None:
    resolved = str(ROOT / path)
    if resolved not in sys.path:
        sys.path.insert(0, resolved)


def clear_modules(*prefixes: str) -> None:
    for name in list(sys.modules):
        if name in prefixes or any(name.startswith(f"{prefix}.") for prefix in prefixes):
            del sys.modules[name]


def write_schema(name: str, schema: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / f"{name}.openapi.json"
    target.write_text(
        json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {target.relative_to(ROOT)}")


def payment_schema() -> dict[str, Any]:
    clear_modules("api", "core", "storage", "payment_plugin", "verifier_engine")
    add_path("payment_sl")
    module = importlib.import_module("api")
    return module.app.openapi()


def generic_verifier_schema() -> dict[str, Any]:
    clear_modules("eon_verifier", "eon_protocol")
    add_path("eon-verifier")
    add_path("eon-protocol-schemas")
    module = importlib.import_module("eon_verifier.api")

    class DummyEngine:
        def ingest_event(self, _event: dict[str, Any]) -> dict[str, Any]:
            return {}

    class DummyStore:
        def list_base_events(self) -> list[dict[str, Any]]:
            return []

        def load_checkpoint(self, *_args: Any, **_kwargs: Any) -> None:
            return None

        def list_verification_log(self, *_args: Any, **_kwargs: Any) -> list[dict[str, Any]]:
            return []

    app = module.create_app(DummyEngine(), DummyStore())
    return app.openapi()


def bundler_engine_schema() -> dict[str, Any]:
    clear_modules("eon_bundler", "eon_protocol", "eon_issuer", "eon_settlement")
    add_path("eon-bundler-engine")
    add_path("eon-protocol-schemas")
    add_path("eon-issuer-framework")
    add_path("eon-settlement-framework")
    module = importlib.import_module("eon_bundler.api")
    module.app.openapi_schema = None
    return module.app.openapi()


def marketplace_bundler_schema() -> dict[str, Any]:
    clear_modules(
        "services",
        "eon_amm",
        "eon_bundler",
        "eon_issuer",
        "eon_protocol",
        "eon_settlement",
        "eon_verifier",
    )
    add_path("eon-marketplace-stack")
    add_path("eon-marketplace-stack/packages/eon-protocol-schemas")
    add_path("eon-marketplace-stack/packages/eon-verifier")
    add_path("eon-marketplace-stack/packages/eon-issuer-framework")
    add_path("eon-marketplace-stack/packages/eon-settlement-framework")
    add_path("eon-marketplace-stack/packages/eon-amm-framework")
    add_path("eon-marketplace-stack/packages/eon-bundler-engine")
    os.environ.setdefault("EON_VERIFIER_URL", "http://localhost:8000")
    module = importlib.import_module("services.bundler_api")
    module.app.openapi_schema = None
    return module.app.openapi()


def main() -> None:
    write_schema("payment-sl", payment_schema())
    write_schema("generic-verifier", generic_verifier_schema())
    write_schema("bundler-engine", bundler_engine_schema())
    write_schema("marketplace-bundler", marketplace_bundler_schema())


if __name__ == "__main__":
    main()
