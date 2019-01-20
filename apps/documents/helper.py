from apps.documents.models import EN_Documents

class DocumentHelper:

    def createRootEntry(self, user_id):
        doc=EN_Documents()
        doc.is_file=False
        doc.is_folder=True
        doc.name="ROOT"
        doc.owner_id=user_id
        doc.is_root = True
        doc.save()