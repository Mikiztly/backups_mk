$(document).ready(function () {
  // Datapicker
  $(".datepicker").datepicker({
    dateFormat: "yy-mm-dd",
    changeYear: true,
  });

  // Iniciamos el DataTable
  var dataTable = $("#routers").DataTable({
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json",
    },
    processing: true,
    serverSide: true,
    serverMethod: "post",
    searching: true,
    ajax: {
      url: "extraer.php",
      data: function (data) {
        // Leer valores de fecha
        var buscar_inicio = $("#buscar_inicio").val();
        var buscar_fin = $("#buscar_fin").val();

        // Append to data
        data.buscarFechaInicio = buscar_inicio;
        data.buscarFechaFin = buscar_fin;
      },
    },
    "pageLength": 100,
    "columnDefs": [ {
        "targets": 0,
        "createdCell": function (td, cellData, rowData, row, col) {
          if ( cellData == "NO" ) {
            $(td).css('background-color', '#FF8A80')
          };
          if ( cellData == "OK" ) {
            $(td).css('background-color', '#1fe039')
          }
        }
      } ],
    columns: [{ data: "status" }, { data: "date" }, { data: "client" }, { data: "system_name" }],
  });

  // Boton Buscar
  $("#btn_search").click(function () {
    dataTable.draw();
  });
});
