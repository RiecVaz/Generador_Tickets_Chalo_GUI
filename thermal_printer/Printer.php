<?php
require __DIR__ . '/vendor/autoload.php';
use Mike42\Escpos\PrintConnectors\WindowsPrintConnector;
use Mike42\Escpos\Printer;
use Mike42\Escpos\EscposImage;

#Se obtiene la información requerida en forma de strings
$Ordenes_json = htmlspecialchars($_GET["Orden"]);
$info_json = htmlspecialchars($_GET["Info"]);

#Sustituir comillas simples por dobles 
$Ordenes_json_comillas = str_replace("'",'"',$Ordenes_json);
$info_json_comillas = str_replace("'",'"',$info_json);

#Convertimos en array
$Ordenes = json_decode($Ordenes_json_comillas,true);
$info = json_decode($info_json_comillas,true);

$connector = new WindowsPrintConnector("EC_LINE");
$printer = new Printer($connector);

#Insertar Logo
$logo = EscposImage::load("Imagen/Logo2.png");
$printer->setJustification(Printer::JUSTIFY_CENTER);
$printer->bitImage($logo);
$printer -> feed();

#Insertar título
$printer -> selectPrintMode($printer::MODE_DOUBLE_HEIGHT | $printer::MODE_DOUBLE_WIDTH | $printer::MODE_UNDERLINE);
$printer -> text(" MARISCOS CHALO");
$printer -> feed(2);
$printer -> selectPrintMode($printer::MODE_FONT_A);

#Definir variables de información complementaria
$fecha = $info[0];
$mesa = $info[1];
$personas = $info[2];
$descuento = $info[3];
$importe = $info[4];

$printer -> text("Fecha: ".$fecha);
$printer -> feed();
$printer -> text("Mesa: ".str_pad($mesa,2,"0",STR_PAD_LEFT)."                "."#Per: ".str_pad($personas,2,"0",STR_PAD_LEFT));
$printer -> feed(2);

#Insertar encabezados
$printer -> selectPrintMode($printer::MODE_EMPHASIZED);
$printer -> text("CANT."."      "."CONCEPTO"."       "."PRECIO");
$printer -> selectPrintMode($printer::MODE_FONT_A);

$total = 0;
// Acepta: OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO 32 caracteres
// 00_000000000000000000000000_0000
foreach($Ordenes as $Orden){

    //Definir los conceptos de la orden
    $cant = $Orden["CANTIDAD"];
    $des_string = $Orden["DESCRIPCION"];
    $pre = $Orden["PRECIO"];
    
    #Si la descripción es muy larga, la cortamos
    if(strlen($des_string) >= 25){
        $des = substr($des_string,0,24);
    }
    else{
        $des = $des_string;
    }
  
    // Obtener el total
    $total += $pre;
    $printer -> text(str_pad($cant, 2, "0", STR_PAD_LEFT)." ".str_pad($des,24," ",STR_PAD_RIGHT)." ".str_pad($pre,4," ",STR_PAD_LEFT));
    $printer -> feed();
}

#Agregamos descuento o importe extra según sea el caso
if( ($descuento != 0) && ($importe != 0) ){
    $printer -> selectPrintMode($printer::MODE_EMPHASIZED);
    $total = $total - $descuento + $importe;

    $printer -> text("DESCUENTO DE LA CASA: "."      ".str_pad($descuento,4," ",STR_PAD_LEFT));
    $printer -> feed();
    $printer -> text("IMPORTE: "."                   ".str_pad($importe,4," ",STR_PAD_LEFT));
}
elseif($descuento != 0){
    $printer -> selectPrintMode($printer::MODE_EMPHASIZED);
    $total -= $descuento;
    $printer -> text("DESCUENTO DE LA CASA: "."      ".str_pad($descuento,4," ",STR_PAD_LEFT));
}
elseif($importe != 0){
    $printer -> selectPrintMode($printer::MODE_EMPHASIZED);
    $total += $importe;
    $printer -> text("IMPORTE: "."                   ".str_pad($importe,4," ",STR_PAD_LEFT));
}

$printer -> feed();
$printer -> selectPrintMode($printer::MODE_EMPHASIZED);
$printer -> text("TOTAL"."$".str_pad($total,26," ", STR_PAD_LEFT));
$printer -> feed(2);

#Calcular impuestos
$impuestos = $total * 0.16;

#Colocar pie
$printer -> text("Impuestos Incluidos");
$printer -> feed();
$printer -> text("| 16.0 % de ". $total. " ". " es: ".$impuestos." |");
$printer -> feed();
$printer -> text("--------------------------------");
$printer -> text("ESTIMADO CLIENTE, SE LE INFORMA:");
$printer -> feed();
$printer -> text("Puede pedir su factura en caja");
$printer -> feed();
$printer -> text("--------------------------------");
$printer -> feed(2);
$printer -> selectPrintMode($printer::MODE_EMPHASIZED);
$printer -> text("¡FUE UN GUSTO ATENDERLE!");
$printer -> feed(5);
$printer -> close();

?>

