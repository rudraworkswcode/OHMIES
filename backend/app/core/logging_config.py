import logging
import sys
import os

def setup_logging():
    log_level = logging.INFO if os.getenv("ENVIRONMENT") != "debug" else logging.DEBUG
    
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), "../../../logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(log_dir, "app.log"), encoding="utf-8")
        ]
    )
    
    logger = logging.getLogger("ohmies")
    logger.info("Logging configured cleanly without exposing credentials.")
    return logger

logger = setup_logging()

