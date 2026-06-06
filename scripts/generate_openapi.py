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
PUBLIC_OUT_DIR = ROOT / "eon-docs" / "public" / "openapi"


SERVICE_META: dict[str, dict[str, Any]] = {
    "payment-sl": {
        "title": "IOVI Payment SL Sandbox API",
        "description": (
            "Public sandbox middleware for trying the current IOVI Payment semantic-layer flow: "
            "register wallets, create semantic-layer actions, batch them, and verify accepted state."
        ),
        "servers": [
            {
                "url": "https://eon-payment-sl-demo-production.up.railway.app",
                "description": "Public Payment SL sandbox",
            }
        ],
    },
    "generic-verifier": {
        "title": "IOVI Generic Verifier API",
        "description": (
            "Public verifier API for ingesting ordered base-layer events and replaying semantic-layer "
            "rules into accepted local state."
        ),
        "servers": [
            {
                "url": "https://verifier-production-7dc3.up.railway.app",
                "description": "Public Generic Verifier service",
            }
        ],
    },
    "bundler-engine": {
        "title": "IOVI Bundler Engine API",
        "description": (
            "Public bundler API for wrapping child semantic-layer payloads into bundle payloads that can "
            "be transported as base-layer UTXO Data."
        ),
        "servers": [
            {
                "url": "https://bundler-production-b637.up.railway.app",
                "description": "Public Bundler Engine service",
            }
        ],
    },
    "marketplace-bundler": {
        "title": "IOVI Marketplace Bundler API",
        "description": (
            "Public marketplace extension API for AMM quotes, liquidity, approvals, swaps, and bundle "
            "settlement payloads."
        ),
        "servers": [
            {
                "url": "https://bundler-production-b637.up.railway.app",
                "description": "Public Bundler/Marketplace service",
            }
        ],
    },
    "base-layer": {
        "title": "IOVI Base-Layer API",
        "description": (
            "HTTP posting and read API around IOVI SDK wallet, UTXO, transaction, and transfer-with-Data flows. "
            "Semantic-layer meaning is not interpreted by this service."
        ),
        "servers": [
            {
                "url": "https://iovi-api-production.up.railway.app",
                "description": "Public Base-Layer API. The live service does not expose OpenAPI; this checked-in schema documents the public surface.",
            }
        ],
    },
}


TAG_DESCRIPTIONS: dict[str, str] = {
    "Health": "Liveness, readiness, and service configuration checks.",
    "Operator": "Operator-local lifecycle, batching, and pending-work endpoints.",
    "Wallets": "Wallet registration and VK-derived identity lookups.",
    "Base-Layer Accounts": "Base-layer account records used by the sandbox middleware.",
    "Semantic Layers": "Semantic-layer and asset registry endpoints.",
    "Actions": "Payment semantic-layer actions queued before batching and verification.",
    "Devnet": "Payload encoding and devnet submission boundaries.",
    "Verifier": "Verifier ingestion and accepted-state read surfaces.",
    "Reads": "Read models for accepted balances and service state.",
    "Bundles": "Bundle wrapper construction from child payloads.",
    "Marketplace": "AMM assets, pools, quotes, liquidity, approvals, swaps, and settlement payloads.",
    "Base Layer": "Base-layer wallet, balance, UTXO, transaction, and transfer posting endpoints.",
}


SEMANTIC_LAYER_ID_DESCRIPTION = (
    "Hex semantic-layer identifier. Use the default Payment SL `00010001` or generate an isolated "
    "hex lane such as `a9bca654`; non-hex values are rejected by the public sandbox."
)
SEMANTIC_LAYER_ID_PATTERN = "^[0-9a-fA-F]+$"
VERSION_DESCRIPTION = "Semantic-layer version. The public examples use four hex digits such as `0001`."


