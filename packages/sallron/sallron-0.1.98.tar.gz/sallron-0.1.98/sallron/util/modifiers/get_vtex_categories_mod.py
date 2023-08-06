def handle_categories(result):
    '''
    This function receives a list of responses from Vtex API with information about products and returns a list of categories for all the products.

    Args: 
        result (list): list of responses.
    Returns:
        categories (list): List of list of categories. 
    '''
    categories={}
    
    for r in result:
        if r and isinstance(r[0], dict):
                categories_temp = r[0].get('categories')
                link_temp = r[0].get('link').split("/")[-2].replace("-", " ").title()

                if isinstance(categories_temp, list):
                    cat_temp = []
                    for item in categories_temp:
                        cat_temp += list(set(item.split('/')))
                elif isinstance(categories_temp, str):
                    cat_temp = list(set(categories_temp.split('/')))
                else:
                    cat_temp = ['']

                cat_temp = list(set(filter(lambda category: category != '', cat_temp)))
                categories.update({link_temp: cat_temp})
        else:
            categories.update({'No product': ['No Category']})
    
    return categories