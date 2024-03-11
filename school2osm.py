#!/usr/bin/env python3
# -*- coding: utf8

# school2osm
# Converts schools from Kunnskapsdirektoratet api feed to osm format for import/update
# Usage: python school2osm.py [output_filename.osm]
# Default output filename: "skoler.osm"


import urllib.request, urllib.error
import html
import json
import sys
import time
import os
import errno


version = "1.1.0"

transform_name = {
	'vgs': 'videregående skole',
	'VGS': 'videregående skole',
	'Vgs': 'videregående skole',
	'v.g.s.': 'videregående skole',
	'V.g.s.': 'videregående skole',
	'KVS': 'kristen videregående skole',
	'Kvs': 'kristen videregående skole',
	'Videregående': 'videregående',
	'Vidaregåande': 'vidaregåande',
	'Videregåande': 'vidaregåande',
	'Vidregående': 'videregående',
	'Vidregåande': 'vidaregåande',
	'Bibelskole': 'bibelskole',
	'Oppvekstsenter': 'oppvekstsenter',
	'Oppvekstområde': 'oppvekstområde',
	'Oppveksttun': 'oppveksttun',
	'Oppvekst': 'oppvekstsenter',
	'oppvekst': 'oppvekstsenter',
	'Oahppogald': 'oahppogald',
	'Grunnskoleundervisning': 'grunnskoleundervisning',
	'Grunnskolen': 'grunnskolen',
	'Grunnskole': 'grunnskole',
	'Grunnskoler': 'grunnskoler',
	'Grunnskole/adm': 'grunnskole',
	'Privatskole': 'privatskole',
	'Privatskule': 'privatskule',
	'Private': 'private',
	'Skolen': 'skolen',
	'Skoler': 'skolen',
	'Skole': 'skole',
	'Skule': 'skule',
	'Skuvle': 'skuvle',
	'Skuvla': 'skuvla',
	'Grunn-': 'grunn-',
	'Barne-': 'barne-',
	'Barne-Og': 'barne- og',
	'Barn': 'barn',
	'Ungdomsskole': 'ungdomsskole',
	'Ungdomsskule': 'ungdomsskule',
	'Undomsskule': 'ungdomsskule',
	'Ungdomssskole': 'ungdomsskole',
	'Ungdomstrinn': 'ungdomstrinn',
	'Ungdomstrinnet': 'ungdomstrinnet',
	'Ungdom': 'ungdomsskole',
	'Nærmiljøskole': 'nærmiljøskole',
	'Friskole': 'friskole',
	'Friskule': 'friskule',
	'Sentralskole': 'sentralskole',
	'Sentralskule': 'sentralskule',
	'Grendaskole': 'grendaskole',
	'Reindriftsskole': 'reindriftsskole',
	'Voksenopplæring': 'voksenopplæring',
	'Morsmålsopplæring': 'morsmålsopplæring',
	'Opplæring': 'opplæring',
	'10-Årige': '10-årige',
	'Utdanning': 'utdanning',
	'Kultursenter': 'kultursenter',
	'Kultur': 'kultur',
	'Flerbrukssenter': 'flerbrukssenter',
	'Kristne': 'kristne',
	'Skolesenter': 'skolesenter',
	'Læringssenter': 'læringssenter',
	'Senter': 'senter',
	'Fengsel': 'fengsel',
	'Tospråklig': 'tospråklig',
	'Flerspråklige': 'flerspråklige',
	'Alternative': 'alternative',
	'Tekniske': 'tekniske',
	'Maritime': 'maritime',
	'Offshore': 'offshore',
	'Omegn': 'omegn',
	'Åbarneskole': 'Å barneskole',
	'lurøy': 'Lurøy',
	'hasselvika': 'Hasselvika',
	'tjeldsund': 'Tjeldsund',
	'Kfskolen': 'KFskolen',
	'Davinvi': 'daVinci',
	'masi': 'Masi',
	'Rkk': 'RKK',
	'Aib': 'AIB',
	'(ais)': '(AIS)',
	'Awt': 'AWT',
	'Abr': 'ABR',
	'Fpg': 'FPG',
	'Oks': 'OKS',
	'De': 'de',
	'Cs': 'CS',
	'Ii': 'II',
	'S': 'skole',
	'St': 'St.',
	'Of': 'of',
	'Foreningen': '',
	'Skolelag': '',
	'Stiftelsen': '',
	'stiftelsen': '',
	'Stiftinga': '',
	'Studiested': '',
	'Skolested': '',
	'Avdeling': '',
	'Avd': '',
	'Avd.': '',
	'avd.': '',
	'AS': '',
	'As': '',
	'SA': '',
	'Sa': '',
	'BA': '',
	'Ba': '',
	'ANS': '',
	'Ans': ''
}

