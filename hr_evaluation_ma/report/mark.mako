<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        ${css}
	.simple_table{
	border: 1px solid black;
	border-collapse: collapse;
	}
	.simple_table th{
	border: 1px solid black;
	font-weight: normal;
	padding: 3px;
	}
	.simple_table td{
	border: 1px solid black;
	padding: 3px;
	}
	.box{
	display: inline-block;
	border: 1px solid black;
	text-align: center;
	width: 1.5em;
	height: 1.5em;
	margin-left: 3px;
	margin-right: 3px;
	}
	body{
	width: 960px;
	}
    </style>
</head>
<body>
    %for eval in objects :
    <!-- % emp = eval.employee_id % -->
    <!-- % setLang('ar_SY') % -->
    <h1 style="text-align:center" dir="rtl">
بطاقة التنقيط الفردية ${eval.year}<br/>
    </h1>
<!-- p>
 ${_("Marital Status")}
 ${_("Employee")}
 ${_("")}
 ${_("")}
</p -->

<!-- %
  import logging
  logger = logging.getLogger('Report')
  def getSelection(record, field):
      model = record._model
      lang = objects[0]._context['lang']
      record._context['lang'] = lang
      selection = model.fields_get(record._cr, record._uid, context=record._context)[field]['selection']
      key = record.__getattr__(field)
      return dict(selection)[key]
#% -->

<h2 dir="rtl">هوية الموظف<h2>

    <table width="100%" dir="rtl">
      <tr>
         <td align="right">الاسم العائلي</td>
         <td align="right">${eval.employee_id.surname or ''}</td>
         <td align="right">رقـم التأجيـر</td>
         <td align="right">${eval.employee_id.employee_id or ''}</td>
      </tr>
      <tr>
         <td align="right">الاسم الشخصي</td>
         <td align="right">${eval.employee_id.givenname or ''}</td>
         <td align="right">رقم ب.ت.و</td>
         <td align="right">${eval.employee_id.identification_id}</td>
      </tr>
      <tr>
         <td align="right">تاريخ الازديـاد</td>
         <td align="right">${eval.employee_id.birthday}</td>
         <td align="right">مكان الازديـاد</td>
         <td align="right">${eval.employee_id.birthplace}</td>
      </tr>
      <tr>
         <td align="right">العنــــوان</td>
         <td align="right">${eval.employee_id.address_home_id.street} , ${eval.employee_id.address_home_id.city}</td>
      </tr>
      <tr>
         <td align="right">الحالـة العائليـــة</td>
         <td align="right"><!-- get translated value of the selection field -->
             % for selection in helper.pool['hr.employee'].fields_get(
                     helper.cursor, helper.uid,
                     allfields=['marital'],
                     context={'lang':lang}
                     )['marital']['selection']:
                 % if selection[0] == eval.employee_id.marital:
                     ${selection[1]}
                 % endif
             % endfor
         </td>
         <td align="right">عـدد الأطفال</td>
         <td align="right">${eval.employee_id.children}</td>
      </tr>
      <tr>
         <td align="right">الدرجة ومقـر التعيين</td>
         <td>${eval.grade_id.grade_id.name}</td>
         <td align="right" colspan="2">بــ${eval.employee_id.work_location}</td>
      </tr>
      <tr>
         <td align="right">تاريخ التعيين في الدرجة</td>
         <td align="right">${eval.grade_start}</td>
      </tr>
      <tr>
         <td align="right">الرتبــة والأقدميــة</td>
         <td align="right">${eval.grade_id.echelon}</td>
         <td align="right">منذ</td>
         <td align="right">${eval.grade_id.date_start}</td>
      </tr>
      <tr>
         <td align="right">تاريـخ ولـوج الإدارة</td>
         <td align="right">${eval.employee_id.public_employment_date}</td>
      </tr>
      <tr>
         <td align="right">الوظيفة المزاولة حاليا</td>
         <td align="right">${eval.employee_id.job_id.name}</td>
         <td align="right">منذ</td>
         <td align="right">${eval.employee_id.job_start_date}</td>
      </tr>
    </table>


<h2 dir="rtl">النقطة الممنوحة<h2>


    <table width="100%" class="simple_table" dir="rtl">
        <thead>
	    <tr>
	        <th>عناصر التنقيط</th>
	        <th>سلم التنقيط</th>
	        <th>النقطة الممنوحة</th>
	        <th width="35%">ملاحظات</th>
	    </tr>
	</thead>
	<tbody>
	    <tr>
	        <td>
إنجاز المهام المرتبطة بالوظيفة
                </td>
                <td align="center">
من 0 إلى 5
                </td>
                <td align="center">${eval.work_eval}</td>
                <td></td>
            </tr>
	    <tr>
	        <td>
المردودية
                </td>
                <td align="center">
من 0 إلى 5
                </td>
                <td align="center">${eval.productivity_eval}</td>
                <td></td>
            </tr>
	    <tr>
	        <td>
القدرة على التنظيم
                </td>
                <td align="center">
من 0 إلى 3
                </td>
                <td align="center">${eval.organization_eval}</td>
                <td></td>
            </tr>
	    <tr>
	        <td>
السلوك المهني
                </td>
                <td align="center">
من 0 إلى 4
                </td>
                <td align="center">${eval.conduct_eval}</td>
                <td></td>
            </tr>
	    <tr>
	        <td>
البحث والابتكار
                </td>
                <td align="center">
من 0 إلى 3
                </td>
                <td align="center">${eval.innovation_eval}</td>
                <td></td>
            </tr>
	    <tr>
	        <td>
مجموع النقط الجزئية
                </td>
                <td align="center">
من 0 إلى 20
                </td>
                <td align="center">${eval.sum}</td>
                <td></td>
            </tr>
	</tbody>
    </table>

<h2 dir="rtl">الميزة الممنوحة</h2>

    <table width="100%" dir="rtl">
        <tr>
	    <td width="20%"><span class="box">${eval.mark == 'E' and 'X' or ' '}</span>ممتاز</td>
	    <td width="20%"><span class="box">${eval.mark == 'V' and 'X' or ' '}</span>جيد جدا</td>
	    <td width="20%"><span class="box">${eval.mark == 'G' and 'X' or ' '}</span>جيد</td>
	    <td width="20%"><span class="box">${eval.mark == 'A' and 'X' or ' '}</span>متوسط</td>
	    <td width="20%"><span class="box">${eval.mark == 'W' and 'X' or ' '}</span>ضعيف</td>
	</tr>
	<tr>
	    <td>18-20</td>
	    <td>16-18</td>
	    <td>14-16</td>
	    <td>10-14</td>
	    <td>0-10</td>
	</tr>
    </table>

<h2 dir="rtl">نسق الترقية في الرتبة</h2>

    <table width="100%" dir="rtl">
        <tr>
	    <td width="33%"><span class="box">${eval.grade_id.advancement_pace == 'F' and 'X' or ' '}</span>سريع</td>
	    <td width="33%"><span class="box">${eval.grade_id.advancement_pace == 'M' and 'X' or ' '}</span>متوسط</td>
	    <td width="33%"><span class="box">${eval.grade_id.advancement_pace == 'S' and 'X' or ' '}</span>بطيء</td>
	</tr>
	<tr>
	    <td>16-20</td>
	    <td>10-16</td>
	    <td>0-10</td>
	</tr>
    </table>

<div dir="rtl">
</div><br/>

    <p class="page-break"></p>
    %endfor
</body>
</html>
