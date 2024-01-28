from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from anki import DeckTemplate, make_deck_from_template
from lyrics import clean_lyrics
import genanki

SYSTEM_PROMPT = """
You are an AI that generates ANKI cards from song lyrics. Given a list of song lyrics,
you will generate a translation for each line in the format of an ANKI card.

{deck_format_instructions}
"""

def generate_deck_from_lyrics(lyrics: str) -> genanki.Deck:
    lyrics = clean_lyrics(lyrics)

    # Initialize the llm and chain
    llm = ChatOpenAI(openai_api_key="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", model="gpt-4-1106-preview", temperature=0)

    prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("\n{lyrics}")
    ]
)

    output_parser = PydanticOutputParser(pydantic_object=DeckTemplate)

    chain = LLMChain(llm=llm, prompt=prompt, output_parser=output_parser, verbose=True)

    # ToDo: Put this in a loop until a card has been generated for eah line in the lyrics
    deck_template: DeckTemplate = chain.run({"lyrics": lyrics, "deck_format_instructions": output_parser.get_format_instructions()})

    deck: genanki.Deck = make_deck_from_template(deck_template)

    return deck
