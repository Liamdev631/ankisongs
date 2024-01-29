import streamlit as st
from lyrics import clean_lyrics
from card_gen import generate_deck_from_lyrics
import genanki

st.set_page_config("AnkiTunes", layout="wide")

col_lyrics, col_cards = st.columns(2)

# Draw the artist column, where the user can search for and select an artist
with col_lyrics:
    st.header("Lyrics 📜")

    st.text_area("Lyrics", height=500, key="lyrics")

with col_cards:
    st.header("Cards 📇")
    st.text_input("Deck Name", key="deck_name")
    
    # Generate a deck
    if st.button("Generate Deck"):
        deck_name = st.session_state["deck_name"]
        lyrics = st.session_state["lyrics"]

        # Generate the deck with the LLM
        deck = generate_deck_from_lyrics(lyrics, deck_name)

        # Display a list of all the cards
        for note in deck.notes:
            st.write("Front:", note.fields[0])
            st.write("Back: ", note.fields[1])
            st.write("")

        # Download the deck
        genanki.Package(deck).write_to_file('output.apkg')
        st.download_button("Download Deck", data=deck.to_json(), file_name=f"{deck_name}.json", mime="application/json")

