from tortoise import fields, models

class Item(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()

    class Meta:
        table = "items"
