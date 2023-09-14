class FreelanceSite:
    name: str
    link: str

    def __init__(self,
                 name: str,
                 link: str):
        self.name = name
        self.link = link

    def __str__(self):
        return f"name - {self.name} " \
               f"link - {self.link} "
