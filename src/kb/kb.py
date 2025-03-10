from kb.web_collector import collectFromWeb
from config.bot import getModelPath
import re
import os
from util.logger import logger


class KnowledgeBase:
    def __init__(self, id, sourceType, source, title, description):
        self.id = id
        self.sourceType = sourceType
        self.source = source
        self.title = title
        self.description = description
        self.content = None

    def collect(self):

        # Collect content from the web
        if self.sourceType == "url":
            self.content = collectFromWeb(self.source)

    def refresh(self):
        pass

    def drop(self):
        pass

    def save(self):
        try:
            dest_dir = getFilePath(self.id)

            # ensure title is a valid filename
            # Replace any character that is not alphanumeric with an underscore
            self.title = re.sub(r'\W+', '_', self.title)
            file_name = f"{self.title}.json"

            # Write content to file
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            file_path = os.path.join(dest_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.content)
        except Exception as e:
            logger.error(f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    kb = KnowledgeBase("candawills", "url", "https://www.canadawills.com/",
                       "Canadawills", "Canadawills FAQs")
    kb.collect()
    if kb.content is not None:
        kb.save()
    else:
        logger.debug("No content was collected.")
