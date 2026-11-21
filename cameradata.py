"""Camera and deck models for the camera repair page, one list per manufacturer.

Where the lists come from:
  * Sony, JVC, Canon, RED, PTZ and tape formats: Tek Media Group's own pages
    (the earlier camera page and the model lists on the old tekmg.com site).
  * Fact check, Nov 2026: removed PDW-500, PZW-2000 and PZW-3000 (no Sony models by those
    numbers were found; PMW-500 and PZW-4000 are the real ones), renamed the RED entries
    to RED's own names (SCARLET DRAGON), and regrouped the Sony cameras by product line.
    Left out AJ-SD93, AJ-D455 and BR-S822U: not confirmed in the sources checked.
  * Entries marked filled=True (Panasonic, Hitachi, ARRI, Blackmagic, Panasonic and
    JVC decks): common professional models added so every manufacturer has a list.
    Replace these with the shop's own lists when they are supplied.

Each entry:
  name    manufacturer name, also used in front of the model on the service ticket
  slug    used in element ids
  label   heading shown above the dropdown
  groups  list of (group label, [models]); an empty group label means no sub-heading
"""

TICKET_URL = "https://techmediagroup.repairshopr.com/check_ins"

CAMERA_BRANDS = [
    {"name": "Sony", "slug": "sony", "label": "Sony Cameras", "groups": [
        ("XDCAM shoulder-mount (ENG)", [
            "PMW-320", "PMW-400K", "PMW-500", "PXW-X320", "PXW-X400", "PXW-X500", "PXW-Z750",
            "PDW-510", "PDW-530", "PDW-680", "PDW-700", "PDW-F330", "PDW-F355"]),
        ("XDCAM handheld and compact", [
            "PMW-EX1", "PMW-EX1R", "PMW-EX3", "PMW-100", "PMW-150", "PMW-160", "PMW-200", "PMW-300K1",
            "PXW-X70", "PXW-X160", "PXW-X180", "PXW-X200", "PXW-Z90V", "PXW-Z100", "PXW-Z150",
            "PXW-Z190", "PXW-Z200", "PXW-Z300"]),
        ("Cinema and CineAlta cameras", [
            "PMW-F3", "PMW-F5", "PMW-F55", "PXW-FS5", "PXW-FS7", "PXW-FS7M2", "PXW-FX9", "ILME-FX6",
            "HDW-F900R", "SRW-9000"]),
        ("NXCAM, AVCHD and HDV camcorders", [
            "HXR-NX3", "HXR-NX3D1", "HXR-NX5", "HXR-NX70", "HXR-NX100", "HXR-NX800", "HXR-MC50",
            "HXR-MC1500", "HXR-MC2000", "HVR-A1", "HVR-HD1000", "HVR-Z5"]),
        ("Studio cameras", ["HXC-FB80"]),
    ]},
    {"name": "Panasonic", "slug": "panasonic", "label": "Panasonic Cameras", "filled": True, "groups": [
        ("", [
            "AG-HVX200", "AG-HPX170", "AG-HPX250", "AG-HPX370", "AG-HPX500", "AG-HMC150", "AG-AC160",
            "AG-DVX200", "AG-UX180", "AG-CX350", "AJ-PX270", "AJ-PX380", "AJ-PX800", "AJ-PX5000",
            "AJ-HPX2000", "AJ-HPX3100", "AJ-HDX900", "AU-EVA1", "VariCam LT", "VariCam 35",
            "AK-HC5000", "AK-UC4000"]),
    ]},
    {"name": "JVC", "slug": "jvc", "label": "JVC Cameras", "groups": [
        ("", [
            "GY-HM100U", "GY-HM170U", "GY-HM200U", "GY-HM600U", "GY-HM620U", "GY-HM650U", "GY-HM660U",
            "GY-HM700U", "GY-HM850U", "GY-HM890U", "GY-HMQ10U", "GY-HMZ1U", "GY-LS300",
            "GY-HD100U", "GY-HD110U", "GY-HD200U", "GY-HD250U",
            "GY-DV300U", "GY-DV500U", "GY-DV550U", "GY-DV700WU", "GY-DV5100U", "GZ-HD3U"]),
    ]},
    {"name": "Canon", "slug": "canon", "label": "Canon Cameras", "groups": [
        ("Camcorders and cinema cameras", ["XF105", "EOS C100", "EOS C100 Mark II", "EOS C500"]),
        ("EOS DSLR", [
            "EOS-1D X Mark II", "EOS 5D", "EOS 5D Mark II", "EOS 5DS", "EOS 5DS R", "EOS 6D", "EOS 7D",
            "EOS 7D Mark II", "EOS 30D", "EOS 70D", "EOS 80D", "EOS Rebel T6", "EOS Rebel T6i",
            "EOS Rebel T6s"]),
        ("EOS M and PowerShot", ["EOS M3", "EOS M10", "PowerShot SX710 HS"]),
    ]},
    {"name": "Hitachi", "slug": "hitachi", "label": "Hitachi Cameras", "filled": True, "groups": [
        ("", ["Z-HD5000", "Z-HD5500", "Z-HD6000", "SK-HD1000", "SK-HD1200", "SK-HD1300", "SK-UHD4000"]),
    ]},
    {"name": "ARRI", "slug": "arri", "label": "ARRI Cameras", "placeholder": "Choose an ARRI model...", "filled": True, "groups": [
        ("", ["ALEXA Classic", "ALEXA XT", "ALEXA SXT", "ALEXA Mini", "ALEXA Mini LF", "ALEXA LF",
              "ALEXA 35", "AMIRA"]),
    ]},
    {"name": "RED", "slug": "red", "label": "RED Cameras", "groups": [
        ("MYSTERIUM and MYSTERIUM-X", [
            "RED ONE MYSTERIUM", "RED ONE MYSTERIUM-X", "EPIC-M MYSTERIUM-X", "EPIC-X MYSTERIUM-X",
            "SCARLET-X (MYSTERIUM-X)"]),
        ("DSMC DRAGON", ["EPIC-M DRAGON", "EPIC-X DRAGON", "SCARLET DRAGON"]),
        ("DSMC2 and KOMODO", ["DSMC2", "KOMODO 6K"]),
    ]},
    {"name": "Blackmagic", "slug": "blackmagic", "label": "Blackmagic Cameras", "filled": True, "groups": [
        ("", ["URSA Mini 4.6K", "URSA Mini Pro 4.6K G2", "URSA Mini Pro 12K", "URSA Broadcast G2",
              "Pocket Cinema Camera 4K", "Pocket Cinema Camera 6K", "Pocket Cinema Camera 6K Pro",
              "Studio Camera 4K Pro"]),
    ]},
    # no manufacturer in front of these on the ticket: the option already names it
    {"name": "", "slug": "other", "label": "PTZ, DSLR & Industrial", "placeholder": "Choose a type...", "groups": [
        ("PTZ and robotic cameras", [
            "Sony BRC-Z330", "Sony BRC-Z700", "Panasonic AW-HE40", "Panasonic AW-UE70",
            "Bosch MIC-9502-Z30WVF", "PTZ robotic camera"]),
        ("DSLR and mirrorless", ["DSLR camera", "Mirrorless camera"]),
        ("Industrial", ["Industrial IP / SDI camera", "CCU transmission"]),
    ]},
]

