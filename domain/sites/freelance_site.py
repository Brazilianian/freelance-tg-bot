from domain.sites.freelance_sites_enum import FreelanceSitesEnum


class FreelanceSite:
    name: FreelanceSitesEnum
    link: str

    def __init__(self,
                 name: FreelanceSitesEnum,
                 link: str):
        self.name = name
        self.link = link

    def __str__(self):
        return f"name - {self.name} " \
               f"link - {self.link} "
