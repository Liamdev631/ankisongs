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
you will generate a translation for each line in the format of an ANKI card. Please ignore 
any lines that are in English. Only include English lines if they are embedded between
two non-English words. Do not include erroneous lines that are not part of the song lyrics,
such as the artist name, song title, or other metadata, references to verses or choruses,
or any trace of the site you are using to get the lyrics. For example,

Example Input Lyrics:
不小心暴露 没能够一帆风顺 (暴露, Ayy)
一千个联系人九百个辣妹 (Ayy)
我现在还单身就白出来混
You might also like
Isabellae
Higher Brothers
Made in China
Higher Brothers
HISS
Megan Thee Stallion
[Verse 2: Psy.P]
妹都爱跟我聊骚因为I'ma天蝎座 (Uh)
这都才三点过五分我准备先写歌 (Uh)
不断有消息来打扰
我跑得脱马脑壳好多妹都约过 (Uh)
收了个演出费电话都懒得回
最近批事情很多
有好多的批事情 (批事情)
说之前先问哈你自己 (你自己)
[...]

Desired Output:
不小心暴露 没能够一帆风顺
一千个联系人九百个辣妹
我现在还单身就白出来混
妹都爱跟我聊骚因为I'ma天蝎座
这都才三点过五分我准备先写歌
不断有消息来打扰
我跑得脱马脑壳好多妹都约过
收了个演出费电话都懒得回
最近批事情很多
有好多的批事情
说之前先问哈你自己
[...]

{deck_format_instructions}
"""

def generate_deck_from_lyrics(lyrics: str, deck_name) -> genanki.Deck:
    lyrics = clean_lyrics(lyrics)

    # Initialize the llm and chain
    llm = ChatOpenAI(
        openai_api_key="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",
        #model="gpt-4-turbo-preview",
        model="gpt-3.5-turbo-1106",
        temperature=0)

    # Structure the prompt
    prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("\n{lyrics}")
    ])

    # Define the model of the output. Queries for the deck formatting.
    output_parser = PydanticOutputParser(pydantic_object=DeckTemplate)

    # Throw everything together
    chain = LLMChain(llm=llm, prompt=prompt, output_parser=output_parser, verbose=True)

    # Generate the cards from the lyrics
    deck_template: DeckTemplate = chain.run({"lyrics": lyrics, "deck_format_instructions": output_parser.get_format_instructions()})

    # Build deck for the Anki app
    deck = make_deck_from_template(deck_template, deck_name=deck_name)

    return deck
