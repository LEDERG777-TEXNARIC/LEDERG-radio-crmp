# LEDERG CR:MP — Radio stations

This repository is the source of the custom LEDERG radio playlists. The launcher synchronizes it into the game client automatically.

## Add a station

1. Create a folder in the repository root. **The folder name becomes the station name shown in the game.**
2. Put music files directly inside that folder. Supported formats for the synchronizer: `.mp3`, `.ogg`, `.wav`, `.flac`, `.m4a`, `.opus`.
3. Commit and push to `main`. The launcher syncs the station before launching the game; the station appears when it contains at least one supported audio file.
4. Add or replace songs to update its playlist. The radio plugin reads tracks from the station folder.

## Delete a station

Delete the whole station folder (or remove every audio track from it) and push to `main`. The next synchronization removes the radio's previously managed songs from the client. Other unrelated user files are not deleted.

## Notes

- Put audio files directly inside a station folder, not in nested subfolders.
- Keep station folder names short; they are displayed in the game UI.
- The repository stores tracks and station names only; the game plug-in/runtime is managed separately.
- GitHub limits individual ordinary repository files to 100 MB. Prefer compressed audio or split long sets into several tracks.
- Only upload audio you have permission to distribute.