transform_names = {
	' og Barnehage': '',
	' og barnehage': '',
	' og Sfo': '',
	'Montessori skole': 'Montessoriskole',
	'oppvekstsenter skole': 'oppvekstsenter',
	'oppvekstsenter skule': 'oppvekstsenter',
	'Nordre Land kommune, ': '',
	'Salangen kommune, ': '',
	'Kvs-': 'Kristen videregående skole ',
	'Smi-': 'SMI-',
	'Ntg': 'NTG'
}

transform_operator = {
	'Sa': 'SA',
	'Vgs': 'vgs',
	'Suohkan': 'suohkan',
	'Gielda': 'gielda',
	'Tjïelte': 'tjïelte',
	'Tjielte': 'tjielte',
	'Oks': 'OKS'
}



# Produce a tag for OSM file

def make_osm_line (key,value):

	if value:
		encoded_key = html.escape(key)
		encoded_value = html.escape(value).strip()
		file.write ('    <tag k="%s" v="%s" />\n' % (encoded_key, encoded_value))



# Output message

def message (line):

	sys.stdout.write (line)
	sys.stdout.flush()



# Open file/api, try up to 5 times, each time with double sleep time

def try_urlopen (url):

	tries = 0
	while tries < 5:
		try:
			return urllib.request.urlopen(url)

		except OSError as e:  # Mostly "Connection reset by peer"
			if e.errno == errno.ECONNRESET:
				message ("\tRetry %i in %ss...\n" % (tries + 1, 5 * (2**tries)))
				time.sleep(5 * (2**tries))
				tries += 1			
	
	message ("\n\nError: %s\n" % e.reason)
	message ("%s\n\n" % url.get_full_url())
	sys.exit()



# Main program

if __name__ == '__main__':

	message ("Loading data ...")

	# Load earlier ref from old API (legacy ref)
	'''
	old_refs = {}

	url = "https://data-nsr.udir.no/enheter"
	file = urllib.request.urlopen(url)
	school_data = json.load(file)
	file.close()

	for school in school_data:
		if school['NSRId'] and school['OrgNr']:
			if school['OrgNr'] in old_refs:
				message ("%s %s already exists\n" % (school['OrgNr'], school['Navn']))
			else:
				old_refs[ school['OrgNr'] ] = school['NSRId']
	'''

	# Load basic information of all schools

	url = "https://data-nsr.udir.no/v3/enheter?sidenummer=1&antallPerSide=30000"
	file = urllib.request.urlopen(url)
	school_data = json.load(file)
	file.close()

	first_count = 0
	for school_entry in school_data['Enheter']:
		if (school_entry['ErAktiv'] == True
				and school_entry['ErSkole'] == True
				and (school_entry['ErGrunnskole'] == True or school_entry['ErVideregaaendeSkole'] == True)):
			first_count += 1

	message (" %s schools\n" % first_count)

	if school_data['AntallSider'] > 1:
		message ("*** Note: There are more data from API than loaded\n")

	# Get output filename

	filename = 'skoler.osm'
	
	if len(sys.argv) > 1:
		filename = sys.argv[1]

	file = open (filename, "w")

	# Produce OSM file header

	message ("Converting to file '%s' ...\n" % filename)

	file.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
	file.write ('<osm version="0.6" generator="schools2osm v%s" upload="false">\n' % version)

	node_id = -1000
	count = 0
	geocode = 0

	# Iterate all schools and produce OSM file

	for school_entry in school_data['Enheter']:

		if (school_entry['ErAktiv'] == True
				and school_entry['ErSkole'] == True
				and (school_entry['ErGrunnskole'] == True or school_entry['ErVideregaaendeSkole'] == True)):

			node_id -= 1
			count += 1

			message ("\r%i " % (first_count - count))

			# Load school details

			url = "https://data-nsr.udir.no/v3/enhet/" + str(school_entry['Orgnr'])
			school_file = try_urlopen(url)
			school = json.load(school_file)
			school_file.close()
