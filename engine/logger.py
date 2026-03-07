import os
import sys
import logging

def configure_logging():
    """Sets up the logging configuration and creates the logs folder if needed."""
    
    # Calculate path to the logs directory at the root of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "pywebcore.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("PyWebCore.System")
    logger.info("Logging subsystem initialized.")
