from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os

for tz in ["UTC", "Asia/Tokyo", "UTC"]:
    print(f"-- {tz}")
    os.environ["TZ"] = tz

    now_none:datetime = datetime.now()
    now_utc:datetime = datetime.now(timezone.utc)
    now_jst:datetime = datetime.now(ZoneInfo("Asia/Tokyo"))

    print(f"{now_none.timestamp()} | {now_none}")
    print(f"{now_utc.timestamp()} | {now_utc}")
    print(f"{now_jst.timestamp()} | {now_jst}")
