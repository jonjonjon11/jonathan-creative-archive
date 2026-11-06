"""Author-time mission validation and reference transitions; NOT a Unity runtime.

Python standard library only. Data is never evaluated, executed or sent online.
Passing this module establishes structural consistency, not content or child safety.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

MAX_BYTES = 65536
MAX_DEPTH = 12
MAX_NODES = 4096
ID = re.compile(r"[a-z][a-z0-9-]{0,47}\Z", re.ASCII)
POLICY = {
    "essential_access": "free",
    "network": "offline",
    "runtime_ai": "disabled",
    "public_uploads": "disabled",
    "voice_and_free_text_chat": "disabled",
    "personal_data_collection": "none",
    "model_training_from_players": "disabled",
    "paid_api_requests": 0,
    "physical_device_control": "disabled",
    "release": "internal_prototype",
}
ACCESS = {
    "noncombat_completion": True,
    "seated_menu_equivalent": True,
    "untimed_actions": True,
    "text_equivalent": True,
    "reduced_motion": True,
    "leave_without_penalty": True,
    "solo_scripted_companion": True,
    "role_switching": True,
}
REVIEWS = {
    "content": "pending_human_review",
    "science": "pending_educator_review",
    "accessibility": "pending_device_test",
    "runtime_security": "not_evaluated",
}
TOPICS = {"scale", "projectile-motion", "gravitational-energy", "circular-orbits", "ohms-law", "wave-frequency-period"}
KINDS = {"observe", "repair", "escort", "welcome", "restore", "reflect"}


class ContractError(ValueError):
    """An authoring packet or reference event violates this version's contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def exact_keys(value: object, keys: set[str], where: str) -> None:
    require(type(value) is dict, f"{where}: expected object")
    require(set(value) == keys, f"{where}: missing or unknown fields")


def literal_map(value: object, expected: dict, where: str) -> None:
    exact_keys(value, set(expected), where)
    for key, literal in expected.items():
        require(type(value[key]) is type(literal) and value[key] == literal,
                f"{where}.{key}: unsupported value")


def text(value: object, where: str, maximum: int = 600) -> None:
    require(type(value) is str and 0 < len(value) <= maximum, f"{where}: invalid text length/type")
    require(value == value.strip(), f"{where}: surrounding whitespace")
    require(not any(unicodedata.category(c).startswith("C") for c in value),
            f"{where}: control, surrogate or unassigned character")


def identifier(value: object, where: str) -> None:
    require(type(value) is str and ID.fullmatch(value) is not None, f"{where}: invalid identifier")


def bounded_list(value: object, low: int, high: int, where: str) -> None:
    require(type(value) is list and low <= len(value) <= high, f"{where}: invalid list size/type")


def unique_strings(value: object, low: int, high: int, where: str) -> None:
    bounded_list(value, low, high, where)
    for item in value:
        identifier(item, where)
    require(len(set(value)) == len(value), f"{where}: duplicate identifier")


def check_tree(value: object) -> None:
    # Iterative resource bounds also apply to already-parsed callers.
    todo = [(value, 0)]
    count = 0
    while todo:
        item, depth = todo.pop()
        count += 1
        require(depth <= MAX_DEPTH and count <= MAX_NODES, "packet exceeds structure bounds")
        if type(item) is dict:
            require(all(type(k) is str for k in item), "non-string object key")
            todo.extend((v, depth + 1) for v in item.values())
        elif type(item) is list:
            todo.extend((v, depth + 1) for v in item)
        else:
            require(type(item) in (str, int, bool), "unsupported scalar")


