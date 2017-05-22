# Tarea 4

Como en las tareas anteriores se utilizó PyQt5 para la interfaz que se implementa en la clase View. La clase principal es `Simulator` que posee métodos encargados de realizar las acciones que el usuario solicite. Cada evento es representado con una clase particular. Todas estas clases tienen el método `simulate` que realiza los cambios correspondientes a ese evento. Los parámetros se obtienen de la clase `Parameters` que lee los archivos escenarios.csv y parametros.csv.

# Programacion

<html xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:x="urn:schemas-microsoft-com:office:excel"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=macintosh">
<meta name=ProgId content=Excel.Sheet>
<meta name=Generator content="Microsoft Excel 15">
<link rel=File-List href="Workbook1.fld/filelist.xml">
<style>
<!--table
	{mso-displayed-decimal-separator:"\.";
	mso-displayed-thousand-separator:"\,";}
@page
	{margin:.75in .7in .75in .7in;
	mso-header-margin:.3in;
	mso-footer-margin:.3in;}
.style0
	{mso-number-format:General;
	text-align:general;
	vertical-align:bottom;
	white-space:nowrap;
	mso-rotate:0;
	mso-background-source:auto;
	mso-pattern:auto;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:Calibri, sans-serif;
	mso-font-charset:0;
	border:none;
	mso-protection:locked visible;
	mso-style-name:Normal;
	mso-style-id:0;}
td
	{mso-style-parent:style0;
	padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:Calibri, sans-serif;
	mso-font-charset:0;
	mso-number-format:General;
	text-align:general;
	vertical-align:bottom;
	border:none;
	mso-background-source:auto;
	mso-pattern:auto;
	mso-protection:locked visible;
	white-space:nowrap;
	mso-rotate:0;}
.xl65
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;}
.xl66
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;}
.xl67
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	white-space:normal;}
.xl68
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;}
.xl69
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	white-space:normal;}
.xl70
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	white-space:normal;}
.xl71
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:yellow;
	mso-pattern:black none;}
.xl72
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:yellow;
	mso-pattern:black none;
	white-space:normal;}
.xl73
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:yellow;
	mso-pattern:black none;
	white-space:normal;}
.xl74
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:yellow;
	mso-pattern:black none;
	white-space:normal;}
.xl75
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#ED7D31;
	mso-pattern:black none;}
.xl76
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#ED7D31;
	mso-pattern:black none;
	white-space:normal;}
.xl77
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#ED7D31;
	mso-pattern:black none;}
.xl78
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:#ED7D31;
	mso-pattern:black none;
	white-space:normal;}
.xl79
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#70AD47;
	mso-pattern:black none;}
.xl80
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#70AD47;
	mso-pattern:black none;
	white-space:normal;}
.xl81
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#70AD47;
	mso-pattern:black none;}
.xl82
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:#70AD47;
	mso-pattern:black none;
	white-space:normal;}
.xl83
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:red;
	mso-pattern:black none;}
.xl84
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:red;
	mso-pattern:black none;
	white-space:normal;}
.xl85
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:red;
	mso-pattern:black none;}
.xl86
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:red;
	mso-pattern:black none;
	white-space:normal;}
.xl87
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#5B9BD5;
	mso-pattern:black none;}
.xl88
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#5B9BD5;
	mso-pattern:black none;
	white-space:normal;}
.xl89
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#5B9BD5;
	mso-pattern:black none;}
.xl90
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:#5B9BD5;
	mso-pattern:black none;
	white-space:normal;}
.xl91
	{mso-style-parent:style0;
	color:windowtext;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#7030A0;
	mso-pattern:black none;}
.xl92
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#7030A0;
	mso-pattern:black none;
	white-space:normal;}
.xl93
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:left;
	border:.5pt solid windowtext;
	background:#7030A0;
	mso-pattern:black none;}
.xl94
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:#7030A0;
	mso-pattern:black none;}
.xl95
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;
	background:#7030A0;
	mso-pattern:black none;
	white-space:normal;}
.xl96
	{mso-style-parent:style0;
	font-size:11.0pt;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	border:.5pt solid windowtext;}
-->
</style>
</head>

<body link="#0563C1" vlink="#954F72">

