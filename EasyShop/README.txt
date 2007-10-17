Copyright (c) 2007 Kai Diefenbach iqplusplus - kai.diefenbach@iqpp.de
All Rights Reserved.

EasyShop is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

EasyShop is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EasyShop; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

**EasyShop**

  A online shop for Plone

**Some features in short:**
  
  Properties

    Free definable properties for products (like color, size and weight), with possibillity to change (increase or decrease) the price.
    
  Categories

    To structure products for users. Categories are used to browse through the shop. Products can be in arbitrary categories.

  Groups
  
    To group products for internal reasons. For instance to assign product properties, taxes, shipping prices and so on.
  
  Taxes
  
    Taxes can be assigned to products and customers by several criteria: Date, country, product, group, category, etc.
  
  Shipping
  
    Shipping prices can be assigned by several criteria: Total amount, weight, country, customer, etc.
  
  Payment
  
    PayPal, Direct Debit. Prepayment.
  
  Pluggable
  
    EasyShop tries to be as pluggable as possible (this will be much more with Plone 3.0). For instance you could write your own shipping price to satisfy 
    more complex prices. HowTos will follow.
  
  Presentation
  
    Their are several approaches to format the views of the shop (product selectors: select arbitray products per level, formatter: select columns, lines,   
    image size, description type).
  
**Real Live**

  There is already an (adapted) EasyShop online (and the first products are sold ;-). You can find it here. http://demmelhuber.net/laden

**Demo Shop**

  there is a demo EasyShop now:

  http://shop-1.iqpp.de

  This is a OOTB EasyShop with some content added, which is kindly provided by Dirk Kommol, one of my customers.

  To be a shop manager use:

    manager / manager

  Otherwise just register the default Plone way und you will be a customer.

  Be careful with testing PayPal as EasyShop redirects to the real PayPal site (as not everyone would have access to the sandbox). If you want to try it 
  nevertheless, there is a test product for 0,01 Euro (just search for "Testartikel").

**Credits**

  Many thanks goes to my first shop customer Demmelhuber Holz & Raum, especially Dirk Kommol. His ideas and suggestions concerning e-shopping and EasyShop 
  are very helpful. Moreover he kindly offered me to provide a full copy of his live shop for above mentioned demo shop.

  Some icons are taken from Mark James' silk icons (http://www.famfamfam.com/lab/icons/silk/)