#			time.sleep(1)

			# Fix school name

			name = school['Navn']
			original_name = name

			name = name.replace("/", " / ")

			if school['Karakteristikk']:
				original_name += ", " + school['Karakteristikk']
				if (school['Karakteristikk'].lower() not in
						["skole", "skule", "skolen", "skulen", "avd skule", "avd skole", "avd undervisning", "avdeling skole", "avdeling skule"]):
					name += ", " + school['Karakteristikk']

			if name == name.upper():
				name = name.title()

			name_split = name.split()
			name = ""
			for word in name_split:
				if word[-1] == ",":
					word_without_comma = word[:-1]
				else:
					word_without_comma = word
				if word_without_comma in transform_name:
					if transform_name[word_without_comma]:
						name += transform_name[word_without_comma]
				else:
					name += word
				if word[-1] == ",":
					name += ", "
				else:
					name += " "

			for words in transform_names:
				name = name.replace(words, transform_names[words])

			name = name[0].upper() + name[1:].replace(" ,", ",").replace(",,", ",").replace("  ", " ").strip("- ")

#			if school['Maalform'] == "Nynorsk":
#				name = name.replace("skole", "skule").replace("videregående", "vidaregåande")

			# Generate tags

			if school['Koordinat']:
				latitude = school['Koordinat']['Breddegrad']
				longitude = school['Koordinat']['Lengdegrad']
				if not(latitude or longitude):
					latitude = 0
					longitude = 0
			else:
				latitude = 0
				longitude = 0

			file.write ('  <node id="%i" lat="%s" lon="%s">\n' % (node_id, latitude, longitude))

			make_osm_line ("amenity", "school")
			make_osm_line ("ref:udir_nsr", str(school['Orgnr']))
			make_osm_line ("name", name)

