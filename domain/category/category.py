from domain.sites.freelance_sites_enum import FreelanceSitesEnum


class Category:
    id: int
    name: str
    freelance_site: FreelanceSitesEnum

    def __init__(self, category_id: int, name: str, freelance_site: FreelanceSitesEnum):
        self.id = category_id
        self.name = name
        self.freelance_site = freelance_site

    def __str__(self):
        return f"id - {self.id} " \
               f"name - {self.name} " \
               f"freelance_site - {self.freelance_site} "
