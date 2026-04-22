from django.shortcuts import render


def home(request):
	context = {
	}
	return render(request, 'home.html', context)

def faqs(request):
	faqs = [
		{
			'pregunta': "Què és Trupiessu?",
			'resposta': "Trupiessu és el nostre vi ecològic d'elaboració pròpia, elaborat amb les millors varietats de raïm i seguint pràctiques sostenibles per oferir-te un vi de qualitat excepcional."
		},
		{
			'pregunta': "Quins tipus de vins oferiu?",
			'resposta': "Oferim una àmplia selecció de vins, incloent vins negres, blancs, rosats i escumosos de diverses regions vinícoles."
		},
		{
			'pregunta': "Com puc fer una comanda?",
			'resposta': "Per fer una comanda, simplement navega pel nostre catàleg de vins, selecciona els que t’interessen i afegeix-los al carret. Un cop hagis acabat, segueix el procés de compra per completar la teva comanda."
		},
		{
			'pregunta': "Quins mètodes de pagament accepteu?",
			'resposta': "Acceptem diversos mètodes de pagament, incloent targetes de crèdit, PayPal i transferències bancàries. Pots triar el mètode que millor s’adapti a les teves necessitats durant el procés de compra."
		},
		{
			'pregunta': "Quins són els terminis de lliurament?",
			'resposta': "Els terminis de lliurament varien segons la ubicació i la disponibilitat dels vins. Normalment, les comandes es lliuren en un termini de 3 a 5 dies hàbils. Rebràs una notificació amb els detalls del lliurament un cop la teva comanda hagi estat processada."
		},
		{
			'pregunta': "Puc retornar un producte?",
			'resposta': "Sí, acceptem devolucions dins dels 14 dies posteriors a la recepció de la comanda. Els productes han d’estar en les mateixes condicions en què els vas rebre. Per iniciar una devolució, contacta amb el nostre servei d’atenció al client amb els detalls de la comanda i el motiu de la devolució."
		},
		{
			'pregunta': "Té algun cost per fer una devolució?",
			'resposta': "No, les devolucions són gratuïtes per a tots els clients. Només has de contactar amb el nostre servei d’atenció al client per iniciar el procés."
		},
		{
			'pregunta': "Com puc contactar amb el servei d’atenció al client?",
			'resposta': "Pots contactar amb el nostre servei d’atenció al client a través del formulari de contacte disponible al final de la pàgina o enviando un correu electrònic a client@trupiessu.com."
		}
	]
	context = {
		'faqs': faqs
	}
	return render(request, 'faqs/faqs.html', context)