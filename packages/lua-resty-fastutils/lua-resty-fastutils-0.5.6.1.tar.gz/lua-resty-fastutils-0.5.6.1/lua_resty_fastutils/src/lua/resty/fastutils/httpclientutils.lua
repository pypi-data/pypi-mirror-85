local http = require("resty.http")
local neturl = require("net.url")
local json = require("cjson.safe")
local tableutils = require("fastutils.tableutils")

local httpclientutils = {
    OK = true,
    ERROR = false,
}

function httpclientutils.api_call(api_url, api_queries, api_headers)
    -- set default parameter values
    if api_queries == nil then
        api_queries = {}
    end
    if api_headers == nil then
        api_headers = {}
    end
    -- new httpclient instance
    local httpclient = http.new()
    local api_url_info = neturl.parse(api_url)
    -- do connect
    local connected, http_error_message = httpclient:connect(api_url_info.host, api_url_info.port)
    if not connected then
        local error_message = tableutils.concat({
            "call api failed on connect to api server, api_url_info=", api_url_info,
            ", http_error_message=", http_error_message,
        })
        return httpclientutils.ERROR, nil, error_message
    end
    -- do request
    local http_response, http_error_message = httpclient:request({
        method = "GET",
        path = api_url_info.path,
        query = api_queries,
        headers = api_headers
    })
    if http_error_message then
        local error_message = tableutils.concat({
            "call api failed on request to api server, api_url_info=", api_url_info,
            ", http_error_message=", http_error_message,
        })
        return httpclientutils.ERROR, nil, error_message
    end
    -- parse response body
    local http_response_body = http_response:read_body()
    httpclient:set_keepalive()
    local http_response_data = json.decode(http_response_body)
    if http_response_data == nil then
        local error_message = tableutils.concat({
            "call api got bad json response, api_url_info=", api_url_info,
            ", http_response_body=", http_response_body,
        })
        return httpclientutils.ERROR, nil, error_message
    end
    -- done
    return httpclientutils.OK, http_response_data, nil
end


return httpclientutils
