from io import BytesIO


# Load .env into a string stream
def load_env(env_path: str = ".env") -> BytesIO:
    stream = BytesIO()
    with open(env_path, 'r', encoding='utf-8') as file:
        stream.write(file.read().encode('utf-8'))
    stream.seek(0)
    return stream
