"""
Test File Upload
文件上传测试模块
"""

import time


class TestFileUpload:
    """文件上传测试类"""
    
    def test_upload_text_file(self, file_upload_page, tmp_path):
        """测试上传文本文件"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("这是一个测试文件")
        
        file_upload_page.upload_file(str(test_file))
        time.sleep(1)
        
        assert file_upload_page.is_file_uploaded()
        file_info = file_upload_page.get_file_info()
        assert "test.txt" in file_info
    
    def test_upload_file_info_display(self, file_upload_page, tmp_path):
        """测试上传文件信息显示"""
        test_file = tmp_path / "test_document.pdf"
        test_file.write_bytes(b"PDF content" * 100)
        
        file_upload_page.upload_file(str(test_file))
        time.sleep(1)
        
        file_info = file_upload_page.get_file_info()
        assert "test_document.pdf" in file_info
        assert "KB" in file_info
    
    def test_upload_different_extensions(self, file_upload_page, tmp_path):
        """测试上传不同扩展名文件"""
        extensions = ["txt", "pdf", "jpg", "png"]
        
        for ext in extensions:
            test_file = tmp_path / f"test.{ext}"
            test_file.write_text(f"Test content for {ext}")
            
            file_upload_page.upload_file(str(test_file))
            time.sleep(0.5)
            
            file_info = file_upload_page.get_file_info()
            assert f"test.{ext}" in file_info