DECK_BRANDS = [
    {"name": "Sony", "slug": "sony", "label": "Sony Decks & Recorders", "groups": [
        ("HDCAM SR (SRW)", ["SRW-5000", "SRW-5100", "SRW-5500", "SRW-5800"]),
        ("HDCAM (HDW)", [
            "HDW-500", "HDW-F500", "HDW-250", "HDW-1800", "HDW-D1800", "HDW-2000", "HDW-D2000",
            "HDW-M2000", "HDW-M2100"]),
        ("XDCAM and memory recorders", [
            "PDW-1500", "PDW-HD1500", "PDW-HD1550", "PDW-F75", "PDW-R1", "PDW-U2", "PDW-U4",
            "XDS-PD1000", "XDS-PD2000", "PMW-RX50", "PZW-4000"]),
        ("HDV (HVR)", ["HVR-M15", "HVR-M25", "HVR-M35"]),
    ]},
    {"name": "Panasonic", "slug": "panasonic", "label": "Panasonic Decks & Recorders", "filled": True, "groups": [
        ("", ["AJ-HD1400", "AJ-HD1700", "AJ-HD1800", "AG-DV2500", "AG-HPD24", "AJ-HPM200", "AJ-HPD2500",
              "AJ-PD500", "AG-HMR10"]),
    ]},
    {"name": "JVC", "slug": "jvc", "label": "JVC Decks & Recorders", "filled": True, "groups": [
        ("", ["BR-HD50U", "BR-DV3000U", "BR-DV6000U", "SR-VS30U", "SR-HD1500US", "SR-HD2500US"]),
    ]},
    {"name": "", "slug": "formats", "label": "Tape Formats", "placeholder": "Choose a format...", "groups": [
        ("", ["DAT recorder", "U-matic deck", "Betamax deck", "SuperBetamax / Hi-Band deck"]),
    ]},
]


def _names(brands):
    return [b["name"] for b in brands if b["name"]]


def models_of(brand):
    """Flat list of a brand's models, in the order shown."""
    return [m for _, models in brand["groups"] for m in models]


CAMERA_BRAND_NAMES = _names(CAMERA_BRANDS)
DECK_BRAND_NAMES = _names(DECK_BRANDS)
CAMERA_MODEL_COUNT = sum(len(models_of(b)) for b in CAMERA_BRANDS)
DECK_MODEL_COUNT = sum(len(models_of(b)) for b in DECK_BRANDS)
