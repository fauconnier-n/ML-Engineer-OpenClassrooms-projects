def OFF_Cleaning(file_path, output_path)
	"Nettoyage des données OpenFoodFacts"
	
	"file_path: emplacement du csv d'origine"
	"output_path: emplacement de sortie du fichier nettoyé"
	
	import pandas as pd
	
	# ouvre le fichier csv 
	raw_data = pd.read_csv(file_path, sep='\t')
	
	# Passe nova_group en var catégorielle
	raw_data['nova_group'] = raw_data['nova_group'].astype('object')
	
	# filtre France dans multiples langues
	# filtre non sensible aux majuscules
	raw_data = raw_data[raw_data["countries_en"].str.contains("France|Frankreich|Francia|França|???????|Francia|Frankrijk|Francja|Franta|Fransa|???????|Frankrijk|?a???a|Ga???a|Gallia|Francuska|Francúzsko|Francie|Frakkland", na = False, case=False)]
	
	# Filtre les boissons
	raw_data = raw_data[(raw_data['pnns_groups_1'] == 'Beverages') | (raw_data['pnns_groups_2'] == 'Alcoholic beverages')]
	
	# Supprime les colonnes vides (principalement des sous-catégories d'un ingrédient e.g. sucre)
	raw_data.dropna(axis = 1, how = 'all', inplace=True)
	
	# Drop les lignes sans nutrition facts
	raw_data = raw_data.dropna(subset=nutrition_facts, how='all')
	
	# Suppression des lignes sans nom de produit
	raw_data = raw_data.dropna(subset=['product_name'])
	
	# Drop des doublons ayant le même code
	raw_data = raw_data.drop_duplicates('code',keep='first')
	
	# tri le dataset par nombre de valeurs manquantes descendantes puis date de modification ascendantes
	raw_data['null_count'] = raw_data.isnull().sum(axis=1)
	raw_data = raw_data.sort_values(['null_count', 'last_modified_t'], ascending=(False, False)).drop('null_count', axis=1)

	# suppression des doublons
	raw_data = raw_data.drop_duplicates(subset=['product_name','quantity', 'packaging', 'brands'], keep='first')
	
	# drop de la selection de colonnes hors-descriptif du dataset
	raw_data = raw_data.drop(['packaging_text', 'energy-from-fat_100g', 'fruits-vegetables-nuts-dried_100g', 'fruits-vegetables-nuts-estimate_100g', 'carbon-footprint-from-meat-or-fish_100g'], axis = 1)
	
	# drop d'une selection de colonnes
	raw_data = raw_data.drop(['url', 'creator', 'created_datetime', 'last_modified_t', 'last_modified_datetime', 'abbreviated_product_name', 'generic_name', 'image_url', 'image_small_url', 'image_ingredients_url', 'image_ingredients_small_url', 'image_nutrition_url', 'image_nutrition_small_url', 'carbon-footprint_100g'], axis = 1)
	
	# Drop de colonnes redondantes
	raw_data = raw_data.drop(['packaging_tags'], axis = 1)
	raw_data = raw_data.drop(['brands_tags'], axis = 1)
	raw_data = raw_data.drop(['categories_tags', 'categories'], axis = 1)
	raw_data = raw_data.drop(['origins', 'origins_tags'], axis = 1)
	raw_data = raw_data.drop(['manufacturing_places_tags'], axis = 1)
	raw_data = raw_data.drop(['labels_tags', 'labels'], axis = 1)
	raw_data = raw_data.drop(['emb_codes_tags'], axis = 1)
	raw_data = raw_data.drop(['countries', 'countries_tags'], axis = 1)
	raw_data = raw_data.drop(['traces_tags', 'traces'], axis = 1)
	raw_data = raw_data.drop(['additives_tags'], axis = 1)
	raw_data = raw_data.drop(['nutriscore_score'], axis = 1)
	raw_data = raw_data.drop(['states', 'states_tags'], axis = 1)
	raw_data = raw_data.drop(['main_category'], axis = 1)
	
	# Supprime les lignes ayant des valeurs aberrantes (>100 ou <0)
	raw_data = raw_data[~(raw_data[['fat_100g', 'saturated-fat_100g', 'omega-3-fat_100g', 'omega-9-fat_100g', 'fiber_100g', 'calcium_100g', 'iron_100g', 'fruits-vegetables-nuts-estimate-from-ingredients_100g','carbohydrates_100g', 'sugars_100g']] > 100).any(axis=1)]
	raw_data = raw_data[~(raw_data[['fat_100g', 'saturated-fat_100g', 'omega-3-fat_100g', 'omega-9-fat_100g', 'fiber_100g', 'calcium_100g', 'iron_100g', 'fruits-vegetables-nuts-estimate-from-ingredients_100g','carbohydrates_100g', 'sugars_100g']] < 0).any(axis=1)]
	
	raw_data = raw_data.drop(['categories_en'], axis = 1)
	
	# créé 3 colonnes Dummies
	raw_data['organic'] = raw_data["labels_en"].str.contains("bio|organic", na = False, case=False).astype(int)
	raw_data['fairtrade'] = raw_data["labels_en"].str.contains("fairtrade|fair trade|equitable|équitable", na = False, case=False).astype(int)
	raw_data['madeinfrance'] = raw_data["labels_en"].str.contains("made in france|madeinefrance|fabriqué en france|fabrique en france|fabriquéenfrance|fabriqueenfrance", na = False, case=False).astype(int)

	# drop labels_en
	raw_data = raw_data.drop(['labels_en'], axis = 1)
	
	# Drop de colonnes
	raw_data = raw_data.drop(['packaging', 'origins_en', 'manufacturing_places', 'emb_codes', 'first_packaging_code_geo', 'cities_tags', 'purchase_places', 'stores', 'countries_en', 'ingredients_text', 'serving_size', 'serving_quantity', 'states_en'], axis = 1)
	
	# Convertit en kcal 
	raw_data['energy-kj_100g'] = raw_data['energy-kj_100g'].apply(lambda x: x/4,1868)
	raw_data['energy_100g'] = raw_data['energy_100g'].apply(lambda x: x/4,1868)
	
	# Fill
	raw_data['energy-kcal_100g'] = raw_data['energy-kcal_100g'].fillna(raw_data['energy-kj_100g'])
	raw_data['energy-kcal_100g'] = raw_data['energy-kcal_100g'].fillna(raw_data['energy_100g'])

	# Drop
	raw_data = raw_data.drop(['energy-kj_100g', 'energy_100g'], axis = 1)
	
	# calcul la valeur energetique pour 100g pour tous les produits
	raw_data['energie'] = raw_data['energy-kcal_100g'].fillna(raw_data.groupby('pnns_groups_2')['energy-kcal_100g'].transform('median'))
	
	# Fill
	raw_data['energy-kcal_100g'] = np.where(raw_data['energy-kcal_100g'].isna() == True, raw_data['energie'], raw_data['energy-kcal_100g'])

	# Drop colonne energie
	raw_data = raw_data.drop(['energie'], axis = 1)
	
	# Fill
	raw_data['fruits-vegetables-nuts_100g'] = raw_data['fruits-vegetables-nuts_100g'].fillna(raw_data['fruits-vegetables-nuts-estimate-from-ingredients_100g'])

	# Drop
	raw_data = raw_data.drop(['fruits-vegetables-nuts-estimate-from-ingredients_100g'], axis = 1)
	
	# Fill NaN par 0 pour les variables X_100g
	nutrition_facts = list(raw_data.columns[(raw_data.columns.str.endswith('_100g') == True) & (raw_data.columns != 'nutrition-score-fr_100g') & (raw_data.columns != 'energy-kcal_100g')])
	
	# Fill par nom de colonne
	raw_data[nutrition_facts] = raw_data[nutrition_facts].fillna(0)

	
	
	
	# calcul du nutriscore pour chaque ligne a partir des données nutritionnelles
	def calc_score(row):
		# energie
		if row['energy-kcal_100g']*4.1868 <= 0:
			energie = 0
		elif ((row['energy-kcal_100g']*4.1868 > 0) and (row['energy-kcal_100g']*4.1868 <= 30)):
			energie = 1
		elif ((row['energy-kcal_100g']*4.1868 > 30) and (row['energy-kcal_100g']*4.1868 <= 60)):
			energie = 2
		elif ((row['energy-kcal_100g']*4.1868 > 60) and (row['energy-kcal_100g']*4.1868 <= 90)):
			energie = 3
		elif ((row['energy-kcal_100g']*4.1868 > 90) and (row['energy-kcal_100g']*4.1868 <= 120)):
			energie = 4
		elif ((row['energy-kcal_100g']*4.1868 > 120) and (row['energy-kcal_100g']*4.1868 <= 150)):
			energie = 5
		elif ((row['energy-kcal_100g']*4.1868 > 150) and (row['energy-kcal_100g']*4.1868 <= 180)):
			energie = 6
		elif ((row['energy-kcal_100g']*4.1868 > 180) and (row['energy-kcal_100g']*4.1868 <= 210)):
			energie = 7
		elif ((row['energy-kcal_100g']*4.1868 > 210) and (row['energy-kcal_100g']*4.1868 <= 240)):
			energie = 8
		elif ((row['energy-kcal_100g']*4.1868 > 240) and (row['energy-kcal_100g']*4.1868 <= 270)):
			energie = 9
		else:
			energie = 10    
		# sucre
		if row['sugars_100g'] <= 0:
			sucre = 0
		elif ((row['sugars_100g'] > 0) and (row['sugars_100g'] <= 1.5)):
			sucre = 1
		elif ((row['sugars_100g'] > 1.5) and (row['sugars_100g'] <= 3)):
			sucre = 2
		elif ((row['sugars_100g'] > 3) and (row['sugars_100g'] <= 4.5)):
			sucre = 3
		elif ((row['sugars_100g'] > 4.5) and (row['sugars_100g'] <= 6)):
			sucre = 4
		elif ((row['sugars_100g'] > 6) and (row['sugars_100g'] <= 7.5)):
			sucre = 5
		elif ((row['sugars_100g'] > 7.5) and (row['sugars_100g'] <= 9)):
			sucre = 6
		elif ((row['sugars_100g'] > 9) and (row['sugars_100g'] <= 10.5)):
			sucre = 7
		elif ((row['sugars_100g'] > 10.5) and (row['sugars_100g'] <= 12)):
			sucre = 8
		elif ((row['sugars_100g'] > 12) and (row['sugars_100g'] <= 13.5)):
			sucre = 9
		else:
			sucre = 10 
		# gsat (graisses saturées)
		if row['saturated-fat_100g'] <= 1:
			gsat = 0
		elif ((row['saturated-fat_100g'] > 1) and (row['saturated-fat_100g'] <= 2)):
			gsat = 1
		elif ((row['saturated-fat_100g'] > 2) and (row['saturated-fat_100g'] <= 3)):
			gsat = 2
		elif ((row['saturated-fat_100g'] > 3) and (row['saturated-fat_100g'] <= 4)):
			gsat = 3
		elif ((row['saturated-fat_100g'] > 4) and (row['saturated-fat_100g'] <= 5)):
			gsat = 4
		elif ((row['saturated-fat_100g'] > 5) and (row['saturated-fat_100g'] <= 6)):
			gsat = 5
		elif ((row['saturated-fat_100g'] > 6) and (row['saturated-fat_100g'] <= 7)):
			gsat = 6
		elif ((row['saturated-fat_100g'] > 7) and (row['saturated-fat_100g'] <= 8)):
			gsat = 7
		elif ((row['saturated-fat_100g'] > 8) and (row['saturated-fat_100g'] <= 9)):
			gsat = 8
		elif ((row['saturated-fat_100g'] > 9) and (row['saturated-fat_100g'] <= 10)):
			gsat = 9
		else:
			gsat = 10 
		# sodium
		if row['sodium_100g']*1000 <= 90:
			sodium = 0
		elif ((row['sodium_100g']*1000 > 90) and (row['sodium_100g']*1000 <= 180)):
			sodium = 1
		elif ((row['sodium_100g']*1000 > 180) and (row['sodium_100g']*1000 <= 270)):
			sodium = 2
		elif ((row['sodium_100g']*1000 > 270) and (row['sodium_100g']*1000 <= 360)):
			sodium = 3
		elif ((row['sodium_100g']*1000 > 360) and (row['sodium_100g']*1000 <= 450)):
			sodium = 4
		elif ((row['sodium_100g']*1000 > 450) and (row['sodium_100g']*1000 <= 540)):
			sodium = 5
		elif ((row['sodium_100g']*1000 > 540) and (row['sodium_100g']*1000 <= 630)):
			sodium = 6
		elif ((row['sodium_100g']*1000 > 630) and (row['sodium_100g']*1000 <= 720)):
			sodium = 7
		elif ((row['sodium_100g']*1000 > 720) and (row['sodium_100g']*1000 <= 810)):
			sodium = 8
		elif ((row['sodium_100g']*1000 > 810) and (row['sodium_100g']*1000 <= 900)):
			sodium = 9
		else:
			sodium = 10
		# fruit
		if row['fruits-vegetables-nuts_100g'] <= 40:
			fruit = 0
		elif ((row['fruits-vegetables-nuts_100g'] > 40) and (row['fruits-vegetables-nuts_100g'] <= 60)):
			fruit = 2
		elif ((row['fruits-vegetables-nuts_100g'] > 60) and (row['fruits-vegetables-nuts_100g'] <= 80)):
			fruit = 4
		else:
			fruit = 10
		# fibre
		if row['fiber_100g'] <= 0.9:
			fibre = 0
		elif ((row['fiber_100g'] > 0.9) and (row['fiber_100g'] <= 1.9)):
			fibre = 1
		elif ((row['fiber_100g'] > 1.9) and (row['fiber_100g'] <= 2.8)):
			fibre = 2
		elif ((row['fiber_100g'] > 2.8) and (row['fiber_100g'] <= 3.7)):
			fibre = 3
		elif ((row['fiber_100g'] > 3.7) and (row['fiber_100g'] <= 4.7)):
			fibre = 4
		else:
			fibre = 5
		# proteines
		if row['proteins_100g'] <= 0.9:
			proteines = 0
		elif ((row['proteins_100g'] > 0.9) and (row['proteins_100g'] <= 1.9)):
			proteines = 1
		elif ((row['proteins_100g'] > 1.9) and (row['proteins_100g'] <= 2.8)):
			proteines = 2
		elif ((row['proteins_100g'] > 2.8) and (row['proteins_100g'] <= 3.7)):
			proteines = 3
		elif ((row['proteins_100g'] > 3.7) and (row['proteins_100g'] <= 4.7)):
			proteines = 4
		else:
			proteines = 5
		
		# score
		nutriscore = energie+sucre+gsat+sodium-fruit-fibre-proteines
		
		return nutriscore

	

	# calcul du nutrigrade pour chaque ligne a partir du nutriscore calculé par la fonction précédente
	def calc_grade(row):
		if ((row['nutriscore'] <= 0) and (row['pnns_groups_2'] == 'Waters and flavored waters')):
			nutrigrade = 'a'
		elif ((row['nutriscore'] <= 1) and (row['pnns_groups_2'] != 'Waters and flavored waters') or (row['nutriscore'] == 1) and (row['pnns_groups_2'] == 'Waters and flavored waters')): 
			nutrigrade = 'b'
		elif ((row['nutriscore'] >= 2) and (row['nutriscore'] <= 5)):
			nutrigrade = 'c'
		elif ((row['nutriscore'] >= 6) and (row['nutriscore'] <= 9)):
			nutrigrade = 'd'
		elif ((row['pnns_groups_2'] == 'Alcoholic beverages') or (row['alcohol_100g'] > 1.2)):
			nutrigrade = 'alcool'
		else:
			nutrigrade = 'e'
			
		return nutrigrade


	# Calcul des nutriscores et nutrigrades à l'aide des fonctions
	raw_data['nutriscore'] = raw_data.apply(lambda row: calc_score(row),axis=1)
	raw_data['nutrigrade'] = raw_data.apply(lambda row: calc_grade(row),axis=1)
	
	# Fill
	raw_data['nutrigrade'] = np.where(raw_data['nutriscore_grade'].isna() == True, raw_data['nutrigrade'], raw_data['nutriscore_grade'])
	raw_data['nutrigrade'] = np.where((raw_data['alcohol_100g'] > 1.2) | (raw_data['nutrigrade'] == 'alcool') | (raw_data['pnns_groups_2'] == 'Alcoholic beverages'), 'alcool', raw_data['nutrigrade'])
	
	# Fill
	raw_data['brands'] = raw_data['brands'].fillna(raw_data['brand_owner'])

	# drop
	raw_data = raw_data.drop(['brand_owner'], axis = 1)
	
	# Autres fills par 0
	raw_data['additives_n'] = raw_data['additives_n'].fillna(0)
	raw_data['ingredients_from_palm_oil_n'] = raw_data['ingredients_from_palm_oil_n'].fillna(0)
	raw_data['ingredients_that_may_be_from_palm_oil_n'] = raw_data['ingredients_that_may_be_from_palm_oil_n'].fillna(0)

	# on fill également l'écograde quand il n'est pas reseigné, ainsi que le nova_group
	raw_data['ecoscore_grade_fr'] = raw_data['ecoscore_grade_fr'].fillna('inconnu')
	raw_data['nova_group'] = raw_data['nova_group'].fillna('inconnu')
	
	# Drop
	raw_data = raw_data.drop(['created_t', 'traces_en', 'additives_en', 'ingredients_from_palm_oil_tags', 'ingredients_that_may_be_from_palm_oil_tags', 'pnns_groups_1', 'main_category_en', 'brands'], axis = 1)
	
	# Transformation en dummy
	raw_data['allergens'] = np.where((raw_data['allergens'].notna() == True), 1, 0)
	
	
	
	# Selection pour eviter des colonnes supplémentaires en cas d'ajouts dans le fichier csv d'origine
	raw_data = raw_data['code',	'product_name',	'quantity',	'allergens',	'additives_n',	'ingredients_from_palm_oil_n',	'ingredients_that_may_be_from_palm_oil_n',	'nova_group',	'pnns_groups_2',	'ecoscore_score_fr',	'ecoscore_grade_fr',	'energy-kcal_100g',	'fat_100g',	'saturated-fat_100g',	'monounsaturated-fat_100g',	'polyunsaturated-fat_100g',	'omega-3-fat_100g',	'omega-6-fat_100g',	'omega-9-fat_100g',	'trans-fat_100g',	'cholesterol_100g',	'carbohydrates_100g',	'sugars_100g',	'starch_100g',	'polyols_100g',	'fiber_100g',	'proteins_100g',	'casein_100g',	'serum-proteins_100g',	'salt_100g',	'sodium_100g	alcohol_100g',	'vitamin-a_100g',	'beta-carotene_100g',	'vitamin-d_100g',	'vitamin-e_100g',	'vitamin-k_100g',	'vitamin-c_100g',	'vitamin-b1_100g',	'vitamin-b2_100g',	'vitamin-pp_100g',	'vitamin-b6_100g',	'vitamin-b9_100g',	'folates_100g',	'vitamin-b12_100g',	'biotin_100g',	'pantothenic-acid_100g',	'silica_100g',	'bicarbonate_100g',	'potassium_100g',	'chloride_100g',	'calcium_100g',	'phosphorus_100g',	'iron_100g',	'magnesium_100g',	'zinc_100g',	'copper_100g',	'manganese_100g',	'fluoride_100g',	'selenium_100g',	'chromium_100g',	'molybdenum_100g',	'iodine_100g',	'caffeine_100g',	'taurine_100g',	'ph_100g',	'fruits-vegetables-nuts_100g',	'cocoa_100g',	'choline_100g',	'phylloquinone_100g',	'beta-glucan_100g',	'inositol_100g',	'organic',	'fairtrade',	'madeinfrance',	'nutriscore',	'nutrigrade']
	
	
	
	# Sauvegarde le csv final
	raw_data.to_csv(output_path, index=False)