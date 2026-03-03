import redis
import os


redis_client= redis.from_url(os.getenv("REDIS_URL","redis://localhost:6379"))

# redis_client = redis.Redis(  # redis_client redis server se connect ho raha hai
#     host="localhost",  # redis server kaha chal raha hai
#     port=6379,  # default redis port
#     decode_responses=True,  # will give data in string format not in bytes
# )
