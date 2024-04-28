cd ./src/ui/web
npm run build
cd ../../../
python -m eel ./src/start_ui.py ./src/ui/web -y --onefile --noconsole --log-level=DEBUG --add-data="./src/ui/bin/ungoogled-chromium.AppImage:./ui/bin" -n spoken-words-counter
