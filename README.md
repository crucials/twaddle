![two abstract waves, mediocre logo](https://github.com/crucials/spoken-words-counter/assets/83793845/da0404ed-95c0-4e48-b010-af665913d558)

# spoken-words-counter

transcribes speech from mic and calculates stats like total spoken words count and all frequencies for all words

## installation

this is a desktop app and it uses your gpu resources to convert speech to text (needs around 1.5gb of video ram)

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
