import redis

class Leaderboard:
    def __init__(self, redis_client, key="guess_game_leaderboard"):
        self.redis = redis_client
        self.key = key

    def add_score(self, username, score):
        self.redis.zadd(self.key, {username: score})

    def get_top_n(self, n=10):
        return self.redis.zrevrange(self.key, 0, n - 1, withscores=True)

    def get_user_rank(self, username):
        rank = self.redis.zrevrank(self.key, username)
        if rank is not None:
            return rank + 1
        return None

    def get_user_score(self, username):
        return self.redis.zscore(self.key, username)
