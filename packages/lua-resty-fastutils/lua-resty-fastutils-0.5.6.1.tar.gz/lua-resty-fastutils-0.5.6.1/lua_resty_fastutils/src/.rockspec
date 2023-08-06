package = "lua-resty-fastutils"
version = "0.5.6-1"
source = {
    url = "lua-resty-fastutils-0.5.6-1.zip"
}
description = {
    summary = "Collection of simple utils.",
}
dependencies = {
    "lua >= 5.1, < 5.4",
    "lua-fastutils >= 0.1.5",
    "net-url >= 0.9",
}
build = {
    type = "builtin",
    modules = {
        ["resty.fastutils.httpclientutils"] = "lua/resty/fastutils/httpclientutils.lua",
        ["resty.fastutils.kongutils"] = "lua/resty/fastutils/kongutils.lua",
        ["resty.fastutils.redisutils"] = "lua/resty/fastutils/redisutils.lua",
    }
}