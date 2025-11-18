"""Serverless handler for Yoruba Dream Interpreter AI."""

import json
from typing import Any, Dict, List

SYMBOLS: List[Dict[str, Any]] = [
    {
        "keywords": ["river", "stream", "water", "lagoon"],
        "orisha": "Oshun",
        "meaning": "renewal, emotional clarity, gentle abundance",
        "symbolism": "Rivers signal the flow of intuition, creativity, and feminine power.",
    },
    {
        "keywords": ["lightning", "thunder", "fire", "volcano"],
        "orisha": "Shango",
        "meaning": "justice, courage, fiery transformation",
        "symbolism": "Lightning highlights moments where truth and courage must lead.",
    },
    {
        "keywords": ["metal", "iron", "weapon", "sword", "forge", "machine"],
        "orisha": "Ogun",
        "meaning": "work, resilience, conflict, craftsmanship",
        "symbolism": "Metal imagery points to discipline, labor, and the need to clear obstacles.",
    },
    {
        "keywords": ["storm", "wind", "whirlwind", "tornado"],
        "orisha": "Oya",
        "meaning": "change, transitions, new cycles",
        "symbolism": "Oya's winds announce endings that make room for new beginnings.",
    },
    {
        "keywords": ["crossroad", "road", "path", "intersection"],
        "orisha": "Esu",
        "meaning": "decision-making, duality, trickster insight",
        "symbolism": "Crossroads highlight choices where character and destiny align.",
    },
    {
        "keywords": ["snake", "serpent", "python"],
        "orisha": "Ancient serpent wisdom",
        "meaning": "transformation, renewal, hidden knowledge",
        "symbolism": "Snakes speak to healing, initiation, and evolving identity.",
    },
    {
        "keywords": ["tree", "forest", "roots", "wood"],
        "orisha": "Ancestors",
        "meaning": "grounding, lineage, protection",
        "symbolism": "Forests and trees reflect ancestral guidance and stability.",
    },
    {
        "keywords": ["falling", "slip", "crash"],
        "orisha": "Ori (inner head)",
        "meaning": "uncertainty, surrender, recalibration",
        "symbolism": "Falling dreams reveal fears about control and trust in destiny.",
    },
    {
        "keywords": ["flying", "levitating", "sky"],
        "orisha": "Ori + ancestral wind",
        "meaning": "liberation, higher calling, destiny clarity",
        "symbolism": "Flight signals freedom from weight and alignment with purpose.",
    },
    {
        "keywords": ["owl", "bat", "night animal", "panther"],
        "orisha": "Night guardians",
        "meaning": "mystery, hidden truth, spiritual sight",
        "symbolism": "Night creatures uncover secrets and sharpen intuition.",
    },
    {
        "keywords": ["sun", "sunrise", "fire", "flame"],
        "orisha": "Sun/Agba",
        "meaning": "vitality, purification, bold expression",
        "symbolism": "Solar images ignite confidence and burn away stagnation.",
    },
]

DEFAULT_MESSAGE = (
    "Your dream speaks through subtle currents of destiny (ori) and ancestral "
    "presence. Even without a clear symbol, it invites you to balance action and "
    "reflection, honor your inner guidance, and stay attentive to signs from "
    "your lineage."
)


def extract_matches(dream: str) -> List[Dict[str, str]]:
    """Return symbol records that appear in the dream text."""
    lowered = dream.lower()
    matches = []
    for symbol in SYMBOLS:
        if any(keyword in lowered for keyword in symbol["keywords"]):
            matches.append(symbol)
    return matches


def build_interpretation(matches: List[Dict[str, str]], dream: str) -> str:
    if not matches:
        return DEFAULT_MESSAGE

    lines = [
        "In Yoruba spirituality, your dream opens a portal of guidance.",
    ]

    for match in matches:
        lines.append(
            f"It resonates with {match['orisha']} — representing {match['meaning']}."
        )
        lines.append(match["symbolism"])

    lines.append(
        "Together, these signs suggest you are being nudged to align your ori with "
        "purpose, heed the counsel of ancestors, and act with confident balance."
    )
    return "\n".join(lines)


def handler(request):
    """Vercel serverless entry point."""
    payload = _extract_payload(request)

    dream_text = (payload or {}).get("dream", "").strip()

    if not dream_text:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Dream text is required."}),
        }

    matches = extract_matches(dream_text)
    interpretation = build_interpretation(matches, dream_text)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"interpretation": interpretation}),
    }


def _extract_payload(request) -> Dict[str, Any]:
    """Best-effort payload extraction compatible with Vercel + tests."""
    # If Vercel passes a dict (edge/runtime style)
    if isinstance(request, dict):
        body = request.get("body") or "{}"
        if request.get("isBase64Encoded"):
            try:
                import base64

                body = base64.b64decode(body).decode("utf-8")
            except Exception:  # pragma: no cover
                body = "{}"
        try:
            return json.loads(body or "{}")
        except Exception:  # pragma: no cover
            return {}

    # If request behaves like a flask/werkzeug request
    raw_body = getattr(request, "body", None) or getattr(request, "data", None)
    if raw_body:
        if isinstance(raw_body, bytes):
            raw_body = raw_body.decode("utf-8")
        try:
            return json.loads(raw_body or "{}")
        except Exception:  # pragma: no cover
            pass

    if callable(getattr(request, "json", None)):
        try:
            value = request.json() or {}
            if isinstance(value, dict):
                return value
        except Exception:  # pragma: no cover
            pass

    # As a last resort, look for query/body params
    if hasattr(request, "args") and "dream" in request.args:
        return {"dream": request.args.get("dream", "")}

    return {}
