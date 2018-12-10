from apps.books.models import TL_BooksCategory, TL_BooksSubCategory

class BookHelper() :

    def getBookCategoryList(self):
        chMailList = []
        for row in TL_BooksCategory.objects.all():
            chList = []
            chList.append(row.code)
            chList.append(row.name)
            chMailList.append(tuple(chList))
        return tuple(chMailList)