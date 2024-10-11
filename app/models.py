from tortoise import fields, models

class Item(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()

    class Meta:
        table = "items"
