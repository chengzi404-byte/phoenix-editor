def validate_settings(settings):
    """验证设置是否有效"""
    required_fields = ["file-encoding", "lang", "font", "fontsize", "code"]
    for field in required_fields:
        if field not in settings:
            return False
    return True
