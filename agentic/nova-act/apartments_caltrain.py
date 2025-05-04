"""Find some apartments and calculate distance to Caltrain station.

Usage:
python -m nova_act.samples.apartments_caltrain \
    [--caltrain_city <city_with_a_caltrain_station>] \
    [--bedrooms <number_of_bedrooms>] \
    [--baths <number_of_baths>] \
    [--headless]

python -m nova_act.samples.apartments_caltrain \
    --caltrain_city "Palo Alto" \
    --bedrooms 1 \
    --baths 1 


"""

from concurrent.futures import ThreadPoolExecutor, as_completed

import fire  # type: ignore
import pandas as pd
from pydantic import BaseModel

from nova_act import NovaAct


class Apartment(BaseModel):
    address: str
    price: str
    beds: str
    baths: str


class ApartmentList(BaseModel):
    apartments: list[Apartment]


class CaltrainBiking(BaseModel):
    biking_time_hours: int
    biking_time_minutes: int
    biking_distance_miles: float


def add_biking_distance(apartment: Apartment, caltrain_city: str, headless: bool) -> CaltrainBiking | None:
    with NovaAct(
        starting_page="https://maps.google.com/",
        headless=headless,
    ) as nova:
        nova.act(
            f"Search for {caltrain_city} Caltrain station and press enter. "
            "Click Directions. "
            f"Enter '{apartment.address}' into the starting point field and press enter. "
            "Click the bicycle icon for cycling directions."
        )
        result = nova.act("Return the shortest time and distance for biking", schema=CaltrainBiking.model_json_schema())
        if not result.matches_schema:
            print(f"Invalid JSON {result=}")
            return None
        time_distance = CaltrainBiking.model_validate(result.parsed_response)
        return time_distance


def main(
    caltrain_city: str = "Redwood City",
    bedrooms: int = 2,
    baths: int = 1,
    headless: bool = False,
    min_apartments_to_find: int = 5,
) -> None:
    all_apartments: list[Apartment] = []

    with NovaAct(
        starting_page="https://zumper.com/",
        headless=headless,
    ) as nova:

        nova.act(
            "Close any cookie banners. "
            f"Search for apartments near {caltrain_city}, CA, "
            f"then filter for {bedrooms} bedrooms and {baths} bathrooms. "
            "If you see a dialog about saving a search, close it. "
            "If results mode is 'Split', switch to 'List'. "
        )

        for _ in range(5):  # Scroll down a max of 5 times.
            result = nova.act(
                "Return the currently visible list of apartments", schema=ApartmentList.model_json_schema()
            )
            if not result.matches_schema:
                print(f"Invalid JSON {result=}")
                break
            apartment_list = ApartmentList.model_validate(result.parsed_response)
            all_apartments.extend(apartment_list.apartments)
            if len(all_apartments) >= min_apartments_to_find:
                break
            nova.act("Scroll down once")

        print(f"Found apartments: {all_apartments}")

    apartments_with_biking = []
    with ThreadPoolExecutor() as executor:
        future_to_apartment = {
            executor.submit(add_biking_distance, apartment, caltrain_city, headless): apartment
            for apartment in all_apartments
        }
        for future in as_completed(future_to_apartment.keys()):
            apartment = future_to_apartment[future]
            caltrain_biking = future.result()
            if caltrain_biking is not None:
                apartments_with_biking.append(apartment.model_dump() | caltrain_biking.model_dump())
            else:
                apartments_with_biking.append(apartment.model_dump())

    apartments_df = pd.DataFrame(apartments_with_biking)
    closest_apartment_data = apartments_df.sort_values(
        by=["biking_time_hours", "biking_time_minutes", "biking_distance_miles"]
    )

    print()
    print("Biking time and distance:")
    print(closest_apartment_data.to_string())


if __name__ == "__main__":
    fire.Fire(main)


