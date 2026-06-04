from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


DATE = "2026-06-04"
REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "04_outputs" / "skilland_ia_mujeres" / "data_prep"

AYTO_CSV = REPO_ROOT / "04_outputs" / "skilland-ia-mujeres" / "ayuntamientos_contactos_igualdad_social" / "directorio_ayuntamientos_igualdad_social.csv"
AYTO_SEED = REPO_ROOT / "04_outputs" / "skilland-ia-mujeres" / "ayuntamientos_contactos_igualdad_social" / "municipios_canarias_seed.csv"
CABILDOS_CSV = REPO_ROOT / "04_outputs" / "skilland-ia-mujeres" / "cabildos_contactos_igualdad_social" / "directorio_cabildos_igualdad_social.csv"

UNKNOWN = "Unknown"

ORGANIZATION_FIELDS = [
    "organization_name",
    "organization_type",
    "island",
    "municipality",
    "department_area",
    "website",
    "email_main",
    "phone_main",
    "source_url",
    "source_file",
    "source_type",
    "icp_segment",
    "notes",
    "quality_flags",
    "needs_manual_review",
    "duplicate_possible",
]

CONTACT_FIELDS = [
    "organization_name",
    "contact_name",
    "role_title",
    "department_area",
    "email",
    "email_type",
    "phone",
    "island",
    "municipality",
    "source_url",
    "source_file",
    "source_type",
    "icp_segment",
    "notes",
    "quality_flags",
    "high_confidence",
    "generic_email",
    "needs_manual_review",
    "duplicate_possible",
]

COMBINED_FIELDS = [
    "record_type",
    "organization_name",
    "organization_type",
    "contact_name",
    "role_title",
    "department_area",
    "email",
    "email_type",
    "phone",
    "island",
    "municipality",
    "website",
    "source_url",
    "source_file",
    "source_type",
    "icp_segment",
    "high_confidence",
    "generic_email",
    "needs_manual_review",
    "duplicate_possible",
    "quality_flags",
    "notes",
]

GENERIC_LOCAL_PARTS = {
    "admin",
    "administracion",
    "alcaldia",
    "ayuntamiento",
    "cabildo",
    "contacto",
    "desarrollolocal",
    "empleo",
    "igualdad",
    "info",
    "mujer",
    "participacion",
    "registro",
    "sede",
    "serviciossociales",
}

ORG_EMAIL_RANK = {
    "generic_department": 3,
    "generic_institutional": 2,
    "personal": 1,
    "unknown": 0,
}

CONTACT_EMAIL_RANK = {
    "personal": 3,
    "generic_department": 2,
    "generic_institutional": 1,
    "unknown": 0,
}

CONFIDENCE_RANK = {
    "Alto": 3,
    "Medio": 2,
    "Bajo": 1,
    UNKNOWN: 0,
}

INVENTORY_SOURCES = [
    {
        "path": "04_outputs/skilland-ia-mujeres/Directorio_Igualdad_Empleo_Cabildos_Canarias.xlsx",
        "apparent_content": "Legacy cabildos spreadsheet focused on igualdad/empleo contacts in Canarias.",
        "likely_target": "cabildos",
        "usable_for_import": "partial",
        "notes": "Legacy spreadsheet at project root; treated as precursor source, not final normalized dataset.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.csv",
        "apparent_content": "Final tabular directory of cabildo contacts across igualdad, accion social and empleo.",
        "likely_target": "cabildos",
        "usable_for_import": "yes",
        "notes": "Primary structured source used for cabildo normalization.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.xlsx",
        "apparent_content": "Excel version of the final cabildo directory.",
        "likely_target": "cabildos",
        "usable_for_import": "partial",
        "notes": "Likely export of the final CSV; not used directly because CSV is easier to normalize reproducibly.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.md",
        "apparent_content": "Narrative report and tabular summary for the cabildo directory.",
        "likely_target": "cabildos",
        "usable_for_import": "no",
        "notes": "Used as contextual validation only.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/scraping_notes.md",
        "apparent_content": "Cabildo source methodology, source URLs and quality notes.",
        "likely_target": "cabildos",
        "usable_for_import": "no",
        "notes": "Useful for traceability, not for direct import.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/municipios_canarias_seed.csv",
        "apparent_content": "Seed list of the 88 municipalities with official websites and transparency URLs.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "partial",
        "notes": "Used to canonicalize municipality websites.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.csv",
        "apparent_content": "Final tabular directory of municipal contacts across igualdad, servicios sociales and related areas.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "yes",
        "notes": "Primary structured source used for ayuntamiento normalization.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.xlsx",
        "apparent_content": "Excel version of the final ayuntamiento directory.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "partial",
        "notes": "Likely export of the final CSV; not used directly because CSV is easier to normalize reproducibly.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.md",
        "apparent_content": "Narrative report and summary table for the ayuntamiento directory.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "no",
        "notes": "Used as contextual validation only.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/fuentes_ayuntamientos.json",
        "apparent_content": "JSON traceability map of municipalities and official sources consulted.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "partial",
        "notes": "Useful for traceability and source audits, not for direct CRM import.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/coverage_report.md",
        "apparent_content": "Coverage summary by island for municipal directory production.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "no",
        "notes": "Coverage QA summary only.",
    },
    {
        "path": "04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/scraping_notes_ayuntamientos.md",
        "apparent_content": "Municipal methodology and data quality notes.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "no",
        "notes": "Useful for traceability, not for direct import.",
    },
    {
        "path": "05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv",
        "apparent_content": "Scratch raw directory for ayuntamientos before final export.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "partial",
        "notes": "Intermediate scratch dataset; final CSV in 04_outputs takes precedence.",
    },
    {
        "path": "05_scratch/ayuntamientos_contactos_igualdad_social/local_curated_rows.csv",
        "apparent_content": "Partial locally curated municipal rows used during assembly.",
        "likely_target": "ayuntamientos",
        "usable_for_import": "no",
        "notes": "Intermediate partial file with incomplete coverage.",
    },
]


