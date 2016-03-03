<html>
<head>
    <style type="text/css">
        body{
            width: 84mm !important;
            font-family: 'arabswell_1', 'KacstBook';
            font-size: 8pt;
            background-image: url(${'data:image/{1};base64,{0}'.format(*helper.get_logo_by_name('Card BG'))});
            background-repeat: no-repeat;
            background-size: 100%;
        }
        ${css}
        table{
            width: 100%;
            border-collapse: collapse;
        }
        td{
            vertical-align: top;
            padding: 1mm 2mm;
        }
    </style>
</head>
<body>
%for emp in objects :
    <table>
      <tr style="height:25mm;">
      </tr>
      <tr>
         <td style="width:30mm;">
             ${setLang('fr_FR') or ''}
             <br/><span style="font-size:larger;font-weight:bold;">${emp.givenname_latin.title() or ''} ${emp.surname_latin.upper() or ''}</span><br/>
             ${emp.job_id and emp.job_id.name or emp.grade_id and emp.grade_id.name.title() or ''}<br/>
         </td>
         <td style="width:8mm;"></td>
         <td style="width:20mm;" dir="rtl"><br/>
             ${setLang('ar_SY') or ''}
             <span style="font-weight:bold;">${emp.givenname or ''} ${emp.surname or ''}</span><br/>
             <span style="font-size:smaller;">
             ${emp.job_id and emp.job_id.name or emp.grade_id and emp.grade_id.name or ''}<br/>
             </span>
         </td>
         <td style="padding:1mm 0;">${helper.embed_image('png', emp.image_small)|safe}</td>
      </tr>
      <tr>
         <td></td>
         <td></td>
         <td dir="rtl" colspan="2">
             ر.ت &nbsp; &nbsp; &nbsp;: ${emp.employee_id or ''}<br/>
             ب.ت.و : ${emp.identification_id or ''}
         </td>
      </tr>
    </table>
    <p class="page-break"></p>
%endfor
</body>
</html>
