import redis
import time

from ast import literal_eval


REDIS_HOST='heatmaptraining_redis_1'
REDIS_PORT=6379

class RedisRequestSender:
    """
    Base class that provides interface for sending API requests
    to web-based hosting services for version control using Git
    """

    def __init__(self):
        RETRIES = 30
        while True:
            try:
                # declare connection
                self.redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
                break
            except redis.exceptions.ConnectionError as exc:
                if RETRIES == 0:
                    print('Failed to connect!')
                    raise exc
                RETRIES -= 1
                time.sleep(1)
        print('Successfully connected Redis!')


    def get_entry(self,body):
        print(self.redis_db.keys())
        assert isinstance(body, dict), 'Inputted "body" type is not dict'
        key='-'.join(body.values())
        try:
            return(literal_eval(self.redis_db.get(key).decode()))
        except:
            print("Problems with Redis get")
            return(None)

    def set_entry(self,body,response):
        assert isinstance(body, dict), 'Inputted "body" type is not dict'
        key='-'.join(body.values())
        try:
            pipe=self.redis_db.pipeline()
            pipe.set(name=key,value=response,ex=3600)
            pipe.execute()
        except:
            print("Problems with Redis set")

