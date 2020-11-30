/*
    Módulo para las operaciones en el formulario de movimientos en la aplicación 
    inventario. (Implementado con AngularJS).
*/

// Variables globales.
var FIJO = "FIJO";
var PORCENTAJE = "PORCENTAJE";
var URL_MOVIMIENTO_CALCULAR = getById("id_url_movimiento_calcular").value;

// Datos obtenidos del servidor al momento de validar la información.
var validationData = null;

// Formulario.
var form = new Object();
form.self = getById("form1-iframe");
form.articulo = getById("id_articulo");
form.referencia = getById("id_referencia");
form.description = getById("id_description");
form.cantidad = getById("id_cantidad");
form.disponible = getById("id_disponible");
form.precio_introduccido = getById("id_precio_introduccido");
form.precio = getById("id_precio");
form.impuesto_ya_incluido = getById("id_impuesto_ya_incluido");
form.descuento = getById("id_descuento");
form.descuento_tipo = getById("id_descuento_tipo");
form.descuento_total = getById("id_descuento_total");
form.impuesto = getById("id_impuesto");
form.impuesto_value = getById("id_impuesto_value");
form.impuesto_value_type = getById("id_impuesto_value_type");
form.subtotal = getById("id_subtotal");
form.documento = getById("id_documento");
form.movimiento = getById("id_movimiento");


form.getCantidad = function() {
    return form.cantidad.value;
}

form.getPrecioIntroduccido = function() {
    return form.precio_introduccido.value;
}

form.getPrecio = function() {
    if (form.impuesto_ya_incluido.checked) {
        form.precio.value = float(extraerImpuesto(form.getPrecioIntroduccido(), form.impuesto_value_type.value, form.getImpuestoValue())).toFixed(2);
    } else {
        form.precio.value = float(form.getPrecioIntroduccido());
    }
    return float(form.precio.value);
}

form.getImporte = function() {
    return float(form.getCantidad() * form.getPrecio());
}

form.getDescuento = function() {
    form.descuento.value = float(form.descuento.value, "");
    return float(form.descuento.value);
}

form.getDescuentoTotal = function() {
    if (form.descuento_tipo.value == PORCENTAJE) {
        form.descuento_total.value = ((form.getImporte() / 100) * form.getDescuento()).toFixed(2);
    } else if (form.descuento_tipo.value == FIJO) {
        form.descuento_total.value = form.getDescuento();
    }
    return float(form.descuento_total.value);
}

form.getImporteConDescuento = function() {
    return float(form.getImporte() - form.getDescuentoTotal());
}

form.getImpuesto = function() {
    form.impuesto.value = calcularImpuesto(form.getImporteConDescuento(), form.impuesto_value_type.value, form.getImpuestoValue()).toFixed(2);
    return float(form.impuesto.value);
}

form.getImpuestoValue = function() {
    form.impuesto_value.value = float(form.impuesto_value.value, "");
    return float(form.impuesto_value.value);
}

form.getSubtotal = function() {
    form.subtotal.value = float(form.getImporteConDescuento() + form.getImpuesto(), 0).toFixed(2);
    return float(form.subtotal.value);
}

// Valida algunas informaciones del formulario.
// Es resto es validado en el servidor al momento de
// elegir un artículo o realizar el post.
form.validate = function() {
    // El descuento total no puede ser mayor al importe total.
    if (form.getImporte() < form.getDescuentoTotal()) {
        showMessage("El descuento no puede ser mayor al importe total.", title="Descuento", type="danger", alt_out="console");
    }
}

form.update = function() {
    form.getSubtotal();
}


// Eventos.

// Artículo.
form.articulo.onchange = onSelectArticulo;
// Cantidad.
form.cantidad.onchange = calcular;
form.cantidad.onkeyup = calcular;
// Precio introduccido.
form.precio_introduccido.onchange = calcular;
form.precio_introduccido.onkeyup = calcular;
// impuesto_ya_incluido.
form.impuesto_ya_incluido.onchange = calcular;
// Descuento.
form.descuento.onchange = calcular;
form.descuento.onkeyup = calcular;
// Tipo de descuento.
form.descuento_tipo.onchange = calcular;



