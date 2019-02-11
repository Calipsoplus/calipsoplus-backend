def enum(**enums):
    return type('Enum', (), enums)


ResourceType = enum(dockercontainer="docker_container", kubernetes="kubernetes", virtual_machine="virtual_machine",
                    static_link="static_link")
