import redis
from datetime import datetime
import sys

r = redis.Redis(host="localhost", port=6379, db=0)

def get_key(date=None):
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    return f"visitors:{date}"

def track_visit(user_id, ttl_seconds=2592000):  # 30 days TTL
    key = get_key()
    added = r.sadd(key, user_id)
    if added:
        if r.ttl(key) == -1:
            r.expire(key, ttl_seconds)
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

def print_help():
    print("""
Usage:
    python visitor_tracker.py visit <user_id>
    python visitor_tracker.py today
    python visitor_tracker.py count <YYYY-MM-DD>
    python visitor_tracker.py intersect <date1> <date2>
    python visitor_tracker.py union <date1> [<date2> ...]
    python visitor_tracker.py diff <date1> <date2>
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "visit":
        if len(sys.argv) != 3:
            print("Error: 'visit' requires <user_id>")
            sys.exit(1)
        track_visit(sys.argv[2])

    elif cmd == "today":
        get_today_count()

    elif cmd == "count":
        if len(sys.argv) != 3:
            print("Error: 'count' requires <YYYY-MM-DD>")
            sys.exit(1)
        get_count_by_date(sys.argv[2])

    elif cmd == "intersect":
        if len(sys.argv) != 4:
            print("Error: 'intersect' requires <date1> <date2>")
            sys.exit(1)
        get_common_users(sys.argv[2], sys.argv[3])

    elif cmd == "union":
        if len(sys.argv) < 3:
            print("Error: 'union' requires at least one date")
            sys.exit(1)
        get_union_users(sys.argv[2:])

    elif cmd == "diff":
        if len(sys.argv) != 4:
            print("Error: 'diff' requires <date1> <date2>")
            sys.exit(1)
        get_diff_users(sys.argv[2], sys.argv[3])

    else:
        print(f"Unknown command: {cmd}")
        print_help()
