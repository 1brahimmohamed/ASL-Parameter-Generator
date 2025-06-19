import json


class FileReader:

    @staticmethod
    def read(file_path):
        try:
            # Determine if the input is a FileStorage object or a file path
            if isinstance(file_path, str):
                file_stream = open(file_path, 'r')
            else:
                raise RuntimeError("Unsupported file type: {type(file_path)}")

            if file_path.endswith('.json'):
                return FileReader._read_json(file_stream)

            elif file_path.endswith('.tsv'):
                return FileReader._read_tsv(file_stream)

            else:
                raise RuntimeError("Unsupported file format")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error decoding JSON from file: {e.msg}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {str(e)}")

    @staticmethod
    def _read_json(file_stream):
        """
        Reads a JSON file and returns its content.

        :param file_stream: Path to the JSON file.
        :return: Parsed JSON data.
        """
        with file_stream as f:
            content = f.read().strip()  # Read the content and strip any leading/trailing whitespace
            if content:  # Check if the file is not empty
                data = json.loads(content)  # Parse JSON content
                return data
            else:
                return None

    @staticmethod
    def _read_tsv(file_stream):
        """
        Reads a TSV file and returns its content as a list of strings.
        :param file_stream: Path to the TSV file.
        :return: List of strings representing the TSV content, or None if the file is empty.
        """
        with file_stream as f:
            lines = f.readlines()

        if not lines:
            return None

        header = lines[0].strip()

        if header != 'volume_type':
            raise RuntimeError("Invalid TSV header, not \"volume_type\"")

        data = [line.strip() for line in lines[1:]]
        return data
