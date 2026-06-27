#!/usr/bin/env python3
"""
Автомая публикация поста в ВКонтакте для рассылки по эфирным маслам.
Читает расписание из data/schedule.md, шаблон из data/template.md,
и опционально источники из data/sources.md.
Публикует пост через VK API (wall.post).
Логирует результат в logs/.
"""

import os
import sys
import datetime
import re
import logging
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------- Конфигурация ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
TEMPLATE_PATH = DATA_DIR / "template.md"
SCHEDULE_PATH = DATA_DIR / "schedule.md"
SOURCES_PATH = DATA_DIR / "sources.md"
ENV_PATH = BASE_DIR / ".env"

LOGS_DIR.mkdir(exist_ok=True)

load_dotenv(dotenv_path=ENV_PATH)

VK_TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")  # id сообщества без знака minus, будет использовано как -GROUP_ID
API_VERSION = "5.199"

if not VK_TOKEN or not GROUP_ID:
    sys.exit("Ошибка: VK_TOKEN и GROUP_ID должны быть заданы в .env файле")

# ---------- Логирование ----------
log_file = LOGS_DIR / f"vk_post_{datetime.date.today().isoformat()}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ---------- Вспомогательные функции ----------
def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def load_sources() -> str:
    if SOURCES_PATH.exists():
        return SOURCES_PATH.read_text(encoding="utf-8")
    return "- Источник 1\n- Источник 2"  # fallback

def parse_schedule(today: datetime.date):
    """Возвращает (description, is_sales) если сегодня есть запись, иначе (None, None)."""
    if not SCHEDULE_PATH.exists():
        logger.warning("Файл расписания не найден")
        return None, None
    content = SCHEDULE_PATH.read_text(encoding="utf-8")
    # ищем строки вида "- Понедельник, 02.07.2025 – Информационный пост: ..."
    pattern = r"-\s*([^,]+),\s*(\d{2}\.\d{2}\.\d{4})\s*[–-]\s*(.+)"
    for line in content.splitlines():
        m = re.match(pattern, line.strip())
        if not m:
            continue
        _, date_str, description = m.groups()
        try:
            day = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            continue
        if day == today:
            is_sales = "продаж" in description.lower() or "скидк" in description.lower() or "предложени" in description.lower()
            return description.strip(), is_sales
    return None, None

def build_post(description: str, is_sales: bool, template: str, sources: str) -> str:
    # Определяем заголовок и вводную часть из описания
    # Пример описания: "Понедельник, 02.07.2025 – Информационный пост: Лаванда для сна"
    # Мы просто берём часть после двоеточия как тему.
    if ":" in description:
        _, topic = description.split(":", 1)
        topic = topic.strip()
    else:
        topic = description.strip()
    # Придумываем заголовок
    if is_sales:
        title = f"Спецпредложение: {topic}"
        intro = f"Сегодня speciale предложение по теме '{topic}'. Не упустите шанс!"
        cta = "Переходите в магазин по ссылке в закреплённом посте и приобретайте со скидкой!"
    else:
        title = f"Полезно знать: {topic}"
        intro = f"Интересный факт о {topic.lower()}, который может улучшить ваше самочувствие."
        cta = "Поделитесь этим постом с друзьями, кому будет полезно!"
    facts = "- Факт 1\n- Факт 2"  # заглушка; можно парсить из sources
    usage = "- Способ 1\n- Способ 2"
    # Заполняем шаблон
    post = template.format(
        title=title,
        intro=intro,
        facts=facts,
        usage=usage,
        sources=sources,
        call_to_action=cta,
    )
    return post

def post_to_vk(message: str) -> dict:
    url = "https://api.vk.com/method/wall.post"
    params = {
        "owner_id": f"-{GROUP_ID}",
        "message": message,
        "access_token": VK_TOKEN,
        "v": API_VERSION,
    }
    resp = requests.post(url, params=params)
    data = resp.json()
    if "error" in data:
        logger.error(f"Ошибка VK API: {data['error']}")
    else:
        logger.info(f"Пост опубликован, id={data.get('response',{}).get('post_id')}")
    return data

def main():
    today = datetime.date.today()
    logger.info(f"Запуск скрипта для даты {today.isoformat()}")

    description, is_sales = parse_schedule(today)
    if description is None:
        logger.info("На сегодня запланированных публикаций нет.")
        return

    template = load_template()
    sources = load_sources()
    post_text = build_post(description, is_sales, template, sources)
    logger.debug(f"Текст поста:\n{post_text}")

    result = post_to_vk(post_text)
    # Если пост успешно опубликован, можно добавить запись в Google Sheet (заглушка)
    if "response" in result:
        post_id = result["response"].get("post_id")
        # TODO: integrate gspread update
        logger.info(f"Готово. post_id={post_id}")

if __name__ == "__main__":
    main()