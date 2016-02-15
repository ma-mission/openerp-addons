<html>
<head>
	<style>
	${css}
	table.full{width:100%;border-collapse: collapse;}
	table.with-borders td,
	table.with-borders th{
		border:1px solid black;
	}
	td.label{border-right:1px solid black;width:20%;}
	</style>
</head>
<body>
%for piece in objects:
	<h1>Informations sur la pièce</h1>
	<p><br/></p>
	<table class="full">
		<tr>
			<td class="label">Numéro</td><td>${piece.name}</td>
		</tr>
		<tr>
			<td class="label">Superficie</td><td>${piece.superficie}</td>
		</tr>
		<tr>
			<td class="label">Batiment</td><td>${piece.batiment_id.name}</td>
		</tr>
		<tr>
			<td class="label">Etage</td><td>${piece.etage}</td>
		</tr>
		<tr>
			<td class="label">Etablissement</td><td>${piece.batiment_id.company_id.name}</td>
		</tr>
	</table>
	
	<p style="font-size:larger;font-weight:bold;">Articles</p>
	<table class="full with-borders">
	%for employe in piece.employee_ids:
		<tr>
			<td>${employe.name}</td>
			<td>
				<table class="full with-borders">
					<tr>
						<th>Désignation</th><th>N° Inventaire</th><th>N° Série</th>
					</tr>
				%for article in employe.article_ids:
					<tr>
						<td>${article.name}</td>
						<td>${article.num_inv}</td>
						<td>${article.num_serie}</td>
					</tr>
				%endfor
				</table>
			</td>
		</tr>
	%endfor
	</table>
	
%endfor
</body>
</html>