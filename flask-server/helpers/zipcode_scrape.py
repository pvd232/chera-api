from bs4 import BeautifulSoup
import requests


def get_nyc_msa_zipcodes():
    nj_zipcodes_url_object = {
        "url": "https://www.zipdatamaps.com/list-of-zip-codes-in-new-jersey.php", "state": "NJ"}
    ny_zipcodes_url_object = {
        "url": "https://www.zipdatamaps.com/list-of-zip-codes-in-new-york.php", "state": "NY"}
    # we dont want to deliver to PA
    # pa_zipcodes_url_object = {
    #     "url": "https://www.zipdatamaps.com/list-of-zip-codes-in-pennsylvania.php", "state": "PA"}
    zipcode_url_list = [nj_zipcodes_url_object,
                        ny_zipcodes_url_object]

    zipcode_objects = []
    for zipcode_url in zipcode_url_list:
        response = requests.get(zipcode_url["url"])
        soup = BeautifulSoup(response.text, "html.parser")
        zipcodes_div = soup.find("table", {
                                 "class": "table table-striped table-bordered table-hover table-condensed"})
        zipcode_rows = zipcodes_div.find_all("tr")
        zipcodes_td = [div.find("td") for div in zipcode_rows]
        zipcodes_a = [td.find("a") for td in zipcodes_td]

        zipcodes = []
        for anchor in zipcodes_a:
            if anchor:
                zipcode = anchor.attrs.get("href")
                zipcodes.append(zipcode)

        zipcode_objects.append(
            {"state": zipcode_url["state"], "zipcodes": zipcodes, "covered_zipcodes": []})

    nyc_msa_url = 'https://statisticalatlas.com/maps/nav/other/101722/Zcta#Overview'
    response = requests.get(nyc_msa_url)
    soup = BeautifulSoup(response.text, features="xml")
    map_svg_data = soup.find(
        "g", {"class": "featured-no-stroke"})
    zipcodes_raw = [a.attrs.get("xlink:href")
                    for a in map_svg_data.find_all("a")]

    for zipcode in zipcodes_raw:
        if zipcode:
            zipcode_split = zipcode.split("/")
            formatted_zipcode = zipcode_split[2]
            for zipcode_object in zipcode_objects:
                for state_zipcode in zipcode_object["zipcodes"]:
                    formatted_zipcode
                    if state_zipcode == formatted_zipcode:
                        zipcode_object["covered_zipcodes"].append(
                            formatted_zipcode)
    new_zipcodes_objects = [{"state": zipcode_object["state"],
                             "zipcodes":zipcode_object["covered_zipcodes"]} for zipcode_object in zipcode_objects]

    return new_zipcodes_objects


get_nyc_msa_zipcodes()