"""
$ python -m nova_act.samples.apartments_caltrain \
>     --caltrain_city "Palo Alto" \
>     --bedrooms 1 \
>     --baths 1



start session 5a2e80df-3021-422b-9981-37cdc9844476 on https://zumper.com/ logs dir /var/folders/l1/dzcw8wr90wxdt447b9wlfw3r0000gn/T/tmpkdl88bes_nova_act_logs/5a2e80df-3021-422b-9981-37cdc9844476

5a2e> act("Close any cookie banners. Search for apartments near Palo Alto, CA, then filter for 1 bedrooms and 1 bathrooms. If you see a dialog about saving a search, close it. If results mode is 'Split', switch to 'List'. ")
...............
5a2e> think("I am on the Zumper homepage. I see a cookie banner at the bottom of the page. I should complete my task by closing the cookie banner. I am now on the homepage, not the search results page. I need to close the cookie banner. I should click on the 'Accept Cookies' button to close the cookie banner.");
>> agentClick("<box>736,1314,776,1442</box>");
.................
5a2e> think("The screenshot now shows that the cookie banner is closed. My prior action of clicking on the 'Accept Cookies' button was successful. The cookie banner is now closed, which is what I need. The search field is empty, but it should say 'Palo Alto, CA'. I should click on the search field and type 'Palo Alto, CA' to search for that location.");
>> agentType("Palo Alto, CA", "<box>388,556,442,1042</box>");
....................
5a2e> think("The screenshot now shows that 'Palo Alto, CA' is entered in the search field. My prior action of typing 'Palo Alto, CA' in the search field was successful. 'Palo Alto, CA' is now entered in the search field, which is what I need. The search has not been initiated yet. I should click on the 'Palo Alto, CA' search suggestion to initiate the search.");
>> agentClick("<box>486,562,538,1034</box>");
.............................
5a2e> think("The screenshot now shows that I am on the search results page for Palo Alto, CA. My prior action of clicking on the Palo Alto, CA search suggestion was successful. I am now on the search results page for Palo Alto, CA, which is what I need. I can see the beds/baths filter, but it is not expanded yet. I should click on the beds/baths filter to expand it.");
>> agentClick("<box>84,24,120,134</box>");
.....................
5a2e> think("The screenshot now shows that the beds/baths filter is expanded. My prior action of clicking on the beds/baths filter was successful. The beds/baths filter is now expanded, which is what I need. I can see the 1 bedroom option, but it is not selected yet. I should click on the 1 bedroom option to select it.");
>> agentClick("<box>178,124,222,166</box>");
....................
5a2e> think("The screenshot now shows that 1 bedroom is selected. My prior action of clicking on the 1 bedroom option was successful. 1 bedroom is now selected, which is what I need. I can see the 1 bathroom option, but it is not selected yet. I should click on the 1 bathroom option to select it.");
>> agentClick("<box>284,40,324,90</box>");
....................
5a2e> think("The screenshot now shows that 1 bathroom is selected. My prior action of clicking on the 1 bathroom option was successful. 1 bathroom is now selected, which is what I need. I can see the view 28 rentals button, but it has not been selected yet. I should click on the view 28 rentals button to view the rentals.");
>> agentClick("<box>366,154,400,312</box>");
.....................
5a2e> think("The screenshot now shows that I am on the results page. My prior action of clicking on the view 28 rentals button was successful. I am now on the results page, which is what I need. I can see a popup on the page, and I need to close it. I see an 'x' button that should close it. I should click on the 'x' button to close the popup.");
>> agentClick("<box>232,988,258,1014</box>");
...................
5a2e> think("The screenshot now shows that the popup has closed. My prior action of clicking on the 'x' button was successful. I am now on the results page without the popup, which is what I need. I can see that the results are currently in split mode, and I need them to be in list mode. I see the 'List' button. I should click on the list button to change the results mode.");
>> agentClick("<box>88,1402,116,1452</box>");
....................
5a2e> think("The screenshot now shows that I am on the list view. My prior action of clicking on the list button was successful. I am now on the list view, which is what I need. My task to close any cookie banners, search for apartments near Palo Alto, CA, then filter for 1 bedrooms and 1 bathrooms and if you see a dialog about saving a search, close it and if results mode is 'Split', switch to 'List' has been completed successfully. My task is complete, and no return information was asked of me. I should empty return.");
>> return;
.....5a2e> act("Return the currently visible list of apartments, format output with jsonschema: {"$defs": {"Apartment": {"properties": {"address": {"title": "Address", "type": "string"}, "price": {"title": "Price", "type": "string"}, "beds": {"title": "Beds", "type": "string"}, "baths": {"title": "Baths", "type": "string"}}, "required": ["address", "price", "beds", "baths"], "title": "Apartment", "type": "object"}}, "properties": {"apartments": {"items": {"$ref": "#/$defs/Apartment"}, "title": "Apartments", "type": "array"}}, "required": ["apartments"], "title": "ApartmentList", "type": "object"}")
................
5a2e> think("Extracting:  Return the currently visible list of apartments");
>> return "{\"apartments\": [{\"address\": \"565 Arastradero Rd, Palo Alto, CA 94306\", \"price\": \"Call for price\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"3375 Alma St, Palo Alto, CA 94306\", \"price\": \"$2,705\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"696 Towle Way #34, Palo Alto, CA 94303\", \"price\": \"$2,895\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"562 Kendall Ave #39, Palo Alto, CA 94301\", \"price\": \"$2,395\", \"beds\": \"1\", \"baths\": \"1\"}]}";
.....5a2e> act("Scroll down once")
..............
5a2e> think("I am on the Zumper website for 1 bedroom apartments in Palo Alto, CA. My task is to scroll down the page. I need to scroll down the page. I see that I can scroll down the page. I should scroll down the page to view more information.");
>> agentScroll("down", "<box>0,0,812,1600</box>");
................
5a2e> think("The page has scrolled down and new information is visible, therefore my last action was successful. I have scrolled down the page. The task is complete, and I need to return.");
>> return;
....5a2e> act("Return the currently visible list of apartments, format output with jsonschema: {"$defs": {"Apartment": {"properties": {"address": {"title": "Address", "type": "string"}, "price": {"title": "Price", "type": "string"}, "beds": {"title": "Beds", "type": "string"}, "baths": {"title": "Baths", "type": "string"}}, "required": ["address", "price", "beds", "baths"], "title": "Apartment", "type": "object"}}, "properties": {"apartments": {"items": {"$ref": "#/$defs/Apartment"}, "title": "Apartments", "type": "array"}}, "required": ["apartments"], "title": "ApartmentList", "type": "object"}")
................
5a2e> think("Extracting:  Return the currently visible list of apartments");
>> return "{\"apartments\": [{\"address\": \"524 Kendall Ave, Palo Alto, CA 94306\", \"price\": \"$2,295\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"562 Kendall Ave #14, Palo Alto, CA 94306\", \"price\": \"$2,445\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"501 Forest Avenue\", \"price\": \"$5,640\", \"beds\": \"1\", \"baths\": \"1\"}, {\"address\": \"588 Channing Ave #1648, Palo Alto, CA 94306\", \"price\": \"$4,420\", \"beds\": \"1\", \"baths\": \"1\"}]}";
......Found apartments: [Apartment(address='565 Arastradero Rd, Palo Alto, CA 94306', price='Call for price', beds='1', baths='1'), Apartment(address='3375 Alma St, Palo Alto, CA 94306', price='$2,705', beds='1', baths='1'), Apartment(address='696 Towle Way #34, Palo Alto, CA 94303', price='$2,895', beds='1', baths='1'), Apartment(address='562 Kendall Ave #39, Palo Alto, CA 94301', price='$2,395', beds='1', baths='1'), Apartment(address='524 Kendall Ave, Palo Alto, CA 94306', price='$2,295', beds='1', baths='1'), Apartment(address='562 Kendall Ave #14, Palo Alto, CA 94306', price='$2,445', beds='1', baths='1'), Apartment(address='501 Forest Avenue', price='$5,640', beds='1', baths='1'), Apartment(address='588 Channing Ave #1648, Palo Alto, CA 94306', price='$4,420', beds='1', baths='1')]

end session

"""    