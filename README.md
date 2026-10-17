# LEDERG CR:MP — Radio stations

This repository is the source of custom LEDERG radio playlists. The launcher synchronizes it into the game client before launch.

## Add a station

1. Create a folder in the repository root. **Its folder name becomes the station name shown in game.**
2. Put music files directly inside the folder. Supported formats: `.mp3`, `.ogg`, `.wav`.
3. Commit and push to `main`. The launcher downloads new/changed tracks before launching the game.
4. Replace a song or add another track and push to update the playlist.

## Delete a station

Delete the station folder, or remove all supported audio files from it, and push to `main`. The next sync deletes only previously LEDERG-managed tracks that no longer exist in the repository. Untracked local files are preserved.

## Current station folders

- `LEDERG FM`
- `LEDERG RAP`
- `LEDERG RUSSIAN`
- `LEDERG ROCK`
- `LEDERG CHILL`
- `LEDERG ELECTRONIC`

Empty folders with only a README are placeholders; a station becomes active only when it has at least one supported audio track.

## Notes

- Put tracks directly inside a station folder (not in nested folders).
- Keep folder names short; the in-game radio wheel displays them.
- Individual GitHub repository files have a 100 MB limit. Use compressed audio and split long recordings.
- Only upload music you have permission to distribute.
