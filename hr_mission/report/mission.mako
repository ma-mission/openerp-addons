<html>
<head>
    <style type="text/css">
        ${css}
        table.mission td[dir="rtl"]{font-family: KacstOffice; font-size: 14pt;}
        table.mission tr{height:3em;}
    </style>
</head>
<body style="border:0; margin:400px 70 70px 100px;">
% for mission in objects:

    <h1>
        <span dir="rtl">تكليف بمهمة</span><br/>
        <span style="font-size:smaller;">Ordre de Mission</span>
    </h1>

    <table class="mission">
        <tr>
                <td  style="width:25%">Personnel de la mission:</td>
                <td style="text-align:center;">${', '.join(mission.employee_ids.name) or ""}</td>
                <td dir="rtl" style="width:25%">موظفو المهمة:</td>
        </tr>
        <tr>
                <td>Mission:</td>
                <td style="text-align:center">${mission.object or ""}</td>
                <td dir="rtl">المهمة:</td>
        </tr>
        <tr>
                <td>De se rendre à:</td>
                <td style="text-align:center"> ${mission.city_to.name or ""}</td>
                <td dir="rtl">سيتجهون إلى:</td>
        </tr>
        <tr>
                <td>Date de départ:</td>
                <td style="text-align:center">${mission.date_start or ""}</td>
                <td dir="rtl">تاريخ الذهاب:</td>
        </tr>
        <tr>
                <td>Date de retour:</td>
                <td style="text-align:center">${mission.date_end or ""}</td>
                <td dir="rtl">تاريخ الإياب:</td>
        </tr>
        <tr>
                <td>Moyen de transport:</td>
                <td style="text-align:center">
                    ${mission.get_transport(mission.transport) or ""}
                    % if mission.transport in  ('fleet', 'personal'):
                        - ${mission.car_immatriculation or ""} -
                    % endif
                </td>
                <td dir="rtl">وسيلة التنقل:</td>
        </tr>
        % if mission.transport == 'fleet':
        <tr>
                <td>Chaffeur:</td>
                <td style="text-align:center">${mission.driver_id.name or ""}</td>
                <td dir="rtl">السائق:</td>
        </tr>
        % endif
    </table>
    <br/><br/><br/>
    <div style="text-align:center">${company.partner_id.city or ""} le ${time.strftime("%d/%m/%Y")}</div>
    <p class="page-break"></p>
% endfor
</body>
</html>
