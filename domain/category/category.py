from domain.sites.freelance_site import FreelanceSite


class Category:
    id: int
    name: str
    freelance_site: FreelanceSite

    def __init__(self, id: int, name: str, freelance_site: FreelanceSite):
        self.id = id
        self.name = name
        self.freelance_site = freelance_site

    def __str__(self):
        return f"name - {self.name} " \
               f"freelance_site - {self.freelance_site} "
