cd ./src/ui/electron
npm run build
npx electron-builder
cd ../../../
pyinstaller ./src/start_ui.py --add-data="./src/ui/electron/dist/spoken-words-counter.AppImage:./ui/electron/dist" -y --onefile --noconsole --log-level=DEBUG -n spoken-words-counter
