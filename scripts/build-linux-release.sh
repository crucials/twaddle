printf "\n (!) this script works only on linux systems \n"
cd ./src/ui/electron
npm run build
npx electron-builder
cd ../../../
pyinstaller ./src/start_ui.py --add-data="./src/ui/electron/bin/spoken-words-counter.AppImage:./ui/electron/bin" -y --noconsole --log-level=DEBUG -n spoken-words-counter
