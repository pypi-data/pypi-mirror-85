import os
from luaproject import LuaProjectManager
import lua_resty_fastutils

application_root = os.path.abspath(os.path.dirname(lua_resty_fastutils.__file__))
manager = LuaProjectManager(application_root).get_manager()

if __name__ == "__main__":
    manager()