#			if school['Orgnr'] in old_refs:
#				make_osm_line ("OLD_REF", str(old_refs[ school['Orgnr'] ]))

			if school['Epost']:
				make_osm_line ("email", school['Epost'].lower())

			if school['Url'] and not("@" in school['Url']):
				make_osm_line ("website", "https://" + school['Url'].lstrip("/").replace("www2.", "").replace("www.", "").replace(" ",""))

			if school['Telefon']:
				phone = school['Telefon'].replace("  ", " ")
				if phone:
					if phone[0] != "+":
						if phone[0:2] == "00":
							phone = "+" + phone[2:].lstrip()
						else:
							phone = "+47 " + phone
					make_osm_line ("phone", phone)

			if school['Elevtall']:
				make_osm_line ("capacity", str(school['Elevtall']))

			# Get school type

			isced = ""
			grade1 = ""
			grade2 = ""

			if school['SkoletrinnGSFra'] and school['SkoletrinnGSTil']:
				grade1 = school['SkoletrinnGSFra']
				grade2 = school['SkoletrinnGSTil']

			if school['SkoletrinnVGSFra'] and school['SkoletrinnVGSTil']:
				if not grade1:
					grade1 = school['SkoletrinnVGSFra']
				grade2 = school['SkoletrinnVGSTil']				

			if grade1 and grade2:
				if grade1 == grade2:
					make_osm_line ("grades", str(grade1))
				else:
					make_osm_line ("grades", str(grade1) + "-" + str(grade2))

				if grade1 <= 7:
					isced = "1"
				if grade1 <= 10 and grade2 >= 8:
					isced += ";2"
				if grade1 >= 11 or grade2 >= 11:
					isced += ";3"

			if not isced:
				if school['ErGrunnskole']:
					isced = "1;2"
				if school['ErVideregaaendeSkole']:
					isced += ";3"

			make_osm_line ("isced:level", isced.strip(";"))

			# Check for "Andre tjenester tilknyttet undervisning" code
			if any([code['Kode'] == "85.609" for code in school["Naeringskoder"]]):
				make_osm_line ("OTHER_SERVICES", "yes")

			# Get operator

			if school['ErOffentligSkole'] == True:
				make_osm_line ("operator:type", "public")
				make_osm_line ("fee", "no")
			elif school['ErPrivatskole'] == True:
				make_osm_line ("operator:type", "private")
				make_osm_line ("fee", "yes")

			for parent in school['ForeldreRelasjoner']:
				if parent['Relasjonstype']['Id'] == "1" and parent['Enhet']['Navn']:  # Owner

					operator_split = parent['Enhet']['Navn'].split()
					operator = ""
					for word in operator_split:
						if word in transform_operator:
							if transform_operator[word]:
								operator += transform_operator[word] + " "
						else:
							operator += word + " "

					operator = operator[0].upper() + operator[1:].replace("  ", " ").strip()
					make_osm_line ("operator", operator)

			# Generate extra tags for help during import

#			if school['GsiId'] != "0":
#				make_osm_line ("GSIID", school['GsiId'])

			if school['DatoFoedt']:
				make_osm_line ("DATE_CREATED", school['DatoFoedt'][0:10])

			make_osm_line ("DATE_UPDATED", school['DatoEndret'][0:10])
			make_osm_line ("MUNICIPALITY", school['Kommune']['Navn'])
			make_osm_line ("COUNTY", school['Fylke']['Navn'])
			make_osm_line ("DEPARTMENT", school['Karakteristikk'])
			make_osm_line ("LANGUAGE", school['Maalform']['Navn'])

			make_osm_line("ENTITY_CODES", "; ".join(["%i.%s" % (code['Prioritet'], code['Navn']) for code in school['Naeringskoder']]))
			make_osm_line("SCHOOL_CODES", str("; ".join([code['Navn'] for code in school['Skolekategorier']])))

			if school['ErSpesialskole'] == True:
				make_osm_line ("SPECIAL_NEEDS", "Spesialskole")

			if name != original_name:
				make_osm_line ("ORIGINAL_NAME", original_name)

			if school['Koordinat']:
				make_osm_line ("LOCATION_SOURCE", school['Koordinat']['GeoKilde'])

			address = school['Beliggenhetsadresse']
			if address:
				address_line = ""
				if address['Adresse'] and (address['Adresse'] != "-"):
					address_line = address['Adresse'] + ", "
				if address['Postnr']:
					address_line += address['Postnr'] + " "
				if address['Poststed']:
					address_line += address['Poststed']
				if address['Land'] and address['Land'] != "Norge":
					address_line += ", " + address['Land']
				if address_line:
					make_osm_line ("ADDRESS", address_line)

			if not (longitude or latitude):
				make_osm_line ("GEOCODE", "yes")
				geocode += 1

			# Done with OSM node

			file.write ('  </node>\n')

	# Produce OSM file footer

	file.write ('</osm>\n')
	file.close()

	message ("\r%i schools written to file\n" % count)
	message ("%i schools need geocoding\n\n" % geocode)
