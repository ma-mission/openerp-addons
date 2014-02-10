<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for emp in objects :
    <!-- % setLang(inv.partner_id.lang) % -->
    <% setLang('ar_SY') %>
    <h1 style="text-align:center">
شهادة العمل<br/>
ATTESTATION DE TRAVAIL 
    </h1>

<div dir="rtl">يشهد رئيس جامعة الحسن الأول بسطات أن السيد(ة)</div><br/>
Le Président de l'Université Hassan 1er de Settat atteste que Mr/Mme:

    <table width="100%">
      <tr>
         <td>Nom</td>
         <td>${emp.surname_latin or ''}</td>
         <td align="right">${emp.surname or ''}</td>
         <td align="right">الاسم العائلي</td>
      </tr>
      <tr>
         <td>Prénom</td>
         <td>${emp.givenname_latin or ''}</td>
         <td align="right">${emp.givenname or ''}</td>
         <td align="right">الاسم الشخصي</td>
      </tr>
      <tr>
         <td>N° CIN</td>
         <td colspan="2" align="center">${emp.identification_id}</td>
         <td align="right">رقم ب.ت.و</td>
      </tr>
      <tr>
         <td>N° PPR</td>
         <td colspan="2" align="center">${emp.employee_id}</td>
         <td align="right">رقم التأجير</td>
      </tr>
      <tr>
         <td>Grade</td>
         <td>${emp.current_grade_id.grade_id.name}</td>
         <td align="right"></td>
         <td align="right">الإطار</td>
      </tr>
      <tr>
         <td>Lieu de Travail</td>
         <td>${emp.work_location}</td>
         <td align="right"></td>
         <td align="right">مقر العمل</td>
      </tr>
      <tr>
         <td colspan="2">Date d'affection dans l'administration publique</td>
         <td align="center">${emp.public_employment_date}</td>
         <td align="right">تاريخ ولوج الوظيفة العمومية</td>
      </tr>
    </table>

    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>
