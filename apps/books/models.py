from django.db import models

'''
    Table   : Roles
    Content : science, fiction, maths,
'''
class TL_BooksCategory(models.Model):
    code        = models.CharField(max_length=60, unique=True,  null=False)
    name        = models.CharField(max_length=60, unique=False, null=False)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_books_category"


class TL_BooksSubCategory(models.Model):
    code        = models.CharField(max_length=60, unique=True,  null=False)
    name        = models.CharField(max_length=60, unique=False, null=False)
    category    = models.ForeignKey(TL_BooksCategory, null=False, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_books_sub_category"


'''
    Table   : Books
'''
class EN_Books(models.Model):
    name           = models.CharField(max_length=150, null=False)
    volume         = models.IntegerField(null=False, default=1)
    book_code      = models.CharField(max_length=100,null=True)
    author         = models.CharField(max_length=100, null=True)
    publisher      = models.CharField(max_length=100, null=True)
    published_year = models.IntegerField(null=False)
    category       = models.ForeignKey(TL_BooksCategory,on_delete=models.PROTECT,null=False)
    sub_category   = models.ForeignKey(TL_BooksSubCategory,on_delete=models.PROTECT,null=True)
    class Meta:
        db_table = "en_books"
        unique_together = ("name","volume","author","publisher","published_year","category")


