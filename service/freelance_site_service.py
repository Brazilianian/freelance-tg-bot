from domain.sites.freelance_site import FreelanceSite
from domain.sites.freelance_sites_enum import FreelanceSitesEnum


def from_json_to_object(freelance_site_json):
    return FreelanceSite(freelance_site_json['name'],
                         freelance_site_json['link'])


def from_freelance_site_to_enum(freelance_site: FreelanceSite):
    for member in FreelanceSitesEnum:
        if member.value == freelance_site.name:
            return member
    return None
