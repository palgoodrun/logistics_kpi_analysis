# ==================================================
# import
# ==================================================
import logging
from pathlib import Path
from typing import TypedDict


# ==================================================
# class
# ==================================================
class LogConfig(TypedDict, total=False):
    level: str
    file_path: str


# ==================================================
# setup_logging
# ==================================================
def setup_logging(log_config: LogConfig) -> logging.Logger:

    # --------------------------
    # root logger取得
    # --------------------------
    logger = logging.getLogger()

    # --------------------------
    # ログレベル
    # --------------------------
    level = getattr(
        logging,
        log_config.get("level", "INFO"),
    )
    logger.setLevel(level)

    # --------------------------
    # ログフォーマット
    # --------------------------
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # --------------------------
    # コンソール出力
    # --------------------------
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # --------------------------
    # Handler重複防止
    # --------------------------
    if not logger.handlers:
        logger.addHandler(console)

    return logger
