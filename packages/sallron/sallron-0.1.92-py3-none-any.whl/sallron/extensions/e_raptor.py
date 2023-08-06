import requests
import functools

PAGESPEED_MAX_RETRIES = 3
RETRY_COUNTER = 0

def get_vtex_categories(
    customer,
    product_name,
    environment="vtexcommercestable"):
    """
    This function will get the categories related to a specific product.

    Args:
        customer (str): Customer name which has the product
        product_name (str): Product name as it comes from the ga_wrapper functions 
                            access_block, exit_rate_block and sales_block.
        environment (str): Environment to use
    
    Returns: 
        unique_categories (list): A list of the categories names.

    Notes:
        No retries implemented, so this is a candidade for data fetch loss.
    """

    product_name = product_name.replace(" ", "-").lower()

    endpoint = f"https://{customer}.{environment}.com.br/api/catalog_system/pub/products/search/{product_name}/p"

    r = requests.get(endpoint).json()
    if r and isinstance(r[0], dict):
        categories = r[0].get('categories')

        categories = list(set(functools.reduce(lambda x, y: x + y, map(
                lambda string: list(filter(
                    lambda element: element,
                    string.split('/')
                )),
                categories
            ))))

        return categories
    else:
        return ["No category"]

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
    print(get_pagespeed_required_urls('fibracirurgica'))