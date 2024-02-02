import sys

from card_gen import generate_deck_from_lyrics

if len(sys.argv) < 2:
    print("Usage: ankisongs.py <lyrics file>")
    sys.exit(1)

song_file_names = sys.argv[1:]
for song_file_name in song_file_names:
    with open(song_file_name, "r") as song_file:
        song_name = song_file_name.rstrip(".txt")
        print(f"Generating deck for {song_name}...")
        lyrics = song_file.read()
        deck = generate_deck_from_lyrics(lyrics, song_file_name)
        deck.write_to_file(f"{song_name}.apkg")
        print(f"Deck for {song_file_name} written to {song_name}.apkg")
