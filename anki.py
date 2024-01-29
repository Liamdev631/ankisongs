from langchain.pydantic_v1 import BaseModel, Field
import genanki
import random


class CardTemplate(BaseModel):
    """A template for an Anki card."""
    line: str = Field(..., description="The line of the song in a non-English language.")
    translation: str = Field(..., description="The translation of the line in English.")

class DeckTemplate(BaseModel):
    cards: list[CardTemplate] = Field(..., description="The cards in the deck, which comprise the entire song.")

# Define an anki model for whole-line translation
# Each card will have a song line and a translation
UID_MODEL = 1640018922
card_model = genanki.Model(UID_MODEL, name="LineModel",
    fields=[
        {"name": "Line"},
        {"name": "Translation"}
        ],
    templates=[{
        "name": "LineTemplate",
        "qfmt": "{{Line}}",
        "afmt": "{{FrontSide}}<hr id=answer>{{Translation}}",
        }])

def make_card_from_template(template: CardTemplate) -> genanki.Note:
    """Make an Anki card from a template."""
    return genanki.Note(
        model=card_model,
        fields=[template.line, template.translation],
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

