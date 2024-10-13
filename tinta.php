<?php
// Dirección IP de la impresora Epson
$printer_ip = '192.168.0.242';  // Cambia esto por la IP de tu impresora

// Comunidad SNMP, generalmente es 'public'
$community = 'public';

// OIDs para los niveles de tinta (ajústalas si es necesario)
$oid_black_ink = '1.3.6.1.2.1.43.11.1.1.9.1.1';  // Nivel de tinta negra
$oid_cyan_ink = '1.3.6.1.2.1.43.11.1.1.9.1.2';   // Nivel de tinta cian
$oid_magenta_ink = '1.3.6.1.2.1.43.11.1.1.9.1.3'; // Nivel de tinta magenta
$oid_yellow_ink = '1.3.6.1.2.1.43.11.1.1.9.1.4';  // Nivel de tinta amarilla

// Función para obtener el nivel de tinta usando SNMP
function getInkLevel($ip, $community, $oid) {
    $result = @snmpget($ip, $community, $oid);
    if ($result !== false) {
        // Extraer solo los números del resultado SNMP
        $value = preg_replace('/[^0-9]/', '', $result);
        return intval($value);  // Devolver el valor como número
    } else {
        return "No se puede obtener el nivel de tinta";
    }
}

// Obtener niveles de tinta
$black_ink_level = getInkLevel($printer_ip, $community, $oid_black_ink);
$cyan_ink_level = getInkLevel($printer_ip, $community, $oid_cyan_ink);
$magenta_ink_level = getInkLevel($printer_ip, $community, $oid_magenta_ink);
$yellow_ink_level = getInkLevel($printer_ip, $community, $oid_yellow_ink);

// Mostrar niveles de tinta en formato JSON
header('Content-Type: application/json');
echo json_encode([
    'black' => $black_ink_level . '%',
    'cyan' => $cyan_ink_level . '%',
    'magenta' => $magenta_ink_level . '%',
    'yellow' => $yellow_ink_level . '%'
]);
