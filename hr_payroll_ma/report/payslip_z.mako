<html>
<head>
<style type="text/css">
table{width:100%;max-width:100%;border-collapse:collapse;font-family:arial;font-size:8pt;}
tr{min-height:1cm;height:auto;}
th, td{border:1px solid #000;text-align:center;}
th{height:1cm;}
${css}
</style>
</head>
<body>
%for ps in objects:

<table style="width:30%;height:2cm;float:right;">
  <tr>
    <th>N C.I.N</th>
    <th>N P.P.R</th>
  </tr>
  <tr>
    <td>${ps.employee_id.identification_id}</td>
    <td>--</td>
  </tr>
</table>

<table class="fullwidth basic_table" style="height:3cm">
  <tr>
    <th>NOM PRENOM ET GRADE</th>
    <th>IMPUTATION ET RESIDENCE</th>
  </tr>
  <tr>
    <td>${ps.employee_id.name}<br/>--Grade--</td>
    <td>----</td>
  </tr>
</table>

<table style="height:3cm">
  <tr>
    <th>DATE DE NAISSANCE</th>
    <th>DATE DE RECRUTEMENT</th>
    <th>Echelle</th>
    <th>Echelon</th>
    <th>Indice</th>
    <th>Sexe</th>
    <th>NATIONALITE</th>
    <th>SITUATION MATRIMONIALE</th>
    <th>NOMBRE ENFANTS</th>
    <th>DEDUCTION</th>
  </tr>
  <tr>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
  </tr>
</table>

<table style="height:4cm">
  <tr>
    <th>EMOLUMENTS BRUTS ANNUELS</th>
    <th>RETENUES ANNUELLES</th>
  </tr>
  <tr>
    <td>
      %for line in ps.line_ids:
        ${line.salary_rule_id.name} - ${line.amount}<br/>
      %endfor
x<br/>
x<br/>
x<br/>
x<br/>
x<br/>
x<br/>
x<br/>
x<br/>
x<br/>
    </td>
    <td>----</td>
  </tr>
</table>

<table style="height:2cm">
  <tr>
    <th>BRUT ANNUEL</th>
    <th>TOTAL RETENUES</th>
    <th>NET ANNUEL</th>
    <th>NET MENSUEL</th>
  </tr>
  <tr>
    <td>----</td>
    <td>----</td>
    <td>----</td>
    <td>----</td>
  </tr>
</table>

<p style="page-break-after:always"></p>
%endfor
</body>
</html>
