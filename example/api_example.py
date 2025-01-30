from src.core.config.loader import Config
from src.services.moodle.api import MoodleAPI

# Create a Config object
config = Config("config.ini")

# Initialize MoodleAPI with config
api = MoodleAPI(config.moodle.url)

# Login using credentials from config
api.login(config.moodle.username, config.moodle.password)

# Get site information
site_info = api.get_site_info()
print(site_info)
