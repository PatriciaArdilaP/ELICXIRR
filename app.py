from flask import Flask, render_template, request, redirect, url_for, session
import os
# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-dev")
# Clave secreta (necesaria para manejar el carrito con sesiones)


# ------------------------
# Catálogo de productos
# ------------------------
PRODUCTS = [
    {"id": "p01", "name": "Flawless Foundation", "price": 39900, "img" : "img/producto_inicial.jpg"},
    {"id": "p02", "name": "Premium Gloss", "price": 25000, "img": "img/producto_labial2.jpg"},
    {"id": "p03", "name": "Active Shadow", "price": 29900, "img": "img/sombras.jpg"},
    {"id": "p04", "name": "Liquid Lip Gloss", "price": 22500, "img": "img/producto_labial1.jpg"},
    {"id": "p05", "name": "Natural Cream", "price": 35000, "img": "img/producto_rubor.jpg"},
    {"id": "p06", "name": "Lipstick Duo", "price": 28900, "img": "img/producto_labial1.jpg"},
    {"id": "p07", "name": "Gold Shadow", "price": 31500, "img": "img/sombras.jpg"},
    {"id": "p08", "name": "Brillo Gloss", "price": 24900, "img": "img/producto_brillo1.jpg"},
]

# ------------------------
# RUTAS PRINCIPALES
# ------------------------

# Página principal
@app.route("/")
def home():
    return render_template("Home.html")

# Página de la tienda
@app.route("/tienda")
def tienda():
    return render_template("tienda.html", products=PRODUCTS)

# Carrito
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# Agregar producto al carrito
@app.route("/add_to_cart/<id>")
def add_to_cart(id):
    cart = session.get("cart", [])
    product = next((p for p in PRODUCTS if p["id"] == id), None)

    if product:
        existing = next((item for item in cart if item["id"] == id), None)
        if existing:
            existing["qty"] += 1
        else:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "img": product["img"],  # ✅ Guarda la imagen
                "qty": 1
            })
        session["cart"] = cart

    return redirect(url_for("cart"))

# Eliminar producto del carrito
@app.route("/remove_from_cart/<id>")
def remove_from_cart(id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != id]
    session["cart"] = cart
    return redirect(url_for("cart"))

# Vaciar carrito
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))

# ------------------------
# CHECKOUT Y CONFIRMACIÓN
# ------------------------

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart)

    if not cart:
        return redirect(url_for("cart"))

    if request.method == "POST":
        # Crear el pedido
        order = {
            "items": cart,
            "total": total,
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "direccion": request.form.get("direccion"),
        }

        # Vaciar carrito y guardar pedido
        session.pop("cart", None)
        session["order"] = order

        return redirect(url_for("confirmacion"))

    return render_template("checkout.html", cart=cart, total=total)

@app.route("/confirmacion")
def confirmacion():
    order = session.get("order", {})
    return render_template("confirmacion.html", order=order)

# ------------------------
# INICIO DE LA APLICACIÓN
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)