<table border=0 cellpadding=0 cellspacing=0 width=1631 style='border-collapse:
 collapse;table-layout:fixed;width:1225pt'>
 <col width=233 span=7 style='mso-width-source:userset;mso-width-alt:7466;
 width:175pt'>
 <tr height=36 style='mso-height-source:userset;height:27.0pt'>
  <td height=36 class=xl65 width=233 style='height:27.0pt;width:175pt'>L</td>
  <td class=xl65 width=233 style='width:175pt'>M</td>
  <td class=xl65 width=233 style='width:175pt'>W</td>
  <td class=xl65 width=233 style='width:175pt'>J</td>
  <td class=xl65 width=233 style='width:175pt'>V</td>
  <td class=xl65 width=233 style='width:175pt'>S</td>
  <td class=xl65 width=233 style='width:175pt'>D</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl66 style='height:54.0pt'>1</td>
  <td class=xl66 style='border-left:none'>2</td>
  <td class=xl66 style='border-left:none'>3</td>
  <td class=xl67 width=233 style='border-left:none;width:175pt'>Clase OOP<br>
  AC01<br>
  4</td>
  <td class=xl66 style='border-left:none'>5</td>
  <td class=xl68 style='border-left:none'>6</td>
  <td class=xl68 style='border-left:none'>7</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl69 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  8</td>
  <td class=xl69 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  9</td>
  <td class=xl69 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  10</td>
  <td class=xl67 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  OOP2<br>
  AC02<br>
  </td>
  <td class=xl70 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T01<br>
  12</td>
  <td class=xl71 style='border-top:none;border-left:none'>13</td>
  <td class=xl71 style='border-top:none;border-left:none'>14</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl72 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  15</td>
  <td class=xl72 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  16</td>
  <td class=xl72 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  17</td>
  <td class=xl73 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Estructuras<br>
  AC03<br>
  Envio notas AC01 y C si hay ctrl</td>
  <td class=xl71 style='border-top:none;border-left:none'>19</td>
  <td class=xl71 style='border-top:none;border-left:none'>20</td>
  <td class=xl71 style='border-top:none;border-left:none'>21</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl72 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Renunion Ayudantes Docencia<br>
  22</td>
  <td class=xl72 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  23</td>
  <td class=xl72 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  24</td>
  <td class=xl73 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Arboles, grafos<br>
  AC04<br>
  Envio notas AC02 y C si hay ctrl</td>
  <td class=xl74 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T02<br>
  Entrega T01 a las 23:59</td>
  <td class=xl75 style='border-top:none;border-left:none'>27</td>
  <td class=xl75 style='border-top:none;border-left:none'>28</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl76 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  29</td>
  <td class=xl77 style='border-top:none;border-left:none'>Ayudant�a</td>
  <td class=xl76 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  31</td>
  <td class=xl78 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Funcional<br>
  AC05<br>
  Envio notas AC03 y C si hay ctrl</td>
  <td class=xl77 style='border-top:none;border-left:none'>33</td>
  <td class=xl75 style='border-top:none;border-left:none'>34</td>
  <td class=xl75 style='border-top:none;border-left:none'>35</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl76 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Renunion Ayudantes Docencia<br>
  36</td>
  <td class=xl76 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  37</td>
  <td class=xl76 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  38</td>
  <td class=xl78 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Metaclases<br>
  AC06<br>
  Envio notas AC04 y CX si hay ctrl</td>
  <td class=xl78 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T03<br>
  Entrega T02 a las 23:59<br>
  Envio notas T01</td>
  <td class=xl79 style='border-top:none;border-left:none'>41</td>
  <td class=xl79 style='border-top:none;border-left:none'>42</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl80 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  43</td>
  <td class=xl80 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  44</td>
  <td class=xl80 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  45</td>
  <td class=xl82 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Simulacion<br>
  AC07<br>
  Envio notas AC05 y CX si hay ctrl</td>
  <td class=xl81 style='border-top:none;border-left:none'>47</td>
  <td class=xl79 style='border-top:none;border-left:none'>48</td>
  <td class=xl79 style='border-top:none;border-left:none'>49</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl80 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  50</td>
  <td class=xl80 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  51</td>
  <td class=xl80 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  52</td>
  <td class=xl82 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Threading<br>
  AC08<br>
  Envio notas AC06 y CX si hay ctrl</td>
  <td class=xl82 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T04<br>
  Entrega T03 a las 23:59<br>
  Envio notas T02</td>
  <td class=xl83 style='border-top:none;border-left:none'>55</td>
  <td class=xl83 style='border-top:none;border-left:none'>56</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl84 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  57</td>
  <td class=xl84 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  58</td>
  <td class=xl84 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  59</td>
  <td class=xl86 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  GUI<br>
  AC09<br>
  Envio notas AC07 y CX si hay ctrl</td>
  <td class=xl85 style='border-top:none;border-left:none'>61</td>
  <td class=xl83 style='border-top:none;border-left:none'>62</td>
  <td class=xl83 style='border-top:none;border-left:none'>63</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl84 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  64</td>
  <td class=xl84 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  65</td>
  <td class=xl84 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  66</td>
  <td class=xl86 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Bytes, serial<br>
  AC10<br>
  Envio notas AC08 y CX si hay ctrl</td>
  <td class=xl86 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T05<br>
  Entrega T04 a las 23:59<br>
  Envio notas T03</td>
  <td class=xl87 style='border-top:none;border-left:none'>69</td>
  <td class=xl87 style='border-top:none;border-left:none'>70</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl88 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  71</td>
  <td class=xl88 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  72</td>
  <td class=xl88 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  73</td>
  <td class=xl90 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Networking<br>
  AC11<br>
  Envio notas AC09 y CX si hay ctrl</td>
  <td class=xl89 style='border-top:none;border-left:none'>75</td>
  <td class=xl87 style='border-top:none;border-left:none'>76</td>
  <td class=xl87 style='border-top:none;border-left:none'>77</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl88 width=233 style='height:54.0pt;border-top:none;
  width:175pt'>Reunion Ayudantes Docencia<br>
  78</td>
  <td class=xl88 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  79</td>
  <td class=xl88 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  80</td>
  <td class=xl90 width=233 style='border-top:none;border-left:none;width:175pt'>Clase
  Webservices<br>
  AC12<br>
  Envio notas AC10 y CX si hay ctrl</td>
  <td class=xl90 width=233 style='border-top:none;border-left:none;width:175pt'>Subir
  T06<br>
  Entrega T05 a las 23:59<br>
  Envio notas T04</td>
  <td class=xl91 style='border-top:none;border-left:none'>83</td>
  <td class=xl91 style='border-top:none;border-left:none'>84</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl92 width=233 style='height:54.0pt;border-top:none;
  width:175pt'><br>
  85</td>
  <td class=xl92 width=233 style='border-top:none;border-left:none;width:175pt'>Ayudant�a<br>
  86</td>
  <td class=xl93 style='border-top:none;border-left:none'>87</td>
  <td class=xl94 style='border-top:none;border-left:none'>Envio notas AC11 y CX
  si hay<span style='display:none'> ctrl</span></td>
  <td class=xl93 style='border-top:none;border-left:none'>89</td>
  <td class=xl91 style='border-top:none;border-left:none'>90</td>
  <td class=xl91 style='border-top:none;border-left:none'>91</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl93 style='height:54.0pt;border-top:none'>92</td>
  <td class=xl93 style='border-top:none;border-left:none'>93</td>
  <td class=xl92 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  94</td>
  <td class=xl94 style='border-top:none;border-left:none'>Envio notas AC12 y CX
  si hay<span style='display:none'> ctrl</span></td>
  <td class=xl95 width=233 style='border-top:none;border-left:none;width:175pt'>Entrega
  T06 a las 23:59<br>
  Envio notas T05</td>
  <td class=xl68 style='border-top:none;border-left:none'>97</td>
  <td class=xl68 style='border-top:none;border-left:none'>98</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl66 style='height:54.0pt;border-top:none'>99</td>
  <td class=xl66 style='border-top:none;border-left:none'>100</td>
  <td class=xl69 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  101</td>
  <td class=xl66 style='border-top:none;border-left:none'>102</td>
  <td class=xl66 style='border-top:none;border-left:none'>103</td>
  <td class=xl66 style='border-top:none;border-left:none'>104</td>
  <td class=xl66 style='border-top:none;border-left:none'>105</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl66 style='height:54.0pt;border-top:none'>106</td>
  <td class=xl66 style='border-top:none;border-left:none'>107</td>
  <td class=xl69 width=233 style='border-top:none;border-left:none;width:175pt'>Atenci�n
  Profesores<br>
  108</td>
  <td class=xl66 style='border-top:none;border-left:none'>109</td>
  <td class=xl96 style='border-top:none;border-left:none'>Envio notas T06</td>
  <td class=xl66 style='border-top:none;border-left:none'>111</td>
  <td class=xl66 style='border-top:none;border-left:none'>112</td>
 </tr>
 <tr height=72 style='mso-height-source:userset;height:54.0pt'>
  <td height=72 class=xl96 align=right style='height:54.0pt;border-top:none'>113</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>114</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>115</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>116</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>117</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>118</td>
  <td class=xl96 align=right style='border-top:none;border-left:none'>119</td>
 </tr>
</table>

</body>

</html>