def validate_pack(pack: object) -> dict:
    check_tree(pack)
    exact_keys(pack, {"schema_version", "policy", "accessibility_requirements", "review_status", "missions"}, "pack")
    require(type(pack["schema_version"]) is int and pack["schema_version"] == 1, "unsupported schema version")
    literal_map(pack["policy"], POLICY, "policy")
    literal_map(pack["accessibility_requirements"], ACCESS, "accessibility_requirements")
    literal_map(pack["review_status"], REVIEWS, "review_status")
    bounded_list(pack["missions"], 1, 8, "missions")
    mission_ids = set()
    for mission in pack["missions"]:
        exact_keys(mission, {"id", "title", "setting", "premise", "combat", "roles", "learning_topics", "objectives"}, "mission")
        identifier(mission["id"], "mission.id")
        require(mission["id"] not in mission_ids, "duplicate mission")
        mission_ids.add(mission["id"])
        for field in ("title", "setting", "premise"):
            text(mission[field], field, 600 if field == "premise" else 100)
        require(type(mission["combat"]) is str and mission["combat"] in {"none", "optional_nonfatal_robots"}, "unsupported combat mode")
        unique_strings(mission["roles"], 2, 4, "roles")
        unique_strings(mission["learning_topics"], 1, 3, "learning_topics")
        require(set(mission["learning_topics"]) <= TOPICS, "unknown reuse topic")
        bounded_list(mission["objectives"], 2, 8, "objectives")
        by_id = {}
        for objective in mission["objectives"]:
            exact_keys(objective, {"id", "kind", "label", "requires", "required"}, "objective")
            identifier(objective["id"], "objective.id")
            require(objective["id"] not in by_id, "duplicate objective")
            by_id[objective["id"]] = objective
            require(type(objective["kind"]) is str and objective["kind"] in KINDS, "unsupported objective kind")
            text(objective["label"], "objective.label", 200)
            unique_strings(objective["requires"], 0, 7, "requires")
            require(type(objective["required"]) is bool, "required must be Boolean")
        required = {key for key, obj in by_id.items() if obj["required"]}
        require(bool(required), "at least one required objective")
        require(any(obj["required"] and obj["kind"] in {"escort", "welcome", "restore"} for obj in by_id.values()),
                "completion must include care, restoration or welcome")
        for key, obj in by_id.items():
            deps = set(obj["requires"])
            require(deps <= set(by_id) and key not in deps, "unknown/self dependency")
            require(not obj["required"] or deps <= required, "required objective depends on optional activity")
            require(obj["kind"] != "reflect" or not obj["required"], "reflection must remain optional")
        # Topological reachability catches longer cycles, including optional nodes.
        reached = set()
        while True:
            ready = {key for key, obj in by_id.items() if set(obj["requires"]) <= reached}
            updated = reached | ready
            if updated == reached:
                break
            reached = updated
        require(reached == set(by_id), "objective dependency cycle")
    return pack


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def _constant(_: str) -> None:
    raise ContractError("non-finite JSON number")


def load_bytes(data: bytes) -> dict:
    require(type(data) is bytes and 0 < len(data) <= MAX_BYTES, "packet size/type")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise ContractError(f"invalid JSON: {exc}") from exc
    return validate_pack(value)


def load_path(path: Path) -> dict:
    # Do not read an arbitrary-size input fully before applying the byte bound.
    with path.open("rb") as stream:
        return load_bytes(stream.read(MAX_BYTES + 1))


class ReferenceRun:
    """Offline authoring oracle, not networking, persistence, scoring or Unity code.

    The live adapter must independently validate/authenticate all player actions.
    Its world-state preconditions cannot be established by this reference model.
    """
    def __init__(self, pack: dict, mission_id: str):
        # Copy after validation so later mutation of an authoring dict cannot alter a run.
        checked = validate_pack(pack)
        self._pack = json.loads(json.dumps(checked))
        matches = [m for m in self._pack["missions"] if m["id"] == mission_id]
        require(len(matches) == 1, "unknown mission")
        self._objectives = {o["id"]: o for o in matches[0]["objectives"]}
        self._done: set[str] = set()
        self._left = False
        self._acknowledgements = 0

    @property
    def acknowledgements(self) -> int:
        return self._acknowledgements

    @property
    def completed(self) -> frozenset[str]:
        return frozenset(self._done)

    def complete(self, objective_id: str) -> str:
        identifier(objective_id, "event.objective_id")
        require(objective_id in self._objectives, "unknown objective")
        if self._left:
            return "closed"
        if objective_id in self._done:
            return "duplicate"
        if not set(self._objectives[objective_id]["requires"]) <= self._done:
            return "blocked"
        self._done.add(objective_id)
        required = {key for key, obj in self._objectives.items() if obj["required"]}
        if self._acknowledgements == 0 and required <= self._done:
            self._acknowledgements = 1
            return "completed"
        return "accepted"

    def leave(self) -> str:
        self._left = True
        return "left_without_penalty"


def main() -> int:
    try:
        require(len(sys.argv) <= 2, "usage: contract.py [mission-pack.json]")
        path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name("mission-pack.json")
        pack = load_path(path)
        print(f"PASS: {len(pack['missions'])} draft mission definitions; structural checks only")
        return 0
    except (ContractError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
