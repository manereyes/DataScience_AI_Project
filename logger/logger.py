import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Shows logs
    ]
)

# 1: Info, 2: warning, 3: error, 4: critical
def generate_log(type: int, msg: str) -> str :
    if type == 1:
        return logging.info(msg)