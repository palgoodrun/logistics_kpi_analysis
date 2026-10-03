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
    # ログフォルダ作成
    # --------------------------
    log_path = Path(log_config.get("file_path", "logs/app.log"))
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------
    # ファイル出力
    # --------------------------
    file = logging.FileHandler(
        log_path,
        mode="a",
        encoding="utf-8",
    )
    file.setFormatter(formatter)

    # --------------------------
    # Handler重複防止
    # --------------------------
    if not logger.handlers:
        logger.addHandler(console)
        logger.addHandler(file)

    return logger
