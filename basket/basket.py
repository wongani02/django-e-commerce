from decimal import Decimal
from store.models import Product
from checkout.models import DeliveryOptions


class Basket():
    '''
    A basket class providing some default behaviours that can 
    be inherited or overided if necessary
    '''

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        ''' 
        method for adding products
        '''
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.regular_price), 'qty': qty}

        self.save()

    def __iter__(self):

        """
        Collect the product_id in the session data to query the database
        and return products
        """

        product_ids = self.basket.keys()
        '''import your products model'''
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):

        ''' 
        get basket data and count
        '''

        return sum(item['qty'] for item in self.basket.values())

    def get_subtotal_price(self):

        ''' get subtotal price without shipping inclusive '''

        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())


    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        '''
        get grand price if items in session data
        '''
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def update(self, product, qty):

        """
        Update values in session data
        """

        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def delete(self, product):

        """
        Delete item from session data
        """

        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            # print(product_id)
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session['skey']
        del self.session["address"]
        del self.session["purchase"]
        self.save()

    def save(self):
        self.session.modified = True


    '''
        First of all i would like to thank all you tube contributors or tutors for helping
        me in exploring the different ways to build cart functionality. This whole 
        cart functionality is based on different concepts that i consumed from these you
        tube guys plus the django documentation.
        
        modifying the code above is absolutely fine with me just make sure
        you dont mess up my code base and be sure to include my name whereever 
        you are to use this code.

        Wongani Tembo.
    '''
