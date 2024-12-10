<head>
    <!-- jQuery UI CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.css">

    <!-- jQuery Library -->
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>

    <!-- jQuery UI JS -->
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>

    <!-- Datatable JS -->
    <script src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js"></script>

    <!-- Datatable Boostrap5 -->
    <script src="https://cdn.datatables.net/1.11.3/js/dataTables.bootstrap5.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.11.3/css/dataTables.bootstrap5.min.css">
</head>

<main>
    <div class="container">
        <div class="alert alert-primary" role="alert">
            Estado de routers
        </div>

        <!-- Date Filter -->
        <form id="formFecha">
            <table>
                <tr>
                    <td>
                        <input type='text' readonly id='buscar_inicio' class="datepicker" placeholder='Fecha Inicio' class="form-control form-control-sm">
                    </td>
                    <td>
                        <input type='text' readonly id='buscar_fin' class="datepicker" placeholder='Fecha fin' class="form-control form-control-sm">
                    </td>
                    <td>
                        <input type='button' id="btn_search" value="Buscar" class="btn btn-primary btn-sm">
                    </td>
                    <td>
                        <input type='button' id="btnLimpiar" value="Limpiar" class="btn btn-danger btn-sm">
                    </td>
                </tr>
            </table>
        </form>
        <hr>
        <!-- Table -->
        <table id='routers' class="table table-striped" style="width:100%">
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Fecha</th>
                    <th>Cliente</th>
                    <th>Router MK</th>
                </tr>
            </thead>

        </table>
    </div>

</main>
<script src="script.js"></script>
<script>
    $("#btnLimpiar").click(function(event) {
        $("#formFecha")[0].reset();
    });
    const dateInput = document.getElementById('buscar_inicio');
    dateInput.value = new Date().toJSON().slice(0, 10);
</script>
