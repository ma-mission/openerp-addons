<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title></title>
	<meta name="generator" content="LibreOffice 4.2.7.2 (Linux)">
	<meta name="author" content="User">
	<meta name="created" content="20160119;103700000000000">
	<meta name="changedby" content="CUTI">
	<meta name="changed" content="20160119;103700000000000">
	<meta name="AppVersion" content="12.0000">
	<meta name="Company" content="DOMICILE">
	<meta name="DocSecurity" content="0">
	<meta name="HyperlinksChanged" content="false">
	<meta name="LinksUpToDate" content="false">
	<meta name="ScaleCrop" content="false">
	<meta name="ShareDoc" content="false">
	<style type="text/css">
	<!--
	${css}
		@page { margin-left: 2.5cm; margin-right: 2.5cm; margin-top: 1.25cm; margin-bottom: 2.5cm }
		p { margin-bottom: 0.25cm; direction: ltr; line-height: 120%; text-align: left; widows: 2; orphans: 2 }
		p.western { font-family: "Times New Roman", serif; font-size: 10pt }
		p.cjk { font-family: "Times New Roman"; font-size: 10pt; so-language: fr-FR }
		p.ctl { font-family: "Times New Roman"; font-size: 10pt }
	-->
	</style>
</head>
<body lang="fr-FR" dir="ltr">
%for sortiefourniture in objects:

<h1>DECHARGE FOURNITURE DE BUREAU </h1>

<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><font size="3" style="font-size: 12pt">Commandé
par Nom et prénom&nbsp;: ${sortiefourniture.employee_id.name}</font>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><font size="3" style="font-size: 12pt">Service&nbsp;:	${sortiefourniture.employee_id.department_id.name}</font></p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><font size="3" style="font-size: 12pt">Atteste
avoir reçu le(s) matériel(s) désigné ci-dessous&nbsp;:</font></p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<table width="650" cellpadding="7" cellspacing="0">
	<col width="217">
	<col width="61">
	<col width="121">
	<col width="193">
	<tr>
		<td width="217" height="36" style="border: 1px solid #000001; padding-top: 0cm; padding-bottom: 0cm; padding-left: 0.2cm; padding-right: 0.19cm">
			<p class="western" align="center"><font size="3" style="font-size: 12pt"><b>Désignation</b></font></p>
		</td>
		
		<td width="193" style="border-top: 1px solid #000001; border-bottom: 1px solid #000001; border-left: 1px solid #00000a; border-right: 1px solid #000001; padding-top: 0cm; padding-bottom: 0cm; padding-left: 0.2cm; padding-right: 0.19cm">
			<p class="western" align="center"><font size="3" style="font-size: 12pt"><b>Quantité</b></font></p>
		</td>
	</tr>
	%for fourniture_ligne in sortiefourniture.ligne_ids:
	<tr valign="top">
		<td width="217" height="60" style="border: 1px solid #000001; padding-top: 0cm; padding-bottom: 0cm; padding-left: 0.2cm; padding-right: 0.19cm">
			<p class="western" align="center">${fourniture_ligne.fourniture_id.name}
			</p>
		</td>
		<td width="61" style="border: 1px solid #000001; padding-top: 0cm; padding-bottom: 0cm; padding-left: 0.2cm; padding-right: 0.19cm">
			<p class="western" align="center">${fourniture_ligne.qte}
			</p>
		</td>
				
	</tr>
	%endfor
</table>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%">	Date&nbsp;:${sortiefourniture.date}
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><font size="3" style="font-size: 12pt">Signature de l’intéressé</font>
</p>

<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>
<p class="western" style="margin-bottom: 0cm; line-height: 100%"><br>
</p>

%endfor
</body>
</html>