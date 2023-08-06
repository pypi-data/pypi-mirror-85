
local httputils = require("fastutils.httputils")
local kong = kong
local kongutils = {
    OK = true,
    ERROR = false,
}

function kongutils.set_request_header(headers)
    if headers == nil then
        headers = {}
    end
    for name, value in pairs(headers) do
        kong.service.request.set_header(name, value)
    end
end

function kongutils.get_request_data(name, use_body)
    if use_body == nil then
        use_body = false
    end
    local queries = kong.request.get_query()
    local headers = kong.request.get_headers()
    local body = nil
    if use_body then
        body = kong.request.get_body()
    end
    return httputils.get_request_data(name, queries, body, headers)
end


return kongutils
