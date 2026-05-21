import os
import unittest
import shutil
from key_manager import KeyManager


class TestKeyManager(unittest.TestCase):
    
    def setUp(self):
        os.environ["MASTER_PASSWORD"] = "test_password_123"
        self.manager = KeyManager(storage_path=".test_keys")
    
    def tearDown(self):
        if os.path.exists(".test_keys"):
            shutil.rmtree(".test_keys")
    
    def test_save_and_get_key(self):
        self.manager.save_key("test_key", "test_value")
        retrieved_value = self.manager.get_key("test_key")
        self.assertEqual(retrieved_value, "test_value")
    
    def test_save_key_with_metadata(self):
        metadata = {"service": "test_service", "version": "1.0"}
        self.manager.save_key("key_with_meta", "value", metadata)
        keys = self.manager.list_keys()
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0]["metadata"]["service"], "test_service")
    
    def test_update_key(self):
        self.manager.save_key("update_test", "old_value")
        self.manager.update_key("update_test", "new_value")
        retrieved_value = self.manager.get_key("update_test")
        self.assertEqual(retrieved_value, "new_value")
    
    def test_delete_key(self):
        self.manager.save_key("delete_test", "value")
        self.assertTrue(self.manager.delete_key("delete_test"))
        self.assertIsNone(self.manager.get_key("delete_test"))
    
    def test_list_keys(self):
        self.manager.save_key("key1", "value1")
        self.manager.save_key("key2", "value2")
        self.manager.save_key("key3", "value3")
        keys = self.manager.list_keys()
        self.assertEqual(len(keys), 3)
    
    def test_get_nonexistent_key(self):
        result = self.manager.get_key("nonexistent")
        self.assertIsNone(result)
    
    def test_export_keys(self):
        self.manager.save_key("export_key1", "value1")
        self.manager.save_key("export_key2", "value2")
        self.assertTrue(self.manager.export_keys("test_export.json"))
        self.assertTrue(os.path.exists("test_export.json"))
        os.remove("test_export.json")


if __name__ == "__main__":
    unittest.main()
