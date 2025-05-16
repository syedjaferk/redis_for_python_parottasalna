# Use the official Redis image as a base
FROM redis:latest

# Set the Bloom filter name as an environment variable
ENV BLOOM_FILTER_NAME myBloom

# Install dependencies, including Python 3
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-distutils \
    && rm -rf /var/lib/apt/lists/*

# Ensure that python3 is available as 'python'
RUN ln -s /usr/bin/python3 /usr/bin/python

# Clone the RedisBloom repository
RUN git clone --recursive https://github.com/RedisBloom/RedisBloom.git /RedisBloom

# Change to the RedisBloom directory and set up dependencies
WORKDIR /RedisBloom 
RUN ./sbin/setup
RUN bash -l 
RUN make


# Load the RedisBloom module and initialize the Bloom filter with the defined name
RUN echo 'redis.call("BF.RESERVE", KEYS[1], 0.01, 1000)' >> bloom_reserve.lua
CMD ["sh", "-c", "redis-server --loadmodule /RedisBloom/bin/linux-x64-release/redisbloom.so --daemonize yes && redis-cli --eval bloom_reserve.lua 1 $BLOOM_FILTER_NAME && tail -f /dev/null"]
