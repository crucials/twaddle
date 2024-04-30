# spoken-words-counter

transcribes speech from mic and calculates stats like total spoken words count and all frequencies for all words

https://github.com/crucials/spoken-words-counter/assets/83793845/8fd060ca-c27a-4667-9792-ba437b26aab0

## installation

this is a desktop app and it uses your pc resources to convert speech to text:
- transcription with cpu needs around 2.5gb of ram
- transcription with gpu needs around 1.5gb of video ram, cant be used yet

:penguin: [linux executable](https://github.com/crucials/spoken-words-counter/releases/download/v1.0.0-beta/spoken-words-counter-linux)

### manual

requires python and pip 

- download the project on the local machine

  ```bash
  git clone https://github.com/crucials/spoken-words-counter.git
  ```

- move to project's folder, install a shitpile of libraries

  ```bash
  pip install -r requirements.txt
  ```

- launch the ui

  ```bash
  python ./src/start_ui.py
  ```

## other info

built with python eel, vue and faster-whisper as a transcription model
