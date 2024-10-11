from tortoise import fields, models

class Item(models.Model):
    """
    Database model representing an item.

    Attributes:
        id (int): The unique identifier for the item, serves as the primary key.
        name (str): The name of the item, stored as a string with a maximum length of 255 characters.
        description (str): A text field containing the description of the item.
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()

    class Meta:
        """
        Metadata for the Item model.

        This sets the table name in the database to 'items'.
        """
        table = "items"
