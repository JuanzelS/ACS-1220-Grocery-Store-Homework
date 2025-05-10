from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from grocery_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

# Add a context processor to ensure current_user is available in templates
@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

##########################################
# Routes #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(new_store)
        db.session.commit()
        flash('New store added successfully!')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()
    
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user
        )
        db.session.add(new_item)
        db.session.commit()
        flash('New item added successfully!')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get_or_404(store_id)
    
    form = GroceryStoreForm(obj=store)
    
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash('Store updated successfully!')
        return redirect(url_for('main.store_detail', store_id=store.id))
    
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    
    form = GroceryItemForm(obj=item)
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        flash('Item updated successfully!')
        return redirect(url_for('main.item_detail', item_id=item.id))
    
    return render_template('item_detail.html', item=item, form=form)

##########################################
# Authentication Routes #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created. Please log in.')
        return redirect(url_for('auth.login'))
    
    # Use flash messages for errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")
                
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        flash('You have been logged in successfully!')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.homepage'))

##########################################
# Shopping List Routes #
##########################################

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    if item not in current_user.shopping_list_items:
        current_user.shopping_list_items.append(item)
        db.session.commit()
        flash(f'{item.name} added to your shopping list!')
    else:
        flash(f'{item.name} is already in your shopping list!')
    return redirect(url_for('main.item_detail', item_id=item_id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    items = current_user.shopping_list_items.all()
    return render_template('shopping_list.html', items=items)

@main.route('/remove_from_shopping_list/<item_id>', methods=['POST'])
@login_required
def remove_from_shopping_list(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    if item in current_user.shopping_list_items:
        current_user.shopping_list_items.remove(item)
        db.session.commit()
        flash(f'{item.name} removed from your shopping list!')
    return redirect(url_for('main.shopping_list'))
@main.route('/remove_item/<item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    
    # Check if the current user created the item
    if item.created_by != current_user:
        flash("You don't have permission to delete this item.")
        return redirect(url_for('main.item_detail', item_id=item.id))
    
    # Store the store_id before deleting the item
    store_id = item.store.id
    store_name = item.store.title
    item_name = item.name
    
    # Delete the item
    db.session.delete(item)
    db.session.commit()
    
    flash(f'{item_name} has been removed from {store_name}.')
    return redirect(url_for('main.store_detail', store_id=store_id))