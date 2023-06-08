from peewee import TextField, AutoField

from model.base_model import BaseModel


class FreelanceSiteModel(BaseModel):
    id: AutoField(primary_key=True,
                  auto_increment=True)
    name: TextField()
    link: TextField()

    def __str__(self):
        return f"id - {self.id} " \
               f"name - {self.name} " \
               f"link - {self.link} "
