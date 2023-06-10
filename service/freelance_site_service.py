from domain.freelance_site import FreelanceSite


def from_json_to_object(freelance_site_json):
    return FreelanceSite(freelance_site_json['name'],
                         freelance_site_json['link'])
