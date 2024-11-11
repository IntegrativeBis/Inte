from RealdataAPI_client import RealdataAPIClient

# Initialize the RealdataAPIClient with your API token
client = RealdataAPIClient("<YOUR_API_TOKEN>")

# Prepare the actor input
run_input = {
    "startUrls": [
        { "url": "https://www.walmart.com/browse/auto-tires/brake-pads/91083_1074765_9038935_4582920" },
        { "url": "https://www.walmart.com/browse/home/" },
        { "url": "https://www.walmart.com/search?grid=true&query=Mixed+Bouquets" },
        { "url": "https://www.walmart.com/ip/Mainstays-Blue-Sunflower-Mix-Bouquet/155345382" },
    ],
    "maxItems": 50,
    "endPage": 1,
    "extendOutputFunction": """($) => {
    const result = {};
    // Uncomment to add a title to the output
    // result.title = $('title').text().trim();

    return result;
}""",
    "outputFilterFunction": "(object) => ({...object})",
    "proxy": { "useRealdataAPIProxy": True },
}

# Run the actor and wait for it to finish
run = client.actor("epctex/walmart-scraper").call(run_input=run_input)

# Fetch and print actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)