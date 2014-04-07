<html>
<head>
<style type="text/css">
table{width:100%;max-width:100%;border-collapse:collapse;font-family:arial;font-size:8pt;}
tr{min-height:1cm;height:auto;}
th, td{border:1px solid #000;text-align:center;}
th{height:1cm;}
table.borderless td{border:0}
${css}
</style>
</head>
<body>
%for ps in objects:

<p style="float:left;">
Etat du salaire du ${ps.date_start} au ${ps.date_end}
</p>

<table style="width:30%;height:2cm;margin-right:0;margin-left:auto;">
  <tr>
    <th>N C.I.N</th>
    <th>N P.P.R</th>
  </tr>
  <tr>
    <td>${ps.employee_id.identification_id}</td>
    <td>${ps.employee_id.employee_id}</td>
  </tr>
</table>

<table class="fullwidth basic_table" style="height:3cm">
  <tr>
    <th>NOM PRENOM ET GRADE</th>
    <th>IMPUTATION ET RESIDENCE</th>
  </tr>
  <tr>
    <td>${ps.employee_id.name}<br/>${ps.employee_id.current_grade_id.grade_id.name}</td>
    <td>${ps.chapter_id.name}<br/>${ps.residence_id.name}</td>
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
    <td>${ps.employee_id.birthday}</td>
    <td>${ps.employee_id.public_employment_date}</td>
    <td></td>
    <td>${ps.employee_id.current_grade_id.echelon}</td>
    <td>${ps.employee_id.current_grade_id.index}</td>
    <%
    def genderCode(g):
        if g=='male':
            return 'M'
        elif g=='female':
            return 'F'
        else:
            return ''
    %>
    <td>${ps.employee_id.gender | genderCode}</td>
    <td>${ps.employee_id.country_id.code}</td>
    <td>${ps.marital_status}</td>
    <td>${ps.children_number}</td>
    <td>${ps.deduction_rate}</td>
  </tr>
</table>

<table style="height:4cm">
  <tr>
    <th>EMOLUMENTS BRUTS ANNUELS</th>
    <th>RETENUES ANNUELLES</th>
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
    <th>BRUT ANNUEL</th>
    <th>TOTAL RETENUES</th>
    <th>NET ANNUEL</th>
    <th>NET MENSUEL</th>
  </tr>
  <tr>
    <td>${ps.total_allowances}</td>
    <td>${ps.total_deductions}</td>
    <td>${ps.net_annual}</td>
    <td>${ps.net_monthly}</td>
  </tr>
</table>

<p>Settat, le ${'%d/%m/%Y' | time.strftime}</p>

<p style="page-break-after:always">&nbsp;</p>
%endfor
</body>
</html>
