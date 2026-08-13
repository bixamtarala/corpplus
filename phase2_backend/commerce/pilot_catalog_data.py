"""Review-only pilot catalog candidates with no stock or supplier claims."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DraftCategory:
    slug: str
    name: str
    translations: dict[str, str]
    sort_order: int


@dataclass(frozen=True)
class DraftProduct:
    slug: str
    name: str
    translations: dict[str, str]
    category_slug: str
    sku_code: str
    pack_quantity: Decimal
    unit_of_measure: str
    indicative_price_paise: int


DRAFT_CATEGORIES = (
    DraftCategory(
        slug="vegetables",
        name="Vegetables",
        translations={"hi": "सब्जियां", "te": "కూరగాయలు"},
        sort_order=10,
    ),
    DraftCategory(
        slug="fruits",
        name="Fruits",
        translations={"hi": "फल", "te": "పండ్లు"},
        sort_order=20,
    ),
    DraftCategory(
        slug="leafy-greens",
        name="Leafy greens",
        translations={"hi": "पत्तेदार सब्जियां", "te": "ఆకుకూరలు"},
        sort_order=30,
    ),
    DraftCategory(
        slug="rice-and-millets",
        name="Rice and millets",
        translations={"hi": "चावल और मोटा अनाज", "te": "బియ్యం మరియు చిరుధాన్యాలు"},
        sort_order=40,
    ),
    DraftCategory(
        slug="pulses",
        name="Pulses",
        translations={"hi": "दालें", "te": "పప్పుధాన్యాలు"},
        sort_order=50,
    ),
    DraftCategory(
        slug="spices",
        name="Spices",
        translations={"hi": "मसाले", "te": "మసాలా దినుసులు"},
        sort_order=60,
    ),
)


DRAFT_PRODUCTS = (
    DraftProduct(
        slug="tomato-1kg",
        name="Tomato",
        translations={"hi": "टमाटर", "te": "టమాటా"},
        category_slug="vegetables",
        sku_code="PILOT-TOMATO-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=4200,
    ),
    DraftProduct(
        slug="onion-1kg",
        name="Onion",
        translations={"hi": "प्याज", "te": "ఉల్లిపాయ"},
        category_slug="vegetables",
        sku_code="PILOT-ONION-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=3600,
    ),
    DraftProduct(
        slug="potato-1kg",
        name="Potato",
        translations={"hi": "आलू", "te": "బంగాళాదుంప"},
        category_slug="vegetables",
        sku_code="PILOT-POTATO-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=3200,
    ),
    DraftProduct(
        slug="banana-robusta-1kg",
        name="Banana",
        translations={"hi": "केला", "te": "అరటిపండు"},
        category_slug="fruits",
        sku_code="PILOT-BANANA-ROBUSTA-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=5800,
    ),
    DraftProduct(
        slug="papaya-1-piece",
        name="Papaya",
        translations={"hi": "पपीता", "te": "బొప్పాయి"},
        category_slug="fruits",
        sku_code="PILOT-PAPAYA-1PC",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="piece",
        indicative_price_paise=6500,
    ),
    DraftProduct(
        slug="spinach-1-bunch",
        name="Spinach",
        translations={"hi": "पालक", "te": "పాలకూర"},
        category_slug="leafy-greens",
        sku_code="PILOT-SPINACH-1BUNCH",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="bunch",
        indicative_price_paise=2500,
    ),
    DraftProduct(
        slug="coriander-leaves-1-bunch",
        name="Coriander leaves",
        translations={"hi": "धनिया पत्ती", "te": "కొత్తిమీర"},
        category_slug="leafy-greens",
        sku_code="PILOT-CORIANDER-1BUNCH",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="bunch",
        indicative_price_paise=1800,
    ),
    DraftProduct(
        slug="sona-masoori-rice-5kg",
        name="Sona Masoori rice",
        translations={"hi": "सोना मसूरी चावल", "te": "సోనా మసూరి బియ్యం"},
        category_slug="rice-and-millets",
        sku_code="PILOT-SONA-MASOORI-5KG",
        pack_quantity=Decimal("5.000"),
        unit_of_measure="kg",
        indicative_price_paise=34500,
    ),
    DraftProduct(
        slug="ragi-1kg",
        name="Ragi",
        translations={"hi": "रागी", "te": "రాగులు"},
        category_slug="rice-and-millets",
        sku_code="PILOT-RAGI-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=7200,
    ),
    DraftProduct(
        slug="toor-dal-1kg",
        name="Toor dal",
        translations={"hi": "अरहर दाल", "te": "కందిపప్పు"},
        category_slug="pulses",
        sku_code="PILOT-TOOR-DAL-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=16800,
    ),
    DraftProduct(
        slug="chana-dal-1kg",
        name="Chana dal",
        translations={"hi": "चना दाल", "te": "శనగపప్పు"},
        category_slug="pulses",
        sku_code="PILOT-CHANA-DAL-1KG",
        pack_quantity=Decimal("1.000"),
        unit_of_measure="kg",
        indicative_price_paise=9800,
    ),
    DraftProduct(
        slug="turmeric-powder-200g",
        name="Turmeric powder",
        translations={"hi": "हल्दी पाउडर", "te": "పసుపు పొడి"},
        category_slug="spices",
        sku_code="PILOT-TURMERIC-200G",
        pack_quantity=Decimal("200.000"),
        unit_of_measure="g",
        indicative_price_paise=6400,
    ),
)
