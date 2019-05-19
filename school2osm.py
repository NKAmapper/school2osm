#!/usr/bin/env python
# -*- coding: utf8

# school2osm
# Converts schools from Kunnskapsdirektoratet api feed to osm format for import/update
# Usage: python school2osm.py [output_filename.osm]
# Default output filename: "skoler.osm"


import urllib2
import cgi
import csv
import json
import sys


version = "0.3.0"

transform_name = {
	'vgs': u'videregående skole',
	'VGS': u'videregående skole',
	'Vgs': u'videregående skole',
	'v.g.s.': u'videregående skole',
	'V.g.s.': u'videregående skole',
	'KVS': u'kristen videregående skole',
	'Kvs': u'kristen videregående skole',
	u'Videregående': u'videregående',
	u'Vidaregåande': u'vidaregåande',
	u'Videregåande': u'vidaregåande',
	u'Vidregående': u'videregående',
	u'Vidregåande': u'vidaregåande',
	'Bibelskole': 'bibelskole',
	'Oppvekstsenter': 'oppvekstsenter',
	u'Oppvekstområde': u'oppvekstområde',
	'Oppveksttun': 'oppveksttun',
	'Oppvekst': 'oppvekstsenter',
	'oppvekst': 'oppvekstsenter',
	'Oahppogaldu': 'oahppogaldu',
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
	u'Nærmiljøskole': u'nærmiljøskole',
	'Friskole': 'friskole',
	'Friskule': 'friskule',
	'Sentralskole': 'sentralskole',
	'Sentralskule': 'sentralskule',
	'Grendaskole': 'grendaskole',
	'Reindriftsskole': 'reindriftsskole',
	u'Voksenopplæring': u'voksenopplæring',
	u'Morsmålsopplæring': u'morsmålsopplæring',
	u'Opplæring': u'opplæring',
	u'10-Årige': u'10-årige',
	'Utdanning': 'utdanning',
	'Kultursenter': 'kultursenter',
	'Kultur': 'kultur',
	'Flerbrukssenter': 'flerbrukssenter',
	'Kristne': 'kristne',
	'Skolesenter': 'skolesenter',
	u'Læringssenter': u'læringssenter',
	'Senter': 'senter',
	'Fengsel': 'fengsel',
	u'Tospråklig': u'tospråklig',
	u'Flerspråklige': u'flerspråklige',
	'Alternative': 'alternative',
	'Tekniske': 'tekniske',
	'Maritime': 'maritime',
	'Offshore': 'offshore',
	'Omegn': 'omegn',
	u'Åbarneskole': u'Å barneskole',
	u'lurøy': u'Lurøy',
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
	'De': 'de',
	'Cs': 'CS',
	'Ii': 'II',
	'S': 'skole',
	'St': 'St.',
	'Of': 'of',
	'Foreningen': '',
	'Skolelag': '',
	'Stiftelsen': '',
	'Studiested': '',
	'Avdeling': '',
	'Avd': '',
	'Avd.': '',
	'avd.': '',
	'AS': '',
	'As': '',
	'Sa': ''
}

transform_names = {
	' og Barnehage': '',
	'Montessori skole': 'Montessoriskole',
	'oppvekstsenter skole': 'oppvekstsenter',
	'oppvekstsenter skule': 'oppvekstsenter',
	'Nordre Land kommune, ': '',
	'Salangen kommune, ': '',
	'Kvs-': u'Kristen videregående skole ',
	'Ntg': 'NTG'
}

transform_operator = {
	'Sa': 'SA',
	'Vgs': 'vgs',
	'Suohkan': 'suohkan',
	'Gielda': 'gielda',
	u'Tjïelte': u'tjïelte',
	'Tjielte': 'tjielte'
}


# Produce a tag for OSM file

def make_osm_line (key,value):

	if value:
		encoded_key = cgi.escape(key.encode('utf-8'),True)
		encoded_value = cgi.escape(value.encode('utf-8'),True).strip()
		file.write ('    <tag k="%s" v="%s" />\n' % (encoded_key, encoded_value))


# Output message

def message (line):

	sys.stdout.write (line)
	sys.stdout.flush()


# Main program

