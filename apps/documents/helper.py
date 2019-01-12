from apps.documents.models import EN_Documents
class DocumentHelper:

    def createRootEntry(self, user_id):
        doc=EN_Documents
        EN_Documents.is_file=False
        EN_Documents.is_folder=True
        EN_Documents.name="root"
        EN_Documents.owner=user_id
        EN_Documents.save()

