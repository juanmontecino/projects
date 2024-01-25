document.addEventListener("DOMContentLoaded", function() {
    const formulario = document.getElementById("miFormulario");

    formulario.addEventListener("submit", function(event) {
        if (!validarFormulario()) {
            event.preventDefault();
        }
    });

    function validarFormulario() {
        
        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellido").value;
        const numero_tel = document.getElementById("numero").value;

        if (!/^[a-zA-Z]+$/.test(nombre)) {
            alert("El nombre no puede contener números");
            nombre.focus();
            return false;
        }
        else if (!/^[a-zA-Z]+$/.test(apellido)) {
            alert("El apellido no puede contener números");
            apellido.focus();
            return false;
        }

        else if (isNaN(numero_tel)) {
            alert("Ingrese un número de teléfono válido");
            numero_tel.focus();
            return false;
        }

        // Puedes agregar más validaciones según tus necesidades
        else{
        return true;
        }
    }
});