def clean_text(value: object) -> str:
    if value is None:
        return UNKNOWN
    text = str(value).strip()
    if not text:
        return UNKNOWN
    normalized = re.sub(r"\s+", " ", text)
    if normalized.lower() in {"unknown", "n/a", "na", "none", "null"}:
        return UNKNOWN
    return normalized


def slug_key(value: str) -> str:
    lowered = clean_text(value).lower()
    lowered = lowered.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ü", "u").replace("ñ", "n")
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    return lowered.strip("_")


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def split_emails(value: str) -> list[str]:
    text = clean_text(value)
    if text == UNKNOWN:
        return []
    pieces = re.split(r"\s*/\s*|\s*;\s*|\s*,\s*", text)
    emails: list[str] = []
    seen: set[str] = set()
    for piece in pieces:
        candidate = piece.strip().lower()
        if not candidate or candidate == "unknown":
            continue
        if "@" not in candidate:
            continue
        if candidate not in seen:
            seen.add(candidate)
            emails.append(candidate)
    return emails


def normalize_phone(value: str) -> str:
    text = clean_text(value)
    if text == UNKNOWN:
        return UNKNOWN
    text = text.replace(" / ", " | ")
    text = re.sub(r"\s+", " ", text)
    return text


def phone_tokens(value: str) -> list[str]:
    text = normalize_phone(value)
    if text == UNKNOWN:
        return []
    return [part.strip() for part in text.split("|") if part.strip()]


def phone_key(value: str) -> str:
    digits = re.sub(r"\D+", "", value)
    return digits if digits else ""


def canonical_url(value: str) -> str:
    text = clean_text(value)
    if text == UNKNOWN:
        return UNKNOWN
    return text


