PRODUCT_DETAILS = """
<table class="shop-default">
    <tr>
        <td width="210px"
            class="image">
            <img src="%(url)s/image_mini" />
        </td>
        
        <td class="information">
            <a href="%(url)s">
                %(title)s
                (%(short_title)s)
            </a>    
            <div>%(article_id)s</div>        
            <p>
                %(short_text)s
        
                <span class="label">
                    Price
                </span>                                
                <span>
                    %(price)s
                </span>
            </p>
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
    </ul><td></tr></table>
"""
