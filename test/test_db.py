import unittest
import dotenv
from db.neo4j_db import init_db
from autogen.agentchat.contrib.graph_rag.document import Document, DocumentType
import os


class TestDB(unittest.TestCase):
    dotenv.load_dotenv()
    def test_db_init(self):
        input_path = "/mnt/d/project-gabut/bsaa/PoA Guideline.pdf"
        # Check if the file exists; if not, the test will fail with the provided message.
        self.assertTrue(os.path.exists(input_path), f"File not found: {input_path}")
        input_documents = [Document(doctype=DocumentType.TEXT, path_or_url=input_path)]
        init_db(docs=input_documents)

if __name__ == '__main__':
    unittest.main()