def root_website(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return UNKNOWN
    return f"{parsed.scheme}://{parsed.netloc}"


DEPARTMENT_EMAIL_KEYWORDS = ("igualdad", "mujer", "empleo", "social", "sociales", "participacion", "desarrollolocal", "bienestar", "accionsocial")
INSTITUTIONAL_EMAIL_KEYWORDS = ("info", "contact", "registro", "sede", "administracion", "admin", "ayuntamiento", "cabildo", "alcaldia", "portal", "atencionciudadana", "gobiernoabierto", "informacion", "oiac")

def normalized_email_local_part(email: str) -> str:
    candidate = clean_text(email).lower()
    if candidate == UNKNOWN.lower() or "@" not in candidate:
        return ""
    local_part = candidate.split("@", 1)[0]
    return re.sub(r"[^a-z]", "", local_part)


def classify_email_type(email: str) -> str:
    normalized = normalized_email_local_part(email)
    if not normalized:
        return "unknown"
    if any(keyword in normalized for keyword in DEPARTMENT_EMAIL_KEYWORDS):
        return "generic_department"
    if any(keyword in normalized for keyword in INSTITUTIONAL_EMAIL_KEYWORDS):
        return "generic_institutional"
    if normalized in GENERIC_LOCAL_PARTS or any(normalized.startswith(prefix) for prefix in GENERIC_LOCAL_PARTS):
        return "generic_institutional"
    return "personal"


def is_generic_email(email: str) -> bool:
    return classify_email_type(email) in {"generic_department", "generic_institutional"}


def review_note_requires_manual_review(review_note: str, email_type: str) -> bool:
    note = slug_key(review_note)
    if note == UNKNOWN.lower():
        return False
    positive_tokens = ("validar", "confirmar", "revalidar", "localizar", "buscar", "recuperar", "segunda_pasada", "conviene", "contrastar", "no_confirmado")
    benign_tokens = ("no_se_localizo_un_email_generico_municipal_mas_util", "no_se_localizo_email_personal", "no_se_localizo_correo_personal")
    if any(token in note for token in benign_tokens):
        return False
    if any(token in note for token in positive_tokens):
        return True
    if "no_localice_email_publico" in note and email_type == "generic_institutional":
        return True
    return False


def normalize_department_area(raw_text: str) -> str:
    text = clean_text(raw_text)
    if text == UNKNOWN:
        return UNKNOWN
    lowered = slug_key(text)
    areas: list[str] = []

    def add(label: str) -> None:
        if label not in areas:
            areas.append(label)

    if "igualdad" in lowered or "diversidad" in lowered or "violencia_genero" in lowered or "lgtbi" in lowered:
        add("Igualdad")
    if "mujer" in lowered:
        add("Mujer")
    if any(token in lowered for token in ["servicios_sociales", "accion_social", "bienestar_social", "politica_social", "politicas_sociales", "asuntos_sociales", "derechos_sociales", "atencion_social", "inclusion"]):
        add("Politicas Sociales")
    if "empleo" in lowered or "empleabilidad" in lowered:
        add("Empleo")
    if "desarrollo_local" in lowered or "promocion_economica" in lowered:
        add("Desarrollo Local")
    if "participacion_ciudadana" in lowered:
        add("Participacion Ciudadana")
    if "educacion" in lowered or "formacion" in lowered:
        add("Educacion")
    if "juventud" in lowered:
        add("Juventud")

    return " / ".join(areas) if areas else UNKNOWN


def icp_segment(organization_type: str, department_area: str) -> str:
    area = clean_text(department_area)
    if area == UNKNOWN:
        return "Unknown"
    if organization_type == "cabildo":
        if "Igualdad" in area or "Mujer" in area:
            return "Cabildo - Igualdad"
        if "Empleo" in area or "Desarrollo Local" in area or "Educacion" in area:
            return "Cabildo - Empleo"
        if "Politicas Sociales" in area or "Participacion Ciudadana" in area:
            return "Cabildo - Politicas Sociales"
        return "Unknown"
    if organization_type == "ayuntamiento":
        if "Igualdad" in area or "Mujer" in area:
            return "Ayuntamiento - Igualdad"
        if "Empleo" in area:
            return "Ayuntamiento - Empleo"
        if "Desarrollo Local" in area:
            return "Ayuntamiento - Desarrollo Local"
        if any(label in area for label in ["Politicas Sociales", "Participacion Ciudadana", "Educacion", "Juventud"]):
            return "Entidad Publica - Igualdad/Empleo"
        return "Unknown"
    return "Unknown"


def source_type_from_hint(hint: str, source_url: str) -> str:
    hint_text = slug_key(hint)
    url_text = clean_text(source_url).lower()
    if hint_text == UNKNOWN.lower() and url_text == UNKNOWN.lower():
        return "unknown"
    if any(token in hint_text for token in ["directorio", "miembros_electos"]) or any(token in url_text for token in ["directorio", "organigrama", "transparencia", "/portal/transparencia/"]):
        return "institutional_directory"
    if any(token in hint_text for token in ["grupo_de_gobierno", "corporacion_municipal", "organizacion_politica", "equipo_de_gobierno", "concejalia", "ficha_de_cargo", "gobierno_municipal", "area_municipal", "servicio_municipal"]):
        return "official_website"
    if url_text.endswith(".pdf"):
        return "official_website"
    return "official_website"


def confidence_rank(value: str) -> int:
    return CONFIDENCE_RANK.get(clean_text(value), 0)


def segment_rank(segment: str) -> int:
    order = {
        "Cabildo - Igualdad": 5,
        "Ayuntamiento - Igualdad": 5,
        "Cabildo - Empleo": 4,
        "Ayuntamiento - Empleo": 4,
        "Cabildo - Politicas Sociales": 3,
        "Ayuntamiento - Desarrollo Local": 3,
        "Entidad Publica - Igualdad/Empleo": 2,
        "Unknown": 0,
    }
    return order.get(segment, 1)


def compose_contact_notes(source_confidence: str, confidence_reason: str, review_note: str, secondary_source: str, extra_note: str = "") -> str:
    parts: list[str] = []
    if clean_text(source_confidence) != UNKNOWN:
        parts.append(f"Source confidence: {clean_text(source_confidence)}.")
    if clean_text(confidence_reason) != UNKNOWN:
        parts.append(clean_text(confidence_reason))
    if clean_text(review_note) != UNKNOWN:
        parts.append(f"Review note: {clean_text(review_note)}.")
    if clean_text(secondary_source) != UNKNOWN:
        parts.append(f"Secondary source: {clean_text(secondary_source)}.")
    if clean_text(extra_note) != UNKNOWN:
        parts.append(clean_text(extra_note))
    return " ".join(parts) if parts else UNKNOWN
def build_quality_flags(
    *,
    contact_name: str,
    role_title: str,
    department_area: str,
    email: str,
    email_type: str,
    phone: str,
    source_confidence: str,
    original_email_count: int,
    review_note: str,
) -> set[str]:
    flags: set[str] = set()
    review_required = review_note_requires_manual_review(review_note, email_type)
    if email == UNKNOWN:
        flags.add("missing_email")
    if phone == UNKNOWN:
        flags.add("missing_phone")
    if email == UNKNOWN and phone == UNKNOWN:
        flags.add("missing_email_and_phone")
    if contact_name == UNKNOWN:
        flags.add("unknown_contact_name")
    if role_title == UNKNOWN:
        flags.add("unknown_role_title")
    if department_area == UNKNOWN:
        flags.add("unknown_department_area")
    if original_email_count > 1:
        flags.add("multiple_emails_in_source")
    if email_type == "generic_department":
        flags.add("generic_department_email")
    if email_type == "generic_institutional":
        flags.add("generic_institutional_email")
    if clean_text(source_confidence) == "Medio":
        flags.add("source_confidence_medium")
    if clean_text(source_confidence) == "Bajo":
        flags.add("source_confidence_low")
    if review_required:
        flags.add("review_required_from_source_note")
    return flags


def needs_manual_review(
    *,
    contact_name: str,
    role_title: str,
    department_area: str,
    email: str,
    email_type: str,
    phone: str,
    source_confidence: str,
    review_note: str,
    merged_duplicate: bool = False,
) -> bool:
    if email == UNKNOWN and phone == UNKNOWN:
        return True
    if contact_name == UNKNOWN:
        return True
    if role_title == UNKNOWN:
        return True
    if department_area == UNKNOWN:
        return True
    if email_type == "generic_institutional":
        return True
    if clean_text(source_confidence) == "Bajo":
        return True
    if review_note_requires_manual_review(review_note, email_type):
        return True
    if merged_duplicate:
        return True
    return False

def high_confidence(*, organization_name: str, department_area: str, email: str, phone: str, source_url: str) -> bool:
    has_org = clean_text(organization_name) != UNKNOWN
    has_channel = email != UNKNOWN or phone != UNKNOWN
    has_source = clean_text(source_url) != UNKNOWN
    fits = department_area != UNKNOWN and any(token in department_area for token in ["Igualdad", "Mujer", "Empleo", "Politicas Sociales", "Desarrollo Local", "Participacion Ciudadana", "Educacion", "Juventud"])
    return has_org and has_channel and has_source and fits


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{key: value for key, value in row.items()} for row in reader]


def load_seed_websites() -> dict[str, str]:
    websites: dict[str, str] = {}
    for row in load_csv(AYTO_SEED):
        websites[clean_text(row["Ayuntamiento"])] = clean_text(row["URL oficial ayuntamiento"])
    return websites


