from django.db import models

# Create your models here.

class BaseModel(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True
class Wheel(BaseModel):
    class Meta:
        db_table = 'axf_wheel'


class Nav(BaseModel):
    class Meta:
        db_table='axf_nav'


class Mustbuy(BaseModel):
    class Meta:
        db_table='axf_mustbuy'


class Shop(BaseModel):
    class Meta:
        db_table='axf_shop'



# trackid,name,img,categoryid,brandname,img1a,childcid1,productid1,longname1,price1,marketprice1

class Mainshow(models.Model):
    trackid=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    img=models.CharField(max_length=100)
    categoryid=models.CharField(max_length=10)
    brandname=models.CharField(max_length=100)


    img1=models.CharField(max_length=100)
    childcid1=models.CharField(max_length=10)
    productid1=models.CharField(max_length=10)
    longname1=models.CharField(max_length=100)
    price1=models.CharField(max_length=10)
    marketprice1=models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table='axf_mainshow'

# typeid,typename,childtypenames,typesort

class Foodtypes(models.Model):

    typeid=models.CharField(max_length=10)
    typename=models.CharField(max_length=100)
    childtypenames=models.CharField(max_length=200)
    typesort=models.IntegerField()

    class Meta:
        db_table='axf_foodtypes'
# productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum
class  Goods(models.Model):
    # 商品ID
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=200)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 商品长名字
    productlongname = models.CharField(max_length=200)
    # 是否精选
    isxf = models.IntegerField()
    # 是否买一送一
    pmdesc = models.IntegerField()
    # 规格
    specifics = models.CharField(max_length=100)
    # 价格
    price = models.DecimalField(max_digits=6,decimal_places=2)
    # 超市价格
    marketprice = models.DecimalField(max_digits=6,decimal_places=2)
    # 分类ID
    categoryid = models.CharField(max_length=10)
    # 子类ID
    childcid = models.CharField(max_length=10)
    # 子类名字
    childcidname = models.CharField(max_length=100)
    # 详情id
    dealerid = models.CharField(max_length=100)
    # 库存量
    storenums = models.IntegerField()
    # 销售量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'




class User(models.Model):

    # 邮箱
    email=models.CharField(max_length=40,unique=True)

    password=models.CharField(max_length=256)

    name=models.CharField(max_length=100)

    img=models.CharField(max_length=40,default='axf.png')

    # 等级
    rank=models.IntegerField(default=1)

    class Meta:
        db_table='axf_user'



