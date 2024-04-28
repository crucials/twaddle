cd ./src/ui/web
npm run build
cd ../../../
python -m eel ./src/start_ui.py ./src/ui/web -y --onefile --noconsole --log-level=DEBUG --add-data="./src/ui/bin/ungoogled-chromium_120.0.6099.109-1.1.AppImage:./ui/bin" -n spoken-words-counter
