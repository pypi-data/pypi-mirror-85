import requests
import functools

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
    """

    product_name = product_name.replace(" ", "-").lower()

    endpoint = f"https://{customer}.{environment}.com.br/api/catalog_system/pub/products/search/{product_name}/p"

    r = requests.get(endpoint).json()

    categories = r[0].get('categories')

    categories = list(set(functools.reduce(lambda x, y: x + y, map(
            lambda string: list(filter(
                lambda element: element,
                string.split('/')
            )),
            categories
        ))))

    return categories

def get_pagespeed_required_urls(customer, environment="vtexcommercestable"):
    """
    """
    endpoint = f"https://{customer}.{environment}.com.br/api/catalog_system/pub/products/search?fq=isAvailablePerSalesChannel_1:1&_from=1&_to=3&O=OrderByTopSaleDESC"

    r = requests.get(endpoint).json()

    productids = []
    product_text_links = []
    categories = []
    for item in r:
        productids.append(item.get('productId'))
        product_text_links.append(item.get('linkText'))
        categories.append(item.get('categories')[0])

    url_checkout = f"https://{customer}.{environment}.com.br/checkout/cart/add?sku={productids[0]}&qty=1&seller=1&sku={productids[1]}&qty=1&seller=1&sku={productids[2]}&qty=1&seller=1&redirect=true&sc=1"
    
    return url_checkout, product_text_links, categories