from domain.freelance_site import FreelanceSite


class Proposal:
    id: int
    title: str
    price: str
    description: str
    link: str
    additional_info_tags: str
    posted_date: str
    freelance_site: FreelanceSite

    def __init__(self,
                 prop_id: int,
                 title: str,
                 price: str,
                 description: str,
                 link: str,
                 additional_info_tags: str,
                 posted_date: str,
                 freelance_site: FreelanceSite):
        self.id = prop_id
        self.title = title
        self.price = price
        self.description = description
        self.link = link
        self.additional_info_tags = additional_info_tags
        self.posted_date = posted_date
        self.freelance_site = freelance_site

    def __str__(self):
        return f"id - {self.id}\n" \
               f"title - {self.title}\n" \
               f"price - {self.price}\n" \
               f"description - {self.description}\n" \
               f"link - {self.link}\n" \
               f"additional_info_tags: {self.additional_info_tags}\n" \
               f"date: {self.posted_date}"
