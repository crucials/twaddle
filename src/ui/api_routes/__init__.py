from ui.api_routes.recording_devices import recording_devices_blueprint
from ui.api_routes.word_lists import word_lists_blueprint
from ui.api_routes.realtime_counter import realtime_counter_blueprint


routes = [recording_devices_blueprint,
          word_lists_blueprint,
          realtime_counter_blueprint]
