from langchain.pydantic_v1 import BaseModel, Field
import genanki
import random
import pinyin

class CardTemplate(BaseModel):
    """A template for an Anki card."""
    front: str = Field(..., description="The line of the song, or word, in a non-English language.")
    back: str = Field(..., description="The translation of the line, or word, in English.")

class DeckTemplate(BaseModel):
    cards: list[CardTemplate] = Field(..., description="The cards in the deck, which comprise the entire song.")

# Define an anki model for whole-line translation
# Each card will have a song line and a translation
UID_MODEL = 1640018922
card_model = genanki.Model(UID_MODEL, name="LineModel",
    fields=[
        {"name": "Front"},
        {"name": "Back"}
        ],
    templates=[{
        "name": "LineTemplate",
        "qfmt": "{{Front}}",
        "afmt": "{{Front}}<hr id=answer>{{Back}}",
        }])

def make_card_from_template(template: CardTemplate) -> genanki.Note:
    """Make an Anki card from a template."""
    return genanki.Note(
        model=card_model,
        fields=[template.front, "\n".join([pinyin.get(template.front), template.back])],
    )

def make_deck_from_template(template: DeckTemplate, deck_name: str) -> genanki.Deck:
    """Make an Anki deck from a template."""
    UID_DECK = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(UID_DECK, deck_name)

    for card in template.cards:
        deck.add_note(
            make_card_from_template(card)
        )

    return deck