REQUEST_EXAMPLES: dict[str, Any] = {
    "InitRequest": {
        "issuer_vk": "circle_inc_verification_key",
        "reset_existing": False,
        "sl_id": "00010001",
        "version": "0001",
    },
    "WalletRequest": {"label": "Alice", "vk": "alice_vk", "kind": "user"},
    "SemanticLayerRequest": {
        "name": "Payment SL",
        "sl_id": "00010001",
        "version": "0001",
        "operator_wallet_address": "c97360fe9a6d9c26751be4f8edf4ef6672123775",
        "base_layer_account_id": "acct_demo_operator",
        "assets": [{"asset_id": "USD", "name": "Demo USD", "decimals": 2}],
    },
    "SemanticLayerAssetRequest": {"asset_id": "USD", "name": "Demo USD", "decimals": 2},
    "AmountToRequest": {
        "to_address": "alice_wallet_address",
        "amount": 1000,
        "asset_id": "USD",
        "sl_id": "00010001",
        "version": "0001",
    },
    "AmountFromRequest": {
        "from_address": "alice_wallet_address",
        "amount": 100,
        "asset_id": "USD",
        "vk": "alice_vk",
        "sl_id": "00010001",
        "version": "0001",
    },
    "TransferRequest": {
        "from_address": "alice_wallet_address",
        "to_address": "bob_wallet_address",
        "amount": 250,
        "asset_id": "USD",
        "vk": "alice_vk",
        "sl_id": "00010001",
        "version": "0001",
    },
    "TargetRequest": {
        "address": "alice_wallet_address",
        "vk": "circle_inc_verification_key",
        "sl_id": "00010001",
        "version": "0001",
    },
    "BaseLayerAccountRequest": {
        "account_id": "acct_demo_operator",
        "label": "Demo operator account",
        "address": "0x1234",
    },
    "BaseLayerAccountGenerateRequest": {"label": "Demo operator account"},
    "PayloadRequest": {"payload_hex": "0001000100010000000000000001"},
    "DevnetSubmitRequest": {"dry_run": True},
    "VerifierSyncRequest": {"limit": 25},
    "BaseEventRequest": {
        "cursor": "devnet:1:0:0",
        "network_id": "devnet",
        "height": 1,
        "block_hash": None,
        "tx_hash": "0xabc123",
        "tx_index": 0,
        "output_index": 0,
        "utxo_id": "0xabc123:0",
        "owner": "0xoperator",
        "amount": "1",
        "data_scalars": ["0x0001000100010000000000000001"],
        "payload_hex": "0001000100010000000000000001",
        "event_key": "devnet:1:0:0",
    },
    "BundleWrapRequest": {
        "bundle_id": "1111111111111111111111111111111111111111111111111111111111111111",
        "child_payload_hex": ["0001000100010000000000000001"],
    },
    "CreatePoolRequest": {
        "pool_id": "stock-usd",
        "asset_a": {"sl_id": "53544f43", "version": "0001", "asset_id": "AAPL"},
        "asset_b": {"sl_id": "55534443", "version": "0001", "asset_id": "USD"},
        "reserve_a": 100,
        "reserve_b": 10000,
        "creator_vk": "market_maker_vk",
    },
    "ApprovePoolRequest": {"pool_id": "stock-usd", "approver_vk": "coordinator_vk"},
    "AddLiquidityRequest": {
        "pool_id": "stock-usd",
        "provider_vk": "liquidity_provider_vk",
        "amount_a": 10,
        "amount_b": 1000,
        "min_lp_shares": 1,
    },
    "RemoveLiquidityRequest": {
        "pool_id": "stock-usd",
        "provider_vk": "liquidity_provider_vk",
        "lp_shares": 5,
        "min_amount_a": 1,
        "min_amount_b": 1,
    },
    "SwapExactInRequest": {
        "pool_id": "stock-usd",
        "trader_vk": "alice_vk",
        "input_asset": {"sl_id": "55534443", "version": "0001", "asset_id": "USD"},
        "amount_in": 100,
        "min_amount_out": 1,
    },
    "TransferWithDataRequest": {
        "recipient": "0xrecipient",
        "amount": 100,
        "fee": 1,
        "data": [12345, "0x00003039"],
    },
}


