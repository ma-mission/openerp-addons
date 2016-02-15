<!DOCTYPE html>
<html>
<head>
<style type="text/css">
${css}
table{width:100%;max-width:100%;border-collapse:collapse;font-family:"Liberation Sans";margin-bottom:1em;}
tr{min-height:1cm;height:auto;}
th, td{border:1px solid #000;text-align:center;}
th{height:1cm;}
table.borderless td{border:0}
.col-8{width:66%}
.col-6{width:50%}
.col-3{width:25%}
.col-4{width:33%}
.col-2{width:33%}
table.t3cm{height:3cm;}
table.t3cm th,
table.t3cm th{
font-size:8pt;
}
/*
.row{clear:both;
width:948px;}
.col{width:70px;padding:0 4px;float:left;border-right: 1px solid black;}
.col10{width:781px;padding:0 4px;float:left;border-right: 1px solid black;}
*/
body {
	margin: 0;
	padding: 0;
	width:960px;
}
.row{
clear:both;
width:960px;
/*
margin-left: -10px;
margin-right: -10px;
*/
}
.row .first{padding-left: 0;}
.row .last{padding-right: 0;}
.col,
.col4,
.col8,
.col10
{
box-sizing:border-box;
float:left;
padding: 0 10px;
}
/*
border-right: 1px solid;
border-left: 1px hidden;border-right: 1px solid;margin-left:-1px;}
*/
.col{width:80px;}
.col4{width:320px;}
.col8{width:640px;}
.col10{width:800px;}
.col12{width:960px;}
</style>
</head>
<body>
%for ps in objects:

<h1>Attestation de Salaire</h1>

<div class="row">

<p class="col8 first" style="font-size:larger;">
Le président de l'Université Hassan 1er de Settat atteste que les émoulements ci-dessous sont servis à compter du ${ps.date_start} au ${ps.date_end} sur la base de données fournie par le D.R.P.P:
</p>

<!--
<table style="width:30%;height:2cm;margin-right:0;margin-left:auto;">
-->
<table class="col4 last" style="height:3cm;">
  <tr>
    <th>N C.I.N</th>
    <th>N P.P.R</th>
  </tr>
  <tr>
    <td>${ps.employee_id.identification_id}</td>
    <td>${ps.employee_id.employee_id}</td>
  </tr>
</table>
</div>

<table style="height:3cm">
  <tr>
    <th>Nom Prenom et Grade</th>
    <th>Imputation et Résidence</th>
  </tr>
  <tr>
    <td>${ps.employee_id.name}<br/>${ps.employee_grade_id.grade_id.name}</td>
    <td>${ps.chapter_id.name}<br/>${ps.residence_id.name}</td>
  </tr>
</table>

<table class="t3cm" style="height:3cm">
  <tr style="font-size:normal;">
    <th>Date de naissance</th>
    <th>Date de recrutement</th>
    <th>Echelle</th>
    <th>Echelon</th>
    <th>Indice</th>
    <th>Sexe</th>
    <th>Nationalité</th>
    <th>Situation<br/>matrimoniale</th>
    <th>Nombre<br/>d'enfants</th>
    <th>Déduction</th>
  </tr>
  <tr style="font-size:smaller;">
    <td>${ps.employee_id.birthday}</td>
    <td>${ps.employee_id.public_employment_date}</td>
    <td></td>
    <td>${ps.employee_grade_id.echelon}</td>
    <td>${ps.employee_grade_id.index}</td>
    <td>${ps.employee_id.gender == 'male' and 'M' or ''}${ps.employee_id.gender == 'female' and 'F' or ''}</td>
    <td>${ps.nationality}</td>
    <td>${ps.marital_status}</td>
    <td>${ps.children_number}</td>
    <td>${ps.deduction_rate}</td>
  </tr>
</table>

<table style="height:4cm">
  <tr>
    <th class="col-6">EMOLUMENTS BRUTS ANNUELS</th>
    <th class="col-6">RETENUES ANNUELLES</th>
  </tr>
  <tr>
    <td style="vertical-align:top;">
      <table class="borderless">
      %for line in ps.line_ids:
        %if line.salary_rule_id.positive:
	  <tr>
	    <td style="text-align:left;">
            ${line.salary_rule_id.name}
	    </td>
	    <td style="text-align:right;">
            ${line.amount}
	    </td>
	  </tr>
        %endif
      %endfor
      </table>
    </td>
    <td style="vertical-align:top;">
      <table class="borderless">
      %for line in ps.line_ids:
        %if not line.salary_rule_id.positive:
	  <tr>
	    <td style="text-align:left;">
            ${line.salary_rule_id.name}
	    </td>
	    <td style="text-align:right;">
            ${line.amount}
	    </td>
	  </tr>
        %endif
      %endfor
      </table>
    </td>
  </tr>
</table>

<table style="height:2cm">
  <tr>
    <th class="col-3">BRUT ANNUEL</th>
    <th class="col-3">TOTAL RETENUES</th>
    <th class="col-3">NET ANNUEL</th>
    <th class="col-3">NET MENSUEL</th>
  </tr>
  <tr>
    <td>${ps.total_allowances}</td>
    <td>${ps.total_deductions}</td>
    <td>${ps.net_annual}</td>
    <td>${ps.net_monthly}</td>
  </tr>
</table>

<p style="float:right;">Settat, le ${time.strftime("%d/%m/%Y")}</p>

<p class="page-break"></p>
%endfor
</body>
</html>
