import logging
from pathlib import Path


class CustomFormatter(logging.Formatter):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"
    
    COLORS = {
        'WARNING': YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }
    
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "Haboosh CS MAJOR Predict %(levelname)s %(message)s"
    )
    formatter = logging.Formatter(format)

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname_color = self.COLOR_SEQ % (30 + self.COLORS[levelname]) + f"[{levelname: ^8}]" + self.RESET_SEQ
            record.levelname = levelname_color
        return self.formatter.format(record)


logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
log_file = Path.cwd() / "cop.log"

if log_file.exists():
    log_file.unlink()

fh = logging.FileHandler(filename=str(log_file))
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)