RESPONSE_EXAMPLES: dict[tuple[str, str], Any] = {
    ("get", "/health"): {"ok": True},
    ("post", "/operator/init"): {
        "initialized": True,
        "sl_id": "00010001",
        "version": "0001",
        "operator_wallet_address": "c97360fe9a6d9c26751be4f8edf4ef6672123775",
    },
    ("post", "/wallets"): {
        "address": "alice_wallet_address",
        "label": "Alice",
        "kind": "user",
    },
    ("post", "/actions/mint"): {"queued": True, "action": "mint", "pending_count": 1},
    ("post", "/actions/transfer"): {"queued": True, "action": "transfer", "pending_count": 1},
    ("post", "/operator/batch"): {
        "batch_id": "batch_0001",
        "payload_hex": "0001000100010000000000000001",
        "data_scalars": ["0x0001000100010000000000000001"],
    },
    ("post", "/verifier/accept-latest-batch"): {"accepted": True, "events": 1},
    ("get", "/verifier/state"): {"sl_id": "00010001", "version": "0001", "balances": {}},
    ("get", "/verifier/log"): [{"status": "accepted", "cursor": "sandbox:batch:0001"}],
    ("post", "/verifier/ingest-event"): {"accepted": True, "cursor": "devnet:1:0:0"},
    ("post", "/bundles/wrap"): {
        "bundle_id": "1111111111111111111111111111111111111111111111111111111111111111",
        "payload_hex": "42554e444c45",
        "data_scalars": ["0x42554e444c45"],
        "child_count": 1,
    },
    ("get", "/assets"): [{"sl_id": "55534443", "version": "0001", "asset_id": "USD"}],
    ("get", "/pools"): [{"pool_id": "stock-usd", "status": "active"}],
    ("get", "/quotes/exact-in"): {"amount_in": 100, "amount_out": 1, "price_impact_bps": 25},
    ("post", "/swaps/exact-in"): {
        "bundle_id": "swap_bundle_0001",
        "settlement_id": "settlement_0001",
        "payload_hex": "53574150",
        "data_scalars": ["0x53574150"],
    },
    ("get", "/wallet/address"): {"address": "0xoperator"},
    ("get", "/balance"): {"owner": "0xoperator", "balance": "1000000"},
    ("get", "/utxos"): {"items": [{"utxo_id": "0xabc123:0", "amount": "100", "data": ["0x00003039"]}]},
    ("get", "/transactions/{hash}"): {"hash": "0xabc123", "status": "accepted"},
    ("post", "/transactions/transfer"): {"hash": "0xabc123", "submitted": True},
}


def add_path(path: str) -> None:
    resolved = str(ROOT / path)
    if resolved not in sys.path:
        sys.path.insert(0, resolved)


def clear_modules(*prefixes: str) -> None:
    for name in list(sys.modules):
        if name in prefixes or any(name.startswith(f"{prefix}.") for prefix in prefixes):
            del sys.modules[name]