function serverValidationData() {
    /*
    argumentos pasados por request:
    ::id: id del movimiento (en caso que sea una modificación) (opcional).
    ::id_documento: id del documento al que pertenece el movimiento.
    ::id_articulo: id del artículo del movimiento.
    ::cantidad: Cantidad de artículos.
    ::precio_introduccido: Precio de venta o costo.
    ::descuento: Descuento al importe total.
    ::descuento_tipo: Tipo de descuento 'PORCENTAJE' o 'FIJO'.
    ::impuesto_ya_incluido: True (si el impuesto está incluido en el precio) o False.
    */

    // Debe haber por lo menos un artículo o un movimiento.
    if (!form.articulo.value && !form.movimiento.value) {
        return showMessage("Debe elegir un artículo.", "Sin artículo", "warning");
    }

    kwargs = {
        id: form.movimiento.value,
        documento: form.documento.value,
        articulo: form.articulo.value,
        cantidad: form.cantidad.value,
        precio_introduccido: form.precio_introduccido.value,
        descuento: form.descuento.value,
        descuento_tipo: form.descuento_tipo.value,
        impuesto_ya_incluido: form.impuesto_ya_incluido.checked,
    }

    $.getJSON(URL_MOVIMIENTO_CALCULAR, kwargs, function(data, status, jqXHR) {

        // Quitamos el mensaje que se mostró anteriormente (si es el caso).
        try {
            getById("movimiento-validacion-error").style.display = "none";
        } catch (error) {}


        // Si error validado por el servidor.
        if (data.error) {
            showMessage(msg=data.message, title="Error en validación", type="warning", id="movimiento-validacion-error");
            console.error(data.message + " | " + URL_MOVIMIENTO_CALCULAR);
            validationData = null;

            // Removemos las clases que posiblemente fueron puestas anteriormente en el siguiente bloque.
            fields = ["articulo", "description", "cantidad", "precio_introduccido", "precio", "descuento", "impuesto"]
            for (e in fields) {
                name = fields[e];
                $("#id_"+name).removeClass("is-invalid");
            }

            // Agregamos la clase is-invalid que enfatiza el control relacionado con el error.
            for (e in data.fields) {
                name = data.fields[e];
                $("#id_"+name).addClass("is-invalid");
            }

        } else {
            validationData = data;

            console.log(data);

            // Con esto especificamos el input de cantidad para que solo acepte
            // cantidades enteras o sea permitido el pnto decimal.
            if (data.is_cantidad_entera) {
                form.cantidad.setAttribute("step", "1");
            } else {
                form.cantidad.setAttribute("step", "0.1");
            }

            // Rellenamos el formulario.
            form.referencia.value = data.referencia;
            form.description.value = data.description;

            // Si es una modificación y se trata del mismo artículo
            // el disponible que se muestra será el disponible más la cantidad indicada.
            form.disponible.value = data.disponible;

            if (!form.precio_introduccido.value) {
                form.precio_introduccido.value = data.precio_introduccido;
            }
            form.precio.value = data.precio;
            form.impuesto_ya_incluido.checked = data.impuesto_ya_incluido;
            form.descuento_tipo.value = data.descuento_tipo;
            form.descuento_total.value = data.descuento_total;
            form.impuesto.value = data.impuesto;
            form.impuesto_value.value = data.impuesto_value;
            form.impuesto_value_type.value = data.impuesto_value_type;
            form.subtotal.value = data.total;
            form.update();
        }
    });
}





// Realiza el calculo de los datos introduccidos.
function calcular() {

    if (form.articulo.value && !validationData) {
        serverValidationData();
    } else {
        form.update();
    }
}



// Al seleccionar un artículo.
function onSelectArticulo() {
    serverValidationData();
}



if (validationData || form.articulo.value) {
    serverValidationData();
}





