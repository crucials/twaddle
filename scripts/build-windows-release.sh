printf "\n (!) this script was made only for windows systems \n"
cd ./src/ui/electron
npm run build
npx electron-builder
cd ../../../
pyinstaller ./src/start_ui.py --add-data="./src/ui/electron/bin/twaddle.exe:./ui/electron/bin" -y --noconsole --log-level=DEBUG -n twaddle
