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
You are an AI that generates ANKI cards from song lyrics. You will begin the deck with all {language_level} 
or higher words, followed by whole lines of the song in the original language.

Please ignore any lines that are in English. Only include English lines if they are embedded between
two non-English words. Automatically convert all traditional Chinese characters you see with their simplified counterparts.
Do not include erroneous lines that are not part of the song lyrics,
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
不小心暴露
Accidently exposed

一帆风顺
Smooth sailing

联系人
Contact (person)

混
Mix

骚
Coquettish

天蝎座
Scorpio

打扰
Reference to the story 武松打虎

马脑壳
Horse skull

演出费
Performance fee

批事情
Criticise things

不小心暴露 没能够一帆风顺
Accidentally exposed, things didn’t go smoothly

一千个联系人九百个辣妹
One thousand contacts, nine hundred hot girls

我现在还单身就白出来混
I'm still single now, so I'll hang out for free

妹都爱跟我聊骚因为I'ma天蝎座
Girls love to chat with me because I'm a Scorpio

这都才三点过五分我准备先写歌
It's only five past three and I'm going to write a song first

不断有消息来打扰
There are constant messages to disturb you

我跑得脱马脑壳好多妹都约过
I ran away so fast that I lost my mind and dated many girls.

收了个演出费电话都懒得回
I didn't even bother to return the phone call after charging a performance fee.

最近批事情很多
There have been a lot of criticisms recently

有好多的批事情
There are a lot of things to say

说之前先问哈你自己
Before you speak, ask yourself
[...]

{deck_format_instructions}
"""

def generate_deck_from_lyrics(lyrics: str, deck_name, language_level: str = "HSK 5") -> genanki.Deck:
    lyrics = clean_lyrics(lyrics)

    # Initialize the llm and chain
    llm = ChatOpenAI(
        openai_api_key="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",
        model="gpt-4-turbo-preview",
        #model="gpt-3.5-turbo-1106",
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
    deck_template: DeckTemplate = chain.run({
        "lyrics": lyrics,
        "deck_format_instructions": output_parser.get_format_instructions(),
        "language_level": language_level
    })

    # Build deck for the Anki app
    deck = make_deck_from_template(deck_template, deck_name=deck_name)

    return deck
