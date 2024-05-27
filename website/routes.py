from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import ProductDatabase, UserBasket, Likes
from . import db

routes = Blueprint('routes', __name__)


@routes.route("/")
@login_required  # have to be logged in to access home page
def home():
    products = ProductDatabase.query.order_by(ProductDatabase.id.desc()).all()

    return render_template('home.html', user=current_user, products=products)


@routes.route("/addproduct/", methods=['POST', 'GET'])
@login_required
def addproduct():
    if request.method == 'POST':
        product_name = request.form.get('productName')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')

        new_product = ProductDatabase(product_name=product_name, price=price, stock=stock, description=description)

        db.session.add(new_product)  # add new product info into product database model
        db.session.commit()

        flash('Your product has been added to the market!')
        return redirect(url_for('routes.home'))

    return render_template('addproduct.html', user=current_user)


@routes.route("/mybasket/")
@login_required
def mybasket():
    user_basket = UserBasket.query.filter_by(user_id=current_user.id).order_by(UserBasket.date_added.desc()).all()  # display item(s) in user's basket
    total_price = sum(item.product.price * item.quantity for item in user_basket)

    return render_template("mybasket.html", user=current_user, basket=user_basket, total_price=total_price)


@routes.route("/addintobasket/", methods=['POST'])
@login_required
def addintobasket():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))

        product = ProductDatabase.query.filter_by(id=product_id).first()

        # check if the product listed is sold by current user
        is_user_product = current_user in product.users_rls if product else False

        if is_user_product:
            flash('You cannot add your own product to your basket!')
        else:
            # calculate the number of quantity in the basket
            existing_item = UserBasket.query.filter_by(user_id=current_user.id, product_id=product_id).first()
            total_quantity = quantity if existing_item is None else quantity + existing_item.quantity

            if product.stock >= total_quantity > 0:  # if product is not out of stock
                if existing_item:  # to update the quantity of the item
                    existing_item.quantity += quantity
                else:  # add item into basket
                    basket_item = UserBasket(user_id=current_user.id, product_id=product_id, quantity=quantity)
                    db.session.add(basket_item)
                db.session.commit()
                flash(f'Added "{product.product_name}" into your basket!')
            else:
                flash(f'The total quantity you have selected for "{product.product_name}" exceeds the available stock limit in your basket.', category='error')

    return redirect(url_for('routes.home'))


@routes.route("/deleteitem/", methods=['POST'])
@login_required
def delete_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        item_to_delete = UserBasket.query.filter_by(id=item_id).first()

        if item_to_delete:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item deleted successfully!', category='success')
        else:
            flash('Item not found or could not be deleted!', category='error')

    return redirect(url_for('routes.mybasket'))


@routes.route("/editbasket/", methods=['POST'])
@login_required
def editbasket():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        new_quantity = int(request.form.get('quantity'))

        # update quantity in basket
        item_to_edit = UserBasket.query.filter_by(id=item_id).first()
        if item_to_edit:
            item_to_edit.quantity = new_quantity
            db.session.commit()
            flash('Quantity updated successfully!', category='success')
        else:
            flash('Item not found or could not be updated!', category='error')

    return redirect(url_for('routes.mybasket'))


@routes.route("/purchase/", methods=['POST'])
def purchase():
    if request.method == 'POST':
        confirmation = request.json.get('confirmation')

        if confirmation:  # handles purchase confirmation
            user_basket = UserBasket.query.filter_by(user_id=current_user.id).all()
            for item in user_basket:
                item.product.stock -= item.quantity
                db.session.delete(item)  # clears basket after purchase is confirmed
            db.session.commit()
            flash('Thank you for purchasing the item(s) in your basket! You have been redirected to the Explore page.')

            return jsonify({'success': True})

    return jsonify({'success': False})


@routes.route("/favourite/", methods=['POST'])
@login_required
def favourite():
    if request.method == 'POST':
        product_id = request.json.get('product_id')
        product = ProductDatabase.query.get(product_id)

        if product:
            like = Likes.query.filter_by(user_id=current_user.id, product_id=product_id).first()
            if like:
                db.session.delete(like)
            else:
                new_like = Likes(user_id=current_user.id, product_id=product_id)
                db.session.add(new_like)

            db.session.commit()
            return jsonify({'success': True})

    return jsonify({'success': False})
