
// Vue App.
const App = {

    data() {
        return {
            alert: {
                title: "",
                message: "",
            },
            user: {
                id: '{{ user.id }}',
                username: '{{ user }}',
            },
            cart: {
                items: {},
                total: {
                    count: 0,
                    cant: 0,
                    subtotal: 0,
                    tax: 0,
                    total: 0
                }
            },
            url: {
                store_item_list: "",
                store_cart_list: "",
                store_cart_add: "",
                store_cart_update: "",
                store_cart_remove: "",
            }

        }
    },



    created() {
        this.url = URL;
        sendData(this.getUrl("store-cart-get"), "GET", "json", {}, this.getData);
    },



    methods: {

        // Se usa la función intcomma del módulo base.js.
        intcomma(num) {
            return intcomma(num);
        },


        getUrl: function (name) {
            return this.url[name];
        },


        // Agrega un item al carrito.
        addItem(id) {
            let cant = document.getElementById("id_cant").value;
            let url = this.getUrl("store-cart-add");
            let formdata = $("#form-add-cart").serialize();
            sendData(url, "POST", "json", formdata, this.getData);
        },


        // Se llamará como un evento que invoca a su vez a 'updateItem'.
        onUpdateItemFromCtrl(event) {
            let ctrl = event.target;
            let item_id = ctrl.dataset.item;
            let cant = ctrl.value;
            this.updateItem(item_id, cant);
        },

        
        // Actualiza el item indicado con la cantidad indicada.
        updateItem(id, cant) {
            let url = this.getUrl("store-cart-update")+"?item_id="+id+"&cant="+cant;
            sendData(url, "GET", "json", null, this.getDataWithoutAlert);
        },


        // Quita del carrito el item con el id indicado.
        removeItem(id) {
            let url = this.getUrl("store-cart-remove")+"?item_id="+id;
            sendData(url, "GET", "json", null, this.getData);
        },


        // Quita del carrito todos los items.
        removeItemAll() {
            this.removeItem("all");
        },


        // Extrae la información obtenida del servidor.
        getData(data) {
            if (data.error) {
                this.showAlert(data.message, 10000);
            } else {
                this.cart.items = data.cart;
                this.cart.total = data.cart_total;
                this.showAlert(data.message, 5000);
            }
        },


        // Lo mismo que getData pero solo muestra mensaje en caso de error.
        getDataWithoutAlert(data) {
            if (data.error) {
                this.showAlert(data.message, 10000);
            } else {
                this.cart.items = data.cart;
                this.cart.total = data.cart_total;
            }
        },


        // Muestra un mensaje en pantalla por el tiempo indicado.
        showAlert(message="", time=5000) {
            this.alert.message = message;
            
            setTimeout(() => {
                this.alert.message = "";
            }, time);
        },
    }
}



Vue.createApp(App).mount("#app");