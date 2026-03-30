"""
Page Objects Init
"""

from .base_page import BasePage
from .form_page import FormPage
from .button_page import ButtonPage
from .progress_page import ProgressPage
from .tab_page import TabPage
from .table_page import TablePage
from .file_upload_page import FileUploadPage

__all__ = [
    'BasePage',
    'FormPage',
    'ButtonPage',
    'ProgressPage',
    'TabPage',
    'TablePage',
    'FileUploadPage'
]
