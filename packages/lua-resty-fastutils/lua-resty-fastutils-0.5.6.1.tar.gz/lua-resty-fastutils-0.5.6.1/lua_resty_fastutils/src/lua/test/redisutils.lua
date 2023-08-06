require("luaunit")

local redisutils = require("redisutils")


TestRedisUtils = {}

function TestRedisUtils:test01()
    local red = redisutils.get_redis("localhost", 6379)
    local keys, op_error = red:keys("*")
    print(keys)
    print(op_error)
end

LuaUnit:run()

