def sanitize_filename(name: str) -> str:
    """格式化文件名
    name: 文件名
    """
    return (
        name
        .replace('\\', '_')
        .replace('/', '_')
        .replace('|', '_')
        .replace('?', '？')
        .replace(':', '：')
        .replace('*', '_')
        .replace('"', '_')
        .replace('<', '《')
        .replace('>', '》')
        .replace('.', '_')
    )