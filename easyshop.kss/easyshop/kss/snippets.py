PRODUCT_DETAILS = """
    <div class="label">
        <a href="%(url)s">
            %(title)s
            (%(short_title)s)
        </a>    
        <div>%(article_id)s</div>
    </div>

    <p>
        <img style="margin-top:14px"
             class="image-left" 
             src="%(url)s/image_mini" />
             
        %(short_text)s
        
        <span class="label">
            Price
        </span>                                
        <span>
            %(price)s
        </span>
    </p>
    <p style="text-align:right">  
        <a href="%(url)s">
           Go to Product
        </a>   
    </p>    
    <br clear="all" />
"""

RELATED_PRODUCTS_HEADER = """
    <div class="label">
        Related Products
    </div>
    <ul>
"""
RELATED_PRODUCTS_BODY = """
    <li>
        <a href="%(url)s">
            <span>%(title)s</span>
            <span>%(article_id)s</span>
        </a>    
    </li>
"""
RELATED_PRODUCTS_FOOTER = """
    </ul>
"""

CATEGORIES_HEADER = """
    <div class="label">
        Categories
    </div>
    <ul>
"""
CATEGORIES_BODY = """
    <li>
        <a href="%(url)s">
            <span>%(title)s</span>
        </a>    
    </li>
"""
CATEGORIES_FOOTER = """
    </ul>
"""

GROUPS_HEADER = """
    <div class="label">
        Groups
    </div>
    <ul>
"""
GROUPS_BODY = """
    <li>
        <a href="%(url)s">
            <span>%(title)s</span>
        </a>    
    </li>
"""
GROUPS_FOOTER = """
    </ul>
"""
