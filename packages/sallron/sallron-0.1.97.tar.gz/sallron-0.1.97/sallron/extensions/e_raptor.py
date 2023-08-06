from sallron.util.modifiers.get_vtex_categories_mod import handle_categories
from dill.source import getsource
from sallron.util import settings
import requests
import os

PAGESPEED_MAX_RETRIES = 3
RETRY_COUNTER = 0

def get_vtex_categories(
    customer,
    products_names=None,
    environment="vtexcommercestable"):
    """
    Utility function to get the categories related to a specific product.

    Args:
        customer (str): Customer name which has the product
        product_name (list): Product name as it comes from the ga_wrapper functions 
                            access_block, exit_rate_block and sales_block.
        environment (str): Environment to use
    
    Returns: 
        unique_categories (list): A list of the categories names.

    Notes:
        No retries implemented, so this is a candidade for data fetch loss.
    """

    products_names = [product_name.replace(" ", "-").lower() for product_name in products_names]

    invariable_endpoint = f"https://{customer}.{environment}.com.br/api/catalog_system/pub/products/search"

    endpoints = list(map(
                lambda product_name: f"{invariable_endpoint}/{product_name}/p",
                products_names
            ))

    print(f"\n The quantity of endpoints is {len(endpoints)}. \n")

    modifier = getsource(handle_categories)

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    endpoint_chunks = chunks(endpoints, 3000)

    categories = {}
    for chunk in endpoint_chunks:
        body = {
            "urls": chunk,
            "modifiers": [modifier],
            "strings": ['handle_categories(result)'],
            "headers": None
        }

        categories =dict(
            categories, **requests.post(
                settings.MAX_STEEL_URL,
                json=body,
                headers={"Content-Type": "application/json"}
            ).json()
        ) 

    return categories

def get_pagespeed_required_urls(customer, environment="vtexcommercestable"):
    """
    """
    global RETRY_COUNTER
    endpoint = f"https://{customer}.{environment}.com.br/api/catalog_system/pub/products/search?fq=isAvailablePerSalesChannel_1:1&_from=1&_to=3&O=OrderByTopSaleDESC"
    productids = []
    product_text_links = []
    categories = []
    response = requests.get(endpoint)
    response_json = response.json()

    if response.status_code in range(200, 300):
        for item in response_json:
            productids.append(item.get('productId'))
            product_text_links.append(item.get('linkText'))
            categories.append(item.get('categories')[0])
            RETRY_COUNTER = 0

    while response.status_code not in range(200, 300):
        print(f"The status_code of the request is {response.status_code}")
        RETRY_COUNTER += 1
        print(f"Retry number {RETRY_COUNTER}")
        response = requests.get(endpoint)
        if RETRY_COUNTER == PAGESPEED_MAX_RETRIES:
            RETRY_COUNTER = 0
            productids = [123,123,123] # Dummy prodIDs so code doesn't break
            break

    url_checkout = f"https://{customer}.{environment}.com.br/checkout/cart/add?sku={productids[0]}&qty=1&seller=1&sku={productids[1]}&qty=1&seller=1&sku={productids[2]}&qty=1&seller=1&redirect=true&sc=1"
    return url_checkout, product_text_links, categories

if __name__ == "__main__":
    from sallron.eye import configureye
    from pprint import pprint
    
    configureye(MAX_STEEL_URL="https://....us-east-2.amazonaws.com/prod")
    
    products_names=[
        'cooktop-a-gas-5-bocas-ke5tp-electrolux',
        'lavadora-de-roupas-16kg-tecnologia-jatos-poderosos-electrolux-lpe16'
    ]

    pprint(get_vtex_categories(
        customer='electrolux', 
        products_names=products_names,

    ))
    