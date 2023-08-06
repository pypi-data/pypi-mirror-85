local redis = require("resty.redis")
local json = require("cjson.safe")
local tableutils = require("fastutils.tableutils")

local redisutils = {
    OK = true,
    ERROR = false,
}

function redisutils.get_redis(host, port, password, database)
    -- set default parameter values
    if database == nil then
        database = 0
    end
    -- create redis isntance
    local redis_sock_opts = {
        pool = host .. ":" .. port .. ":" .. database,
    }
    local redis_instance = redis.new()
    -- do connect
    local redis_ready, redis_error_message = redis_instance:connect(host, port, redis_sock_opts)
    if not redis_ready then
        local error_message = tableutils.concat({
            "get redis connection failed on connect, redis_connect_params=",
            {host=host, port=port, password=password, database=database},
            ", redis_error_message=",
            redis_error_message,
        })
        return redisutils.ERROR, nil, error_message
    end
    -- do auth
    if password then
        local redis_ready, redis_error_message = redis_instance:auth(password)
        if not redis_ready then
            local error_message = tableutils.concat({
                "get redis connection failed on auth, redis_connect_params=",
                {host=host, port=port, password=password, database=database},
                ", redis_error_message=",
                redis_error_message,
            })
            return redisutils.ERROR, nil, error_message
        end
    end
    -- do db select
    local ok, redis_error_message = redis_instance:select(database)
    if redis_error_message then
        local error_message = tableutils.concat({
            "get redis connection failed on select db, redis_connect_params=",
            {host=host, port=port, password=password, database=database},
            ", redis_error_message=",
            redis_error_message,
        })
        return redisutils.ERROR, nil, error_message
    end
    -- done
    return redisutils.OK, redis_instance, nil
end

function redisutils.sismember(redis_instance, key, member)
    -- check redis instance
    if redis_instance == nil then
        return redisutils.ERROR, nil, "redis connection is nil"
    end
    -- check key exists
    local exists, redis_error_message = redis_instance:exists(key)
    if redis_error_message then
        local error_message = tableutils.concat({
            "call redis_instance:exists failed, redis_instance=", redis_instance,
            ", key=", key,
            ", redis_error_message=", redis_error_message
        })
        return redisutils.ERROR, nil, redis_error_message
    end
    if exists == 1 then
        -- check sismember
        local ismember, redis_error_message = redis_instance:sismember(key, member)
        if redis_error_message then
            local error_message = tableutils.concat({
                "call redis_instance:sismember failed, redis_instance=", redis_instance,
                ", key=", key,
                ", redis_error_message=", redis_error_message,
            })
            return redisutils.ERROR, nil, error_message
        end
        -- result
        if ismember == 1 then
            return redisutils.OK, true, nil
        else
            return redisutils.OK, false, nil
        end
    else
        local error_message = tableutils.concat({
            "key not exists, key=", key,
        })
        return redisutils.KEY_ERROR, nil, error_message
    end
end

function redisutils.get_json_data(redis_instance, key)
    -- check redis instance
    if redis_instance == nil then
        return redisutils.ERROR, nil, "redis connection is nil"
    end
    -- check key exists
    local exists, redis_error_message = redis_instance:exists(key)
    if redis_error_message then
        local error_message = tableutils.concat({
            "call redis_instance:exists failed, redis_instance=", redis_instance,
            ", key=", key,
            ", redis_error_message=", redis_error_message
        })
        return redisutils.ERROR, nil, redis_error_message
    end
    if exists == 1 then
        -- get data
        local data, redis_error_message = redis_instance:get(key)
        if data == nil or redis_error_message then
            local error_message = tableutils.concat({
                "call redis_instance:get failed, redis_instance=", redis_instance,
                ", key=", key,
                ", redis_error_message=", redis_error_message,
            })
            return redisutils.ERROR, nil, error_message
        end
        local result = json.decode(data)
        if result == nil then
            local error_message = tableutils.concat({
                "json decode failed on data=", data,
            })
            return redisutils.ERROR, nil, error_message
        else
            return redisutils.OK, result, nil
        end
    else
        local error_message = tableutils.concat({
            "key not exists, key=", key,
        })
        return redisutils.ERROR, nil, error_message
    end
end


return redisutils