def choose_phone(primary: str, fallback: str) -> str:
    first = normalize_phone(primary)
    second = normalize_phone(fallback)
    if first != UNKNOWN:
        return first
    if second != UNKNOWN:
        return second
    return UNKNOWN


def build_contact_rows() -> list[dict[str, str]]:
    contact_rows: list[dict[str, str]] = []
    websites = load_seed_websites()

    for source_path, source_kind in [(AYTO_CSV, "ayuntamiento"), (CABILDOS_CSV, "cabildo")]:
        for row in load_csv(source_path):
            if source_kind == "ayuntamiento":
                organization_name = clean_text(row["Ayuntamiento"])
                organization_type = "ayuntamiento"
                island = clean_text(row["Isla"])
                municipality = clean_text(row["Municipio"])
                raw_area = clean_text(row["Area / Concejalia / Servicio"])
                role_title = clean_text(row["Cargo exacto"])
                contact_name = clean_text(row["Nombre y apellidos"])
                personal_emails = split_emails(row["Email institucional personal"])
                area_emails = split_emails(row["Email del area / concejalia / servicio"])
                fallback_emails = split_emails(row["Email generico municipal"])
                source_url = canonical_url(row["URL fuente principal"])
                secondary_source = canonical_url(row["URL fuente secundaria"])
                source_conf = clean_text(row["Nivel de confianza"])
                confidence_reason = clean_text(row["Motivo del nivel de confianza"])
                review_note = clean_text(row["Dudas pendientes / validacion manual necesaria"])
                source_hint = clean_text(row["Tipo de fuente principal"])
                phone = choose_phone(row["Telefono directo"], row["Telefono general"])
                website = clean_text(websites.get(organization_name, UNKNOWN))
            else:
                organization_name = clean_text(row["Cabildo"])
                organization_type = "cabildo"
                island = clean_text(row["Isla"])
                municipality = UNKNOWN
                raw_area = clean_text(row["Area_Consejeria_Servicio"])
                role_title = clean_text(row["Cargo_exacto"])
                contact_name = clean_text(row["Nombre_y_apellidos"])
                personal_emails = split_emails(row["Email_personal_institucional"])
                area_emails = split_emails(row["Email_area_consejeria"])
                fallback_emails = split_emails(row["Email_generico_fallback"])
                source_url = canonical_url(row["URL_fuente_principal"])
                secondary_source = canonical_url(row["URL_fuente_secundaria"])
                source_conf = clean_text(row["Nivel_confianza"])
                confidence_reason = clean_text(row["Motivo_confianza"])
                review_note = UNKNOWN
                comparison_note = clean_text(row["Comparativa_excel_inicial"])
                source_hint = UNKNOWN
                phone = normalize_phone(row["Telefono"])
                website = root_website(source_url)

            department_area = normalize_department_area(raw_area)
            segment = icp_segment(organization_type, department_area)
            source_type = source_type_from_hint(source_hint, source_url)
            all_emails = []
            for email in personal_emails + area_emails + fallback_emails:
                if email not in all_emails:
                    all_emails.append(email)
            if not all_emails:
                all_emails = [UNKNOWN]

            extra_note = ""
            if source_kind == "cabildo":
                extra_note = comparison_note
            email_total = len([email for email in all_emails if email != UNKNOWN])

            for email in all_emails:
                email_type = classify_email_type(email) if email != UNKNOWN else "unknown"
                generic = is_generic_email(email)
                flags = build_quality_flags(
                    contact_name=contact_name,
                    role_title=role_title,
                    department_area=department_area,
                    email=email,
                    email_type=email_type,
                    phone=phone,
                    source_confidence=source_conf,
                    original_email_count=email_total,
                    review_note=review_note,
                )
                manual_review = needs_manual_review(
                    contact_name=contact_name,
                    role_title=role_title,
                    department_area=department_area,
                    email=email,
                    email_type=email_type,
                    phone=phone,
                    source_confidence=source_conf,
                    review_note=review_note,
                )
                record = {
                    "organization_name": organization_name,
                    "organization_type": organization_type,
                    "contact_name": contact_name,
                    "role_title": role_title,
                    "department_area": department_area,
                    "email": email,
                    "email_type": email_type,
                    "phone": phone,
                    "island": island,
                    "municipality": municipality,
                    "website": website,
                    "source_url": source_url,
                    "source_file": str(source_path.relative_to(REPO_ROOT)),
                    "source_type": source_type,
                    "icp_segment": segment,
                    "notes": compose_contact_notes(
                        source_confidence=source_conf,
                        confidence_reason=confidence_reason,
                        review_note=review_note,
                        secondary_source=secondary_source,
                        extra_note=extra_note,
                    ),
                    "quality_flags": ";".join(sorted(flags)) if flags else UNKNOWN,
                    "high_confidence": bool_str(
                        high_confidence(
                            organization_name=organization_name,
                            department_area=department_area,
                            email=email,
                            phone=phone,
                            source_url=source_url,
                        )
                    ),
                    "generic_email": bool_str(generic),
                    "needs_manual_review": bool_str(manual_review),
                    "duplicate_possible": "false",
                    "_source_confidence": source_conf,
                    "_confidence_rank": str(confidence_rank(source_conf)),
                    "_website": website,
                }
                contact_rows.append(record)
    return contact_rows


def row_score(row: dict[str, str]) -> tuple[int, int, int, int, int]:
    return (
        1 if row["high_confidence"] == "true" else 0,
        1 if row["needs_manual_review"] == "false" else 0,
        int(row["_confidence_rank"]),
        1 if row["contact_name"] != UNKNOWN else 0,
        CONTACT_EMAIL_RANK.get(row["email_type"], 0),
    )


