import os
from pathlib import Path

# load properties from environment based on the environment name
env_name = os.getenv("ENV_NAME", "test")
# declare global variable to store the properties
env_properties = {}


def load_properties(file_name, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    global env_properties
    path_name = None
    try:
        # Point to appropriate ancestor directory
        resource_path = Path(__file__).parent.parent.parent
        # print('resource_path: ', resource_path)
        resource_file_path = str(resource_path) + '/resources/' + file_name
        # path_name = importlib.resources.path(file_name)
        # print('path_name: ', resource_file_path)
        with open(resource_file_path, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    env_properties[key] = value
    except Exception as e:
        print(e)
        print('Error while loading properties from file={}, path={}'.format(file_name, path_name))
    pass


def get_property(prop_name):
    """
    Get the property value based on the property name passed as parameter.
    """
    global env_properties
    if env_properties is None or len(env_properties) == 0:
        load_properties(env_name + ".properties")

    return env_properties.get(prop_name)


# define main function
if __name__ == "__main__":
    print(get_property("PG_DB_NAME"))
