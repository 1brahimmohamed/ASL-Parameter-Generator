import os
import yaml
from .exceptions import ConfigurationError


class Config:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.allowed_file_types_path = os.path.join(config_dir, 'allowed_file_types.yaml')
        self.schemas_dir = os.path.join(config_dir, 'schemas')

    def _load_yaml_file(self, path) -> dict:
        """
        Load a YAML file from the given path.
        :param path:  Path to the YAML file.
        :return: Parsed YAML content as a dictionary.
        """
        if not os.path.exists(path):
            raise ConfigurationError(f"Config file not found: {path}")

        with open(path, 'r') as f:
            content = yaml.safe_load(f)

        if not isinstance(content, dict) or 'allowed_file_types' not in content:
            raise ConfigurationError(f"Invalid config file: {path}")

        return content


    def _load_schemas(self) -> dict:
        """
        Load all YAML schema files from the schemas directory.
        Use the top-level key inside each YAML file as the schema name.
        :return: A dictionary where keys are schema names and values are the parsed schema content.
        """
        schemas = {}
        for root, _, files in os.walk(self.schemas_dir):
            for file in files:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    file_path = os.path.join(root, file)
                    content = self._load_yaml_file(file_path)
                    if isinstance(content, dict) and len(content) == 1:
                        key = next(iter(content))
                        schemas[key] = content[key]
                    else:
                        # fallback: use file name without extension
                        schema_name = os.path.splitext(file)[0]
                        schemas[schema_name] = content
        return schemas

    def load(self) -> dict:
        """
        Load the configuration, including allowed file types and schemas.
        :return:  A dictionary containing allowed file types and schemas.
        """
        allowed_file_types = self._load_yaml_file(self.allowed_file_types_path)
        schemas = self._load_schemas()

        print(allowed_file_types)
        print(schemas)

        return {
            'allowed_file_type': allowed_file_types['allowed_file_types'],
            'schemas': schemas
        }


# Global config instance
CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
config_loader = Config(CONFIG_DIR)
config = config_loader.load()
