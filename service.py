import random
from urllib.parse import urlparse
from config import ALLOWED_CHARACTERS, SHORT_URL_LENGTH
import database


def normalize_and_validate_url(raw_url: str) -> str:
  if not raw_url or not isinstance(raw_url, str):
    raise ValueError("URL daxil edilməyib.")

  url = raw_url.strip()
  if not url:
    raise ValueError("URL boş ola bilməz.")

  if not url.startswith(("http://", "https://")):
    url = "https://" + url

  parsed = urlparse(url)
  if not parsed.netloc or "." not in parsed.netloc:
    raise ValueError("Düzgün URL formatı daxil edin (məs: https://google.com).")

  return url


def _generate_unique_code() -> str:
  while True:
    code = "".join(random.choices(ALLOWED_CHARACTERS, k=SHORT_URL_LENGTH))
    if not database.get_by_short_code(code):
      return code


def create_short_url(raw_url: str, base_url: str) -> dict:
  original_url = normalize_and_validate_url(raw_url)

  existing = database.get_by_original_url(original_url)
  if existing:
    short_code = existing["short_code"]
  else:
    short_code = _generate_unique_code()
    database.save_url(short_code, original_url)

  return {
      "short_code": short_code,
      "short_url": f"{base_url.rstrip('/')}/{short_code}",
      "original_url": original_url,
  }


def resolve_short_url(short_code: str):
  record = database.get_by_short_code(short_code)
  if not record:
    return None

  database.increment_clicks(short_code)
  return record["original_url"]