<?php

// Declaramos las credenciales de conexion
$host = "localhost"; /* Nombre de host */
$user = "strongsystems"; /* User */
$password = "k8TY6&c7D4mW"; /* Password */
$dbname = "strong_db"; /* Nombre de la base de datos */

// Creamos la conexion MySQL
$db = new mysqli($host, $user, $password,$dbname);
// Verificamos la conexión
if (!$db) {
die("Conexion fallida: " . mysqli_connect_error());
}
?>