if __name__ == '__main__':

	# Load basic information of all schools

	message ("Reading data ...")

	url = "https://data-nsr.udir.no/enheter"
	file = urllib2.urlopen(url)
	school_data = json.load(file)
	file.close()

	first_count = 0
	for school_entry in school_data:
		if (school_entry['ErAktiv'] == True) and (school_entry['ErSkole'] == True) and (school_entry['VisesPaaWeb'] == True) and \
			 ((school_entry['ErGrunnSkole'] == True) or (school_entry['ErVideregaaendeSkole'] == True)):
			first_count += 1

	message (" %s schools\n" % first_count)

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

	# Iterate all schools and produce OSM file

	for school_entry in school_data:

		if (school_entry['ErAktiv'] == True) and (school_entry['ErSkole'] == True) and (school_entry['VisesPaaWeb'] == True) and \
			 ((school_entry['ErGrunnSkole'] == True) or (school_entry['ErVideregaaendeSkole'] == True)):

			node_id -= 1
			count += 1

			message ("\r%i " % (first_count - count))

			# Load school details

			url = "https://data-nsr.udir.no/enhet/" + str(school_entry['NSRId'])
			school_file = urllib2.urlopen(url)
			school = json.load(school_file)
			school_file.close()

			# Fix school name

			name = school['Navn']
			original_name = name

			name = name.replace("/", " / ")

			if school['Karakteristikk']:
				original_name += ", " + school['Karakteristikk']
			 	if not(school['Karakteristikk'].lower() in \
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
#				name = name.replace("skole", "skule").replace(u"videregående", u"vidaregåande")

			# Generate tags

			if school['Koordinater']:
				latitude = school['Koordinater']['Breddegrad']
				longitude = school['Koordinater']['Lengdegrad']
				if not(latitude or longitude):
					latitude = 0
					longitude = 0
			else:
				latitude = 0
				longitude = 0

			file.write ('  <node id="%i" lat="%s" lon="%s">\n' % (node_id, latitude, longitude))

			make_osm_line ("amenity", "school")
			make_osm_line ("ref:udir_nsr", str(school['NSRId']))
			make_osm_line ("name", name)
			make_osm_line ("email", school['Epost'].lower())

			if school['Url'] and not("@" in school['Url']):
				make_osm_line ("website", "http://" + school['Url'].lstrip("/").replace("www2.", "").replace("www.", "").replace(" ",""))

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
			if school['SkoleTrinnFra'] and school['SkoleTrinnTil']:
				if school['SkoleTrinnFra'] == school['SkoleTrinnTil']:
					make_osm_line ("grades", str(school['SkoleTrinnFra']))
				else:
					make_osm_line ("grades", str(school['SkoleTrinnFra']) + "-" + str(school['SkoleTrinnTil']))

				if school['SkoleTrinnFra'] <= 7:
					isced = "1"
				if (school['SkoleTrinnFra'] <= 10) and (school['SkoleTrinnTil'] >= 8):
					isced += ";2"
				if (school['SkoleTrinnFra'] >= 11) or (school['SkoleTrinnTil'] >= 11):
					isced += ";3"

			if not(isced):
				if school['ErGrunnSkole']:
					isced = "1;2"
				if school['ErVideregaaendeSkole']:
					isced += ";3"

			make_osm_line ("isced:level", isced.strip(";"))

			# Get operator

			if school['ErOffentligSkole'] == True:
				make_osm_line ("operator:type", "public")
				make_osm_line ("fee", "no")
			if school['ErPrivatSkole'] == True:
				make_osm_line ("operator:type", "private")
				make_osm_line ("fee", "yes")

			for parent in school['ParentRelasjoner']:
				if (parent['RelasjonsType']['Id'] == "1") and parent['Enhet']['Navn']:  # Owner

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

			if school['GsiId'] != "0":
				make_osm_line ("GSIID", school['GsiId'])

			make_osm_line ("LANGUAGE", school['Maalform'])
			make_osm_line ("DATE_CREATED", school['OpprettetDato'][0:10])
			make_osm_line ("DATE_UPDATED", school['SistEndretDato'][0:10])
			make_osm_line ("MUNICIPALITY", school['Kommune']['Navn'])
			make_osm_line ("COUNTY", school['Fylke']['Navn'])
			make_osm_line ("DEPARTMENT", school['Karakteristikk'])

			if name != original_name:
				make_osm_line ("ORIGINAL_NAME", original_name)

			if school['Koordinater']:
				make_osm_line ("GEOCODE_SOURCE", school['Koordinater']['GeoKvalitet'])

			address = school['Besoksadresse']
			if address:
				address_line = ""
				if address['Adress'] and (address['Adress'] != "-"):
					address_line = address['Adress'] + ", "
				if address['Postnr']:
					address_line += address['Postnr'] + " "
				if address['Poststed']:
					address_line += address['Poststed']
				if address_line:
					make_osm_line ("ADDRESS", address_line)

			# Done with OSM node

			file.write ('  </node>\n')

	# Produce OSM file footer

	file.write ('</osm>\n')
	file.close()

	message ("\r%i schools written to file\n" % count)
