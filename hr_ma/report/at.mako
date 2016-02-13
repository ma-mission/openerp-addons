<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
%for emp in objects :
    <!-- % setLang(inv.partner_id.lang) % -->
    <!-- % setLang('ar_SY') % -->

    <h1>
        <span dir="rtl">شهادة العمل</span><br/>
        <span style="font-size:smaller;">ATTESTATION DE TRAVAIL</span>
    </h1>

    <p dir="rtl">يشهد رئيس جامعة الحسن الأول بسطات أن السيد(ة)</p>
    <p>Le Président de l'Université Hassan 1er de Settat atteste que Mr/Mme</p>

    <p>&nbsp;</p>

    <table class="spaced" width="100%">
      <tr>
         <td>Nom</td>
         <td>${emp.surname_latin or ''}</td>
         <td dir="rtl">${emp.surname or ''}</td>
         <td dir="rtl">الاسم العائلي</td>
      </tr>
      <tr>
         <td>Prénom</td>
         <td>${emp.givenname_latin or ''}</td>
         <td dir="rtl">${emp.givenname or ''}</td>
         <td dir="rtl">الاسم الشخصي</td>
      </tr>
      <tr>
         <td>N° CIN</td>
         <td colspan="2" align="center">${emp.identification_id or ''}</td>
         <td dir="rtl">رقم ب ت و</td>
      </tr>
      <tr>
         <td>N° PPR</td>
         <td colspan="2" align="center">${emp.employee_id or ''}</td>
         <td dir="rtl">رقم التأجير</td>
      </tr>
      <tr>
         <td>Grade</td>
         <td colspan="2" align="center">${emp.current_grade_id and emp.current_grade_id.grade_id and emp.current_grade_id.grade_id.name or ''}</td>
         <td dir="rtl">الإطار</td>
      </tr>
      <tr>
         <td>Lieu de Travail</td>
         <td colspan="2" align="center">${emp.work_location or ''}</td>
         <td dir="rtl">مقر العمل</td>
      </tr>
      <tr>
         <td colspan="2">Date d'affection dans l'administration publique</td>
         <td align="center">${emp.public_employment_date or ''}</td>
         <td dir="rtl">تاريخ ولوج الوظيفة العمومية</td>
      </tr>
    </table>

    <p>&nbsp;</p>
    <p dir="rtl">سلمت هذه الشهادة للمعني(ة) بالأمر بطلب منه(ها) للإدلاء بها واستعمالها على الوجه المشروع</p>
    <p>La présente attestation est délivrée à la demande de l'intéressé(e) pour servir et valoir ce que de droit</p>

    <p>&nbsp;</p>
    <div style="text-align:center;">Settat, le: &nbsp; ${time.strftime("%Y/%m/%d")} &nbsp; :حرر بسطات في</div>

    <p class="page-break"></p>
%endfor
</body>
</html>
