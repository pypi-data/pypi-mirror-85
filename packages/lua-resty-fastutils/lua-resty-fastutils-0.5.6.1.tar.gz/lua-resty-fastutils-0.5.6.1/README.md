# lua-resty-fastutils

Collection of simple utils.

## Install

```shell
pip install lua-resty-fastutils
```

## LUA Modules

- resty.fastutils.httpclientutils
  - api_call
- resty.fastutils.kongutils
  - set_request_header
  - get_request_data
- resty.fastutils.redisutils
  - get_redis
  - sismember
  - get_json_data

## Installed Command Utils

- manage-lua-resty-fastutils

## Usage

```shell
Usage: manage-lua-resty-fastutils [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install  Create a lua package and then install it.
  pack     Create a lua package.
```

## Releases

### 0.5.6-1 2020/11/12

- Noop.

### 0.5.4-1 2020/11/04

- Rename resty.fastutils.httputils to resty.fastutils.httpclientutils.
- Fix redisutils.
- Change httpclientutils and redisutils' response data structure to (success, result, error_message).
- Add kongutils.

### 0.2.0-1 2020/08/27

- First release under new framework.