def write_schema(name: str, schema: dict[str, Any]) -> None:
    enhance_schema(name, schema)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / f"{name}.openapi.json"
    public_target = PUBLIC_OUT_DIR / f"{name}.openapi.json"
    content = json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    target.write_text(content, encoding="utf-8")
    public_target.write_text(content, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    print(f"wrote {public_target.relative_to(ROOT)}")


def enhance_schema(name: str, schema: dict[str, Any]) -> None:
    meta = SERVICE_META[name]
    schema.setdefault("info", {})
    schema["info"]["title"] = meta["title"]
    schema["info"]["description"] = meta["description"]
    schema["servers"] = meta["servers"]
    schema["tags"] = [
        {"name": tag, "description": description}
        for tag, description in TAG_DESCRIPTIONS.items()
        if tag_used(name, tag)
    ]
    add_common_schema_docs(schema)

    for path, methods in schema.get("paths", {}).items():
        for method, operation in methods.items():
            tag = infer_tag(path, name)
            operation["tags"] = [tag]
            operation.setdefault("summary", title_from_operation(method, path))
            operation["description"] = operation_description(method, path, tag)
            add_parameter_examples(operation)
            add_request_example(operation)
            add_response_example(method, path, operation)


def add_common_schema_docs(schema: dict[str, Any]) -> None:
    for component in schema.get("components", {}).get("schemas", {}).values():
        properties = component.get("properties", {})
        if not isinstance(properties, dict):
            continue

        for name, property_schema in properties.items():
            if not isinstance(property_schema, dict):
                continue
            if name == "sl_id" or name.endswith("_sl_id"):
                property_schema.setdefault("description", SEMANTIC_LAYER_ID_DESCRIPTION)
                property_schema.setdefault("pattern", SEMANTIC_LAYER_ID_PATTERN)
            if name == "version" or name.endswith("_version"):
                property_schema.setdefault("description", VERSION_DESCRIPTION)


def tag_used(service: str, tag: str) -> bool:
    if service == "payment-sl":
        return tag not in {"Bundles", "Marketplace"}
    if service == "generic-verifier":
        return tag in {"Health", "Verifier"}
    if service == "bundler-engine":
        return tag in {"Health", "Bundles"}
    if service == "marketplace-bundler":
        return tag in {"Health", "Bundles", "Marketplace"}
    if service == "base-layer":
        return tag in {"Health", "Base Layer"}
    return False


def infer_tag(path: str, service: str) -> str:
    if path in {"/", "/health", "/config"}:
        return "Health"
    if path.startswith("/operator") or path.startswith("/pending"):
        return "Operator"
    if path.startswith("/wallets"):
        return "Wallets"
    if path.startswith("/base-layer"):
        return "Base-Layer Accounts"
    if path.startswith("/semantic-layers"):
        return "Semantic Layers"
    if path.startswith("/actions"):
        return "Actions"
    if path.startswith("/devnet"):
        return "Devnet"
    if path.startswith("/verifier"):
        return "Verifier"
    if path.startswith("/balances"):
        return "Reads"
    if path.startswith("/bundles"):
        return "Bundles"
    if path.startswith("/wallet") or path.startswith("/balance") or path.startswith("/utxos") or path.startswith("/transactions"):
        return "Base Layer"
    if service == "marketplace-bundler":
        return "Marketplace"
    return "Health"


def title_from_operation(method: str, path: str) -> str:
    return f"{method.upper()} {path}"


def operation_description(method: str, path: str, tag: str) -> str:
    if method.lower() == "get":
        return f"Read from the {tag.lower()} surface. Use these responses for status checks, discovery, or accepted-state reads."
    if path.startswith("/actions"):
        return "Queue a Payment semantic-layer action. The action is not verifier-accepted until it is batched and replayed."
    if path == "/operator/batch":
        return "Batch pending semantic-layer actions into a canonical payload that can be encoded as UTXO Data."
    if path.startswith("/verifier"):
        return "Ingest or replay ordered data and read verifier-accepted semantic-layer state."
    if path.startswith("/bundles") or tag == "Marketplace":
        return "Create or inspect bundle/marketplace payloads. Bundles transport ordered data; child semantic layers still own validity."
    if tag == "Base Layer":
        return "Read or post base-layer wallet, UTXO, transaction, or transfer data. This service does not validate semantic-layer meaning."
    return f"Mutate or create state in the {tag.lower()} surface."


def add_parameter_examples(operation: dict[str, Any]) -> None:
    examples = {
        "sl_id": "00010001",
        "version": "0001",
        "address": "alice_wallet_address",
        "limit": 10,
        "pool_id": "stock-usd",
        "input_sl_id": "55534443",
        "input_version": "0001",
        "input_asset_id": "USD",
        "amount_in": 100,
        "owner": "0xoperator",
        "hash": "0xabc123",
    }
    for parameter in operation.get("parameters", []):
        name = parameter.get("name")
        if name in examples:
            parameter["example"] = examples[name]
        if name == "sl_id" or (isinstance(name, str) and name.endswith("_sl_id")):
            parameter["description"] = SEMANTIC_LAYER_ID_DESCRIPTION
            schema = parameter.setdefault("schema", {})
            if isinstance(schema, dict):
                schema.setdefault("type", "string")
                schema.setdefault("pattern", SEMANTIC_LAYER_ID_PATTERN)
        if name == "version" or (isinstance(name, str) and name.endswith("_version")):
            parameter.setdefault("description", VERSION_DESCRIPTION)


def add_request_example(operation: dict[str, Any]) -> None:
    request_body = operation.get("requestBody")
    if not request_body:
        return

    media = request_body.get("content", {}).get("application/json")
    if not media:
        return

    schema = media.get("schema", {})
    schema_name = schema.get("$ref", "").split("/")[-1]
    example = REQUEST_EXAMPLES.get(schema_name)
    if example is None:
        example = {"payload": "replace-with-request-body"}
    media["example"] = example


def add_response_example(method: str, path: str, operation: dict[str, Any]) -> None:
    response = operation.setdefault("responses", {}).setdefault("200", {})
    response["description"] = successful_response_description(method, path)
    media = response.setdefault("content", {}).setdefault("application/json", {})
    media.setdefault("schema", {"type": "object", "additionalProperties": True})
    media["example"] = RESPONSE_EXAMPLES.get(
        (method.lower(), path),
        {"ok": True, "status": "success"},
    )


def successful_response_description(method: str, path: str) -> str:
    if path.startswith("/verifier"):
        return "Verifier response. Prefer verifier reads for accepted semantic-layer state."
    if path.startswith("/actions"):
        return "Action queued successfully. Batch and verify before treating it as accepted state."
    if path.startswith("/operator"):
        return "Operator-local response. Useful for batching and transport, not final wallet state."
    return "Successful response."


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
    os.environ.setdefault("EON_VERIFIER_URL", "https://verifier-production-7dc3.up.railway.app")
    module = importlib.import_module("services.bundler_api")
    module.app.openapi_schema = None
    return module.app.openapi()


def base_layer_schema() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {"title": "IOVI Base-Layer API", "version": "0.1.0"},
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health",
                    "responses": {"200": {"description": "Successful response."}},
                }
            },
            "/wallet/address": {
                "get": {
                    "summary": "Wallet Address",
                    "responses": {"200": {"description": "Successful response."}},
                }
            },
            "/balance": {
                "get": {
                    "summary": "Balance",
                    "parameters": [
                        {
                            "name": "owner",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {"200": {"description": "Successful response."}},
                }
            },
            "/utxos": {
                "get": {
                    "summary": "UTXOs",
                    "parameters": [
                        {
                            "name": "owner",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 10, "minimum": 1},
                        },
                    ],
                    "responses": {"200": {"description": "Successful response."}},
                }
            },
            "/transactions/{hash}": {
                "get": {
                    "summary": "Transaction",
                    "parameters": [
                        {
                            "name": "hash",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {"200": {"description": "Successful response."}},
                }
            },
            "/transactions/transfer": {
                "post": {
                    "summary": "Transfer With Data",
                    "security": [{"PosterApiKey": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TransferWithDataRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Successful response."},
                        "401": {"description": "Missing or invalid API key when POSTER_API_KEY is configured."},
                    },
                }
            },
        },
        "components": {
            "securitySchemes": {
                "PosterApiKey": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "x-api-key",
                    "description": "Required for write routes when POSTER_API_KEY is configured. Authorization: Bearer is also accepted by the service.",
                }
            },
            "schemas": {
                "TransferWithDataRequest": {
                    "type": "object",
                    "required": ["recipient", "amount", "fee", "data"],
                    "properties": {
                        "recipient": {"type": "string"},
                        "amount": {"type": "integer", "minimum": 1},
                        "fee": {"type": "integer", "minimum": 0},
                        "data": {
                            "type": "array",
                            "items": {"oneOf": [{"type": "integer"}, {"type": "string"}]},
                            "description": "Scalar values to carry as UTXO Data.",
                        },
                    },
                }
            },
        },
    }


def main() -> None:
    write_schema("payment-sl", payment_schema())
    write_schema("generic-verifier", generic_verifier_schema())
    write_schema("bundler-engine", bundler_engine_schema())
    write_schema("marketplace-bundler", marketplace_bundler_schema())
    write_schema("base-layer", base_layer_schema())


if __name__ == "__main__":
    main()
