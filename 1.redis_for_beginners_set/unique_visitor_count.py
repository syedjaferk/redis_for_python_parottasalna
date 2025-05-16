import redis
from datetime import datetime
import sys

r = redis.Redis(host="localhost", port=6379, db=0)

def get_key(date=None):
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    return f"visitors:{date}"

def track_visit(user_id):
    key = get_key()
    r.sadd(key, user_id)
    print(f"✔️ User '{user_id}' visit recorded for {key}")

def get_today_count():
    count = r.scard(get_key())
    print(f"👥 Unique visitors today: {count}")

def get_count_by_date(date):
    key = get_key(date)
    count = r.scard(key)
    print(f"📅 Unique visitors on {date}: {count}")

def get_common_users(date1, date2):
    users = r.sinter(get_key(date1), get_key(date2))
    decoded = [u.decode() for u in users]
    print(f"👥 Users who visited on both {date1} and {date2}: {decoded}")

def get_union_users(dates):
    keys = [get_key(d) for d in dates]
    users = r.sunion(*keys)
    decoded = [u.decode() for u in users]
    print(f"🧮 Total unique users across {dates}: {decoded}")

def get_diff_users(date1, date2):
    users = r.sdiff(get_key(date1), get_key(date2))
    decoded = [u.decode() for u in users]
    print(f"🧨 Users on {date1} but not on {date2}: {decoded}")

def show_help():
    print("""
Usage:
  visit <user_id>                  Record a visit by user_id
  today                            Show today's unique visitor count
  count <date>                     Show count for a specific date (YYYY-MM-DD)
  intersect <date1> <date2>        Users who visited on both dates
  union <date1> <date2> ...        Union of visitors across dates
  diff <date1> <date2>             Users on date1 but not on date2
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "visit" and len(sys.argv) == 3:
        track_visit(sys.argv[2])
    elif command == "today":
        get_today_count()
    elif command == "count" and len(sys.argv) == 3:
        get_count_by_date(sys.argv[2])
    elif command == "intersect" and len(sys.argv) == 4:
        get_common_users(sys.argv[2], sys.argv[3])
    elif command == "union" and len(sys.argv) >= 3:
        get_union_users(sys.argv[2:])
    elif command == "diff" and len(sys.argv) == 4:
        get_diff_users(sys.argv[2], sys.argv[3])
    else:
        show_help()