def merge_text_values(values: Iterable[str], sep: str = " | ") -> str:
    ordered: list[str] = []
    for value in values:
        cleaned = clean_text(value)
        if cleaned == UNKNOWN:
            continue
        if cleaned not in ordered:
            ordered.append(cleaned)
    return sep.join(ordered) if ordered else UNKNOWN


def merge_flag_values(values: Iterable[str]) -> str:
    flags: set[str] = set()
    for value in values:
        cleaned = clean_text(value)
        if cleaned == UNKNOWN:
            continue
        flags.update(flag for flag in cleaned.split(";") if flag)
    return ";".join(sorted(flags)) if flags else UNKNOWN


def dedupe_contacts(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped: dict[str, dict[str, str]] = {}
    alternates: dict[str, list[str]] = defaultdict(list)

    for index, row in enumerate(rows, start=1):
        email_key = row["email"].lower() if row["email"] != UNKNOWN else ""
        if email_key:
            key = f"email::{email_key}"
        else:
            key = "fallback::{org}::{name}::{role}::{dept}::{idx}".format(
                org=slug_key(row["organization_name"]),
                name=slug_key(row["contact_name"]),
                role=slug_key(row["role_title"]),
                dept=slug_key(row["department_area"]),
                idx=index,
            )
        existing = deduped.get(key)
        if not existing:
            deduped[key] = dict(row)
            deduped[key]["_duplicate_hits"] = "1"
            continue
        winner, loser = (existing, row) if row_score(existing) >= row_score(row) else (row, existing)
        merged = dict(winner)
        merged["source_url"] = merge_text_values([existing["source_url"], row["source_url"]])
        merged["source_file"] = merge_text_values([existing["source_file"], row["source_file"]], sep=";")
        merged["source_type"] = merge_text_values([existing["source_type"], row["source_type"]], sep=";")
        merged["notes"] = merge_text_values([existing["notes"], row["notes"]])
        merged["quality_flags"] = merge_flag_values([existing["quality_flags"], row["quality_flags"], "shared_email_duplicate"])
        merged["needs_manual_review"] = "true" if "true" in {existing["needs_manual_review"], row["needs_manual_review"]} else "false"
        merged["high_confidence"] = "true" if "true" in {existing["high_confidence"], row["high_confidence"]} else "false"
        merged["duplicate_possible"] = "true"
        merged["_confidence_rank"] = str(max(int(existing["_confidence_rank"]), int(row["_confidence_rank"])))
        merged["_duplicate_hits"] = str(int(existing.get("_duplicate_hits", "1")) + 1)
        alt_identity = "{name} ({role})".format(name=clean_text(loser["contact_name"]), role=clean_text(loser["role_title"]))
        if alt_identity not in alternates[key]:
            alternates[key].append(alt_identity)
        deduped[key] = merged

    results: list[dict[str, str]] = []
    for key, row in deduped.items():
        if alternates.get(key):
            row["notes"] = merge_text_values(
                [
                    row["notes"],
                    "Shared email also referenced for: " + ", ".join(alternates[key]) + ".",
                ]
            )
            row["quality_flags"] = merge_flag_values([row["quality_flags"], "shared_email_duplicate"])
            row["duplicate_possible"] = "true"
            row["needs_manual_review"] = "true"
        results.append(row)

    phone_map: dict[str, set[str]] = defaultdict(set)
    for row in results:
        for token in phone_tokens(row["phone"]):
            token_key = phone_key(token)
            if token_key:
                phone_map[token_key].add(f"{row['organization_name']}::{row['department_area']}")

    for row in results:
        duplicate_phone = False
        for token in phone_tokens(row["phone"]):
            token_key = phone_key(token)
            if token_key and len(phone_map[token_key]) > 1:
                duplicate_phone = True
        if duplicate_phone:
            row["duplicate_possible"] = "true"
            row["quality_flags"] = merge_flag_values([row["quality_flags"], "shared_phone"])

    for row in results:
        row["needs_manual_review"] = bool_str(
            needs_manual_review(
                contact_name=row["contact_name"],
                role_title=row["role_title"],
                department_area=row["department_area"],
                email=row["email"],
                email_type=row["email_type"],
                phone=row["phone"],
                source_confidence=row["_source_confidence"],
                review_note=UNKNOWN if "review_required_from_source_note" not in row["quality_flags"] else "flagged",
                merged_duplicate=row["duplicate_possible"] == "true",
            )
        )
    return sorted(results, key=lambda item: (item["organization_name"], item["contact_name"], item["email"], item["role_title"]))


def best_org_email(rows: list[dict[str, str]]) -> str:
    ranked = sorted(
        rows,
        key=lambda row: (
            ORG_EMAIL_RANK.get(row["email_type"], 0),
            segment_rank(row["icp_segment"]),
            int(row["_confidence_rank"]),
        ),
        reverse=True,
    )
    for row in ranked:
        if row["email"] != UNKNOWN:
            return row["email"]
    return UNKNOWN


def best_org_phone(rows: list[dict[str, str]]) -> str:
    phones = [row["phone"] for row in rows if row["phone"] != UNKNOWN]
    if not phones:
        return UNKNOWN
    counter = Counter(phones)
    return sorted(counter.items(), key=lambda item: (item[1], item[0]), reverse=True)[0][0]


def organization_rows(contacts: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in contacts:
        grouped[row["organization_name"]].append(row)

    organizations: list[dict[str, str]] = []
    for organization_name, rows in grouped.items():
        organization_type = rows[0]["organization_type"]
        island = merge_text_values(row["island"] for row in rows)
        municipality = merge_text_values(row["municipality"] for row in rows)
        website = merge_text_values(row["_website"] for row in rows)
        department_area = merge_text_values((row["department_area"] for row in rows), sep=";")
        source_urls = merge_text_values(row["source_url"] for row in rows)
        source_files = merge_text_values((row["source_file"] for row in rows), sep=";")
        source_types = merge_text_values((row["source_type"] for row in rows), sep=";")
        segments = merge_text_values((row["icp_segment"] for row in rows), sep=";")
        flags = merge_flag_values(row["quality_flags"] for row in rows)

        org_notes = [
            f"Merged from {len(rows)} contact rows.",
        ]
        unique_emails = sorted({row["email"] for row in rows if row["email"] != UNKNOWN})
        if unique_emails:
            org_notes.append(f"Unique emails retained: {len(unique_emails)}.")
        if ";" in department_area:
            org_notes.append("Multiple relevant department areas retained.")
        manual_review_count = sum(1 for row in rows if row["needs_manual_review"] == "true")
        if manual_review_count:
            org_notes.append(f"Manual review flagged on {manual_review_count} contact rows.")

        combined_flags = flags
        if len({row["department_area"] for row in rows if row["department_area"] != UNKNOWN}) > 1:
            combined_flags = merge_flag_values([combined_flags, "multi_area"])
        if len({row["icp_segment"] for row in rows if row["icp_segment"] != UNKNOWN}) > 1:
            combined_flags = merge_flag_values([combined_flags, "multi_segment"])

        organizations.append(
            {
                "organization_name": organization_name,
                "organization_type": organization_type,
                "island": island,
                "municipality": municipality,
                "department_area": department_area,
                "website": website,
                "email_main": best_org_email(rows),
                "phone_main": best_org_phone(rows),
                "source_url": source_urls,
                "source_file": source_files,
                "source_type": source_types,
                "icp_segment": segments,
                "notes": " ".join(org_notes),
                "quality_flags": combined_flags,
                "needs_manual_review": bool_str(
                    any(row["needs_manual_review"] == "true" for row in rows)
                    or all(row["email"] == UNKNOWN for row in rows)
                ),
                "duplicate_possible": "false",
            }
        )
    return sorted(organizations, key=lambda item: (item["organization_type"], item["organization_name"]))


def import_ready_rows(organizations: list[dict[str, str]], contacts: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for org in organizations:
        rows.append(
            {
                "record_type": "organization",
                "organization_name": org["organization_name"],
                "organization_type": org["organization_type"],
                "contact_name": UNKNOWN,
                "role_title": UNKNOWN,
                "department_area": org["department_area"],
                "email": org["email_main"],
                "email_type": classify_email_type(org["email_main"]) if org["email_main"] != UNKNOWN else "unknown",
                "phone": org["phone_main"],
                "island": org["island"],
                "municipality": org["municipality"],
                "website": org["website"],
                "source_url": org["source_url"],
                "source_file": org["source_file"],
                "source_type": org["source_type"],
                "icp_segment": org["icp_segment"],
                "high_confidence": "false",
                "generic_email": bool_str(is_generic_email(org["email_main"])),
                "needs_manual_review": org["needs_manual_review"],
                "duplicate_possible": org["duplicate_possible"],
                "quality_flags": org["quality_flags"],
                "notes": org["notes"],
            }
        )
    for contact in contacts:
        rows.append(
            {
                "record_type": "contact",
                "organization_name": contact["organization_name"],
                "organization_type": contact["organization_type"],
                "contact_name": contact["contact_name"],
                "role_title": contact["role_title"],
                "department_area": contact["department_area"],
                "email": contact["email"],
                "email_type": contact["email_type"],
                "phone": contact["phone"],
                "island": contact["island"],
                "municipality": contact["municipality"],
                "website": contact["_website"],
                "source_url": contact["source_url"],
                "source_file": contact["source_file"],
                "source_type": contact["source_type"],
                "icp_segment": contact["icp_segment"],
                "high_confidence": contact["high_confidence"],
                "generic_email": contact["generic_email"],
                "needs_manual_review": contact["needs_manual_review"],
                "duplicate_possible": contact["duplicate_possible"],
                "quality_flags": contact["quality_flags"],
                "notes": contact["notes"],
            }
        )
    return rows


def csv_record_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def json_record_count(path: Path) -> int | str:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        return len(data)
    if isinstance(data, list):
        return len(data)
    return UNKNOWN


def inventory_count(path: Path) -> int | str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return csv_record_count(path)
    if suffix == ".json":
        return json_record_count(path)
    return UNKNOWN


def inventory_markdown() -> str:
    lines = [
        f"# Dataset Inventory - SkilLand IA Mujeres",
        "",
        f"- Date: {DATE}",
        "- Scope: datasets and traceability files located in the existing repo and evaluated for CRM data prep.",
        "- Note: no structured association dataset was found in the inspected CSV/XLSX/JSON sources; the usable tabular data is concentrated in cabildos and ayuntamientos.",
        "",
        "| file_path | file_type | apparent_content | likely_target | record_count_if_known | usable_for_import | notes |",
        "|---|---|---|---|---:|---|---|",
    ]
    for item in INVENTORY_SOURCES:
        path = REPO_ROOT / item["path"]
        count = inventory_count(path) if path.exists() else UNKNOWN
        count_text = str(count) if count != UNKNOWN else "Unknown"
        lines.append(
            "| {path} | {file_type} | {content} | {target} | {count} | {usable} | {notes} |".format(
                path=item["path"],
                file_type=path.suffix.lower().lstrip(".") or "unknown",
                content=item["apparent_content"],
                target=item["likely_target"],
                count=count_text,
                usable=item["usable_for_import"],
                notes=item["notes"],
            )
        )
    return "\n".join(lines) + "\n"


def segment_distribution(organizations: list[dict[str, str]], contacts: list[dict[str, str]]) -> list[dict[str, object]]:
    segments = [
        "Cabildo - Igualdad",
        "Cabildo - Empleo",
        "Cabildo - Politicas Sociales",
        "Ayuntamiento - Igualdad",
        "Ayuntamiento - Empleo",
        "Ayuntamiento - Desarrollo Local",
        "Entidad Publica - Igualdad/Empleo",
        "Unknown",
    ]
    rows: list[dict[str, object]] = []
    for segment in segments:
        org_count = sum(1 for org in organizations if segment in org["icp_segment"].split(";"))
        contact_subset = [contact for contact in contacts if contact["icp_segment"] == segment]
        email_count = sum(1 for contact in contact_subset if contact["email"] != UNKNOWN)
        rows.append(
            {
                "icp_segment": segment,
                "organizations": org_count,
                "contacts": len(contact_subset),
                "emails": email_count,
                "high_confidence": sum(1 for contact in contact_subset if contact["high_confidence"] == "true"),
                "needs_manual_review": sum(1 for contact in contact_subset if contact["needs_manual_review"] == "true"),
            }
        )
    return rows


def quality_report(organizations: list[dict[str, str]], contacts: list[dict[str, str]], combined: list[dict[str, str]]) -> str:
    cabildos = sum(1 for row in organizations if row["organization_type"] == "cabildo")
    ayuntamientos = sum(1 for row in organizations if row["organization_type"] == "ayuntamiento")
    others = len(organizations) - cabildos - ayuntamientos
    personal_emails = sum(1 for row in contacts if row["email_type"] == "personal")
    generic_emails = sum(1 for row in contacts if row["generic_email"] == "true")
    high_conf = sum(1 for row in combined if row["high_confidence"] == "true")
    manual_review = sum(1 for row in combined if row["needs_manual_review"] == "true")
    duplicates = sum(1 for row in combined if row["duplicate_possible"] == "true")

    missing_email = sum(1 for row in contacts if row["email"] == UNKNOWN)
    missing_phone = sum(1 for row in contacts if row["phone"] == UNKNOWN)
    generic_institutional = sum(1 for row in contacts if row["email_type"] == "generic_institutional")
    low_confidence = sum(1 for row in contacts if row["_source_confidence"] == "Bajo")
    unknown_names = sum(1 for row in contacts if row["contact_name"] == UNKNOWN)

    source_rows = [
        ("04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.csv", "spreadsheet", 88, "Primary municipal contact directory used for contacts and organizations."),
        ("04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.csv", "spreadsheet", 16, "Primary cabildo contact directory used for contacts and organizations."),
        ("04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/municipios_canarias_seed.csv", "spreadsheet", 88, "Used only to canonicalize municipal organization websites."),
    ]

    lines = [
        f"# Data Quality Report - SkilLand IA Mujeres",
        "",
        f"- Date: {DATE}",
        "- Note: `high_confidence`, `needs_manual_review` and duplicate totals below are reported on the combined review dataset unless stated otherwise.",
        "",
        "## 1. Resumen ejecutivo",
        "",
        f"- Total organizations: {len(organizations)}",
        f"- Total contacts: {len(contacts)}",
        f"- Cabildos: {cabildos}",
        f"- Ayuntamientos: {ayuntamientos}",
        f"- Asociaciones u otras entidades: {others}",
        f"- Emails personales: {personal_emails}",
        f"- Emails genericos: {generic_emails}",
        f"- Registros `high_confidence`: {high_conf}",
        f"- Registros `needs_manual_review`: {manual_review}",
        f"- Posibles duplicados: {duplicates}",
        "",
        "## 2. Fuentes utilizadas",
        "",
        "| source_file | source_type | records_used | notes |",
        "|---|---|---:|---|",
    ]
    for source_file, source_type, records_used, notes in source_rows:
        lines.append(f"| {source_file} | {source_type} | {records_used} | {notes} |")

    lines.extend(
        [
            "",
            "## 3. Distribucion por segmento",
            "",
            "| icp_segment | organizations | contacts | emails | high_confidence | needs_manual_review |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in segment_distribution(organizations, contacts):
        lines.append(
            "| {icp_segment} | {organizations} | {contacts} | {emails} | {high_confidence} | {needs_manual_review} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## 4. Problemas detectados",
            "",
            "### Datos incompletos",
            "",
            f"- Contact rows without email: {missing_email}.",
            f"- Contact rows without phone: {missing_phone}.",
            f"- Contact rows without named person: {unknown_names}.",
            "",
            "### Emails genericos",
            "",
            f"- Generic email rows: {generic_emails}.",
            f"- Generic institutional email rows: {generic_institutional}.",
            "- Department emails are common and often more useful than personal emails, but they still need manual routing expectations.",
            "",
            "### Duplicados",
            "",
            f"- Records flagged as possible duplicates: {duplicates}.",
            "- Main duplicate driver is exact email reuse across multiple roles or shared central phones.",
            "",
            "### Fuentes ambiguas",
            "",
            f"- Low source confidence rows: {low_confidence}.",
            "- Medium-confidence rows usually rely on generic institutional channels or missing direct role-level contact data.",
            "",
            "### Campos no homologables",
            "",
            "- Source files mix political areas, service units and directorios; `department_area` was normalized into CRM-friendly categories.",
            "- Some source rows contained multiple emails in one field; they were split conservatively into one email per contact row.",
            "",
            "### Registros que necesitan revision manual",
            "",
            f"- Combined rows flagged for manual review: {manual_review}.",
            "- Review is concentrated in generic institutional emails, unknown named contacts, low-confidence sources and merged duplicate channels.",
            "",
            "## 5. Recomendacion para importacion en CRM",
            "",
            f"- Import organizations from `04_outputs/skilland_ia_mujeres/data_prep/organizations_clean.csv`.",
            f"- Import contacts from `04_outputs/skilland_ia_mujeres/data_prep/contacts_clean.csv`.",
            "- Map native fields first: organization/contact names, email, phone, website, municipality, notes.",
            "- Create only the minimum custom campaign fields listed in the Twenty mapping document: `campaign_name`, `icp_segment`, `department_area`, `source_type`, `source_url`, `high_confidence`, `needs_manual_review`, `generic_email`.",
            "- Manually review all rows marked `needs_manual_review=true` before production import; do not blind-import the generic institutional duplicates.",
            "- Dataset readiness: yes for Phase 2 as a review-ready CRM import base, but not for zero-touch import.",
        ]
    )
    return "\n".join(lines) + "\n"


def twenty_mapping() -> str:
    return "\n".join(
        [
            "# Twenty Import Mapping - SkilLand IA Mujeres",
            "",
            f"- Date: {DATE}",
            "- Assumption: standard Twenty objects are `Companies` and `People`, with the listed campaign fields created as lightweight custom fields if they do not already exist.",
            "",
            "## Organizations / Companies",
            "",
            "| CSV field | Twenty object | Twenty field | Notes |",
            "|---|---|---|---|",
            "| organization_name | Companies | Name | Required primary company label. |",
            "| organization_type | Companies | Custom field: organization_type | Useful to separate cabildos from ayuntamientos. |",
            "| island | Companies | Custom field: island | Retain island-level routing context. |",
            "| municipality | Companies | City or Custom field: municipality | Use a custom field if the standard city field is already reserved for another purpose. |",
            "| department_area | Companies | Custom field: department_area | Multi-area values are semicolon-separated. |",
            "| website | Companies | Domain / Website | Use the canonical institutional website. |",
            "| email_main | Companies | Primary email | Company-level default channel; often department or institutional email. |",
            "| phone_main | Companies | Primary phone | Retains the best available institutional phone. |",
            "| source_url | Companies | Custom field: source_url | Traceability back to the public source. |",
            "| source_file | Companies | Custom field: source_file | Preserve repo lineage for audits. |",
            "| source_type | Companies | Custom field: source_type | Helps separate official website vs directory provenance. |",
            "| icp_segment | Companies | Custom field: icp_segment | Primary CRM segmentation field for this campaign. |",
            "| notes | Companies | Notes | Keep import notes visible to operators. |",
            "| quality_flags | Companies | Custom field: quality_flags | Semicolon-separated QA flags. |",
            "| needs_manual_review | Companies | Custom field: needs_manual_review | Filter before outreach. |",
            "| duplicate_possible | Companies | Custom field: duplicate_possible | Useful in post-import QA views. |",
            "",
            "## Contacts / People",
            "",
            "| CSV field | Twenty object | Twenty field | Notes |",
            "|---|---|---|---|",
            "| organization_name | People | Company relation | Match to the imported company by organization name. |",
            "| contact_name | People | Name | `Unknown` values should be reviewed before production outreach. |",
            "| role_title | People | Job title | Preserve the original institutional role. |",
            "| department_area | People | Custom field: department_area | Normalized department tag for campaign routing. |",
            "| email | People | Primary email | One email per row after conservative split/dedupe. |",
            "| email_type | People | Custom field: email_type | Distinguishes personal vs generic channels. |",
            "| phone | People | Primary phone | May contain more than one public number separated by `|`. |",
            "| island | People | Custom field: island | Useful for routing and reporting. |",
            "| municipality | People | City or Custom field: municipality | Use the same convention as Companies. |",
            "| source_url | People | Custom field: source_url | Traceability back to the public source. |",
            "| source_file | People | Custom field: source_file | Preserve repo lineage for audits. |",
            "| source_type | People | Custom field: source_type | Differentiates official site vs directory provenance. |",
            "| icp_segment | People | Custom field: icp_segment | Campaign segmentation field. |",
            "| notes | People | Notes | Keep QA and merge notes visible to operators. |",
            "| quality_flags | People | Custom field: quality_flags | Semicolon-separated QA flags. |",
            "| high_confidence | People | Custom field: high_confidence | Fast filter for priority review/import. |",
            "| generic_email | People | Custom field: generic_email | Useful to isolate routing-heavy contacts. |",
            "| needs_manual_review | People | Custom field: needs_manual_review | Review queue filter. |",
            "| duplicate_possible | People | Custom field: duplicate_possible | Useful in post-import QA views. |",
            "",
            "## Campos custom recomendados",
            "",
            "- `campaign_name = IA Mujeres 2026`",
            "- `icp_segment`",
            "- `department_area`",
            "- `source_type`",
            "- `source_url`",
            "- `high_confidence`",
            "- `needs_manual_review`",
            "- `generic_email`",
        ]
    ) + "\n"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, UNKNOWN) for field in fieldnames})


def write_json(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump([{field: row.get(field, UNKNOWN) for field in fieldnames} for row in rows], handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    contacts = dedupe_contacts(build_contact_rows())
    organizations = organization_rows(contacts)
    combined = import_ready_rows(organizations, contacts)

    write_csv(OUT_DIR / "organizations_clean.csv", ORGANIZATION_FIELDS, organizations)
    write_json(OUT_DIR / "organizations_clean.json", organizations, ORGANIZATION_FIELDS)
    write_csv(OUT_DIR / "contacts_clean.csv", CONTACT_FIELDS, contacts)
    write_json(OUT_DIR / "contacts_clean.json", contacts, CONTACT_FIELDS)
    write_csv(OUT_DIR / "import_ready_combined.csv", COMBINED_FIELDS, combined)

    (OUT_DIR / f"{DATE}_dataset_inventory.md").write_text(inventory_markdown(), encoding="utf-8")
    (OUT_DIR / f"{DATE}_data_quality_report.md").write_text(quality_report(organizations, contacts, combined), encoding="utf-8")
    (OUT_DIR / f"{DATE}_twenty_import_mapping.md").write_text(twenty_mapping(), encoding="utf-8")


if __name__ == "__main__":
    main()
