
class TranslationError(Exception):
    """Lỗi cơ sở cho các chức năng dịch thuật."""


class TranslationConfigurationError(TranslationError):
    """Lỗi cấu hình dịch thuật."""


class TranslationAPIError(TranslationError):
    """Lỗi khi gọi API dịch thuật."""


class TranslationTimeoutError(TranslationError):
    """API phản hồi quá thời gian cho phép."""


class UnsupportedProviderError(TranslationError):
    """Nhà cung cấp dịch thuật không được hỗ trợ."""
