


#Functions to split entries which contain a list of multiple countries
def HandleSplit(x, delim, data, col):
    if isinstance(x[col], str):
        x[col] = x[col].split(delim)
    return x
        
def SplitCountries(data, col, delim = ', '):
    data = data.apply(lambda x: HandleSplit(x, delim, data, col), axis = 1)
    data = data.explode(col, ignore_index = True)
    return data

#Functions to convert country names into standardized ISO-2 country codes
def CheckKeys(x, c_dict, not_in_dict):
    if not_in_dict == False:
        if x in c_dict.keys():
            return c_dict[x]
        else:
            return x
    else:
        return c_dict[x]
    
def CountryCodes(data, country_col, c_dict, not_in_dict = True):
    countries = data[country_col]
    countries = countries.apply(lambda x: CheckKeys(x, c_dict, not_in_dict))
    data[country_col] = countries
    return data

#functions to remove rows containing certain locations
def IncludeCountry(x, countries, country_col, filter_out):
    if filter_out == True:
        if x[country_col] in countries:
            return False
        return True
    else:
        if x[country_col] in countries:
            return True
        return False

def RemoveLoc(data, countries, country_col, filter_out = True):
    include = data.apply(lambda x: IncludeCountry(x, countries, country_col, filter_out), axis = 1)
    data = data[include]
    return data

#functions to filter the data to only include certain years
def Between(x, year_col, begin, end):
    if int(x[year_col]) >= begin and int(x[year_col]) <= end:
        return True
    else:
        return False
    
def YearCutoff(data, year_col, begin, end):
    locs = data.apply(lambda x: Between(x, year_col, begin, end), axis = 1)
    data = data[locs]
    data = data.reset_index()
    return data

#Function to convert organizations to their constituent countries then explode the dataframe

def ApplyOrg(x, country_col, org_list):
    if x[country_col] in org_list.keys():
        x[country_col] = org_list[x[country_col]]
    return x

def ConvertOrgs(data, country_col, org_list):
    data = data.apply(lambda x: ApplyOrg(x, country_col, org_list), axis = 1)
    data = data.explode(country_col, ignore_index = True)
    return data

#function to create a score column

def ApplyScore(x, scores, data_country_col, score_country_col, score_score_col, 
               year_sensitive, data_year_col, score_year_col):
    country = x[data_country_col]
    if year_sensitive == False:
        score = scores.loc[scores[score_country_col] == country, score_score_col]
        if score.shape[0] == 0:
            return "N/A"
        else:
            return score.values[0]
    else:
        year = x[data_year_col]
        score = scores.loc[(scores[score_country_col] == country) & (scores[score_year_col] == year), 
                           score_score_col]
        if score.shape[0] == 0:
            return "N/A"
        else:
            return score.values[0]

def CreateScoreCol(data, scores, data_country_col, score_country_col, score_score_col, new_col_name, 
                   year_sensitive = False, data_year_col = None, score_year_col = None):
    scores = data.apply(lambda x: ApplyScore(x, scores, data_country_col, score_country_col,
                                              score_score_col, year_sensitive, data_year_col, 
                                              score_year_col), axis = 1)
    data[new_col_name] = scores
    return data

us_states = {
    'AL': 'US',
    'AK': 'US',
    'AZ': 'US',
    'AR': 'US',
    'CA': 'US',
    'CO': 'US',
    'CT': 'US',
    'DE': 'US',
    'FL': 'US',
    'GA': 'US',
    'HI': 'US',
    'ID': 'US',
    'IL': 'US',
    'IN': 'US',
    'IA': 'US',
    'KS': 'US',
    'KY': 'US',
    'LA': 'US',
    'ME': 'US',
    'MD': 'US',
    'MA': 'US',
    'MI': 'US',
    'MN': 'US',
    'MS': 'US',
    'MO': 'US',
    'MT': 'US',
    'NE': 'US',
    'NV': 'US',
    'NH': 'US',
    'NJ': 'US',
    'NM': 'US',
    'NY': 'US',
    'NC': 'US',
    'ND': 'US',
    'OH': 'US',
    'OK': 'US',
    'OR': 'US',
    'PA': 'US',
    'RI': 'US',
    'SC': 'US',
    'SD': 'US',
    'TN': 'US',
    'TX': 'US',
    'UT': 'US',
    'VT': 'US',
    'VA': 'US',
    'WA': 'US',
    'WV': 'US',
    'WI': 'US',
    'WY': 'US',
    'DC': 'US'
}

import pycountry
alpha_2_to_name={}
t = list(pycountry.countries)

for country in t:
    alpha_2_to_name[country.alpha_2]=country.name

name_to_alpha_2 = dict((name, code) for code,name in alpha_2_to_name.items())

extra = {
    'Wales': 'GB',
    'England': 'GB',
    'Scotland': 'GB',
    'Russia': 'RU',
    'Domincan Republic': 'DO',
    'USA': 'US',
    'Macedonia': 'MK',
    'United States of America': 'US',
    'Democratic Republic of Congo': 'CD',
    'Republic of Korea': 'KR',
    "Democratic People's Republic of Korea": "KP",
    'Tanzania': "TZ",
    'Iran': 'IR',
    'The Republic of North Macedonia': 'MK',
    'Micronesia (Federated States of)': 'FM',
    'State of Palestine': 'PS',
    'Moldova': 'MD',
    'Bolivia (Plurinational State of)': 'BO',
    'Democratic Republic of the Congo': 'CD',
    'Czech Republic': 'CZ',
    'Venezuela': 'VE',
    'Cote d\'Ivoire': 'CI',
    'Vatican': 'VA',
    'Germany': 'DE',
    'Republic of Cyprus': 'CY',
    'Republic of the Congo': 'CG',
    'Ivory Coast': 'CI',
    'Sahrawi Arab Democratic Republic': 'EH',
    'São Tomé and Príncipe': 'ST',
    'Bolivia': 'BO',
    'Taiwan': 'TW',
    'Federated States of Micronesia': 'FM',
    'South Korea': 'KR',
    'South Vietnam': 'VN',
    'Holy See': 'VA',
    'Brunei': 'BN',
    'Palestine': 'PS',
    'Syria': 'SY',
    'Kosovo': 'XK',
    'Malagasy Republic': 'MG',
    'Yugoslavia': 'YU',
    'North Korea': 'KP',
    'Laos':'LA',
    'Ceylon': 'LK',
    'Transjordan': 'JO',
    'Korea (Rep. of)': 'KR',
    'Nepal (Republic of)': 'NP',
    'Iran (Islamic Republic of)': 'IR',
    'Dominican Rep.': 'DO',
    'Dem. Rep. of the Congo': 'CD',
    'Central African Rep.': 'CF',
    'Dem. People\'s Rep. of Korea': 'KP',
    'Micronesia': 'FM',
    'Lao P.D.R.': 'LA',
    'Congo (Rep. of the)': 'CG',
    'Macau': 'MO',
    'Vietnam': 'VN',
    'Myanmar [Burma]': 'MM',
    'Netherlands Antilles': 'NL',
    'Cape Verde': 'CV',
    "British Virgin Islands": 'VG',
    'eSwatini': 'SZ',
    'Republic of Congo': 'CG',
    'Caribbean Netherlands': 'BQ',
    'Curacao': 'CW',
    'Sint Maarten': 'SX',
    'Saint-Martin': 'MF',
    'Bailiwick of Guernsey':'GG',
    'Bailiwick of Jersey' : 'JE',
    'East Timor': 'TL',
    'Reunion': 'RE',
    'Vatican City': 'VA',
    'West Bank and Gaza': 'PS',
    'Bahamas, The': 'BS',
    'Congo, Republic of ': 'CG',
    'Hong Kong SAR': 'HK',
    'Kyrgyz Republic': 'KG',
    'North Macedonia ': 'MK',
    'Slovak Republic': 'SK',
    'South Sudan, Republic of': 'SS',
    'Taiwan Province of China': 'TW',
    'Türkiye, Republic of': 'TR',
    'Gambia, The': 'GM',
    "China, People's Republic of": 'CN',
    'Congo, Dem. Rep. of the': 'CD',
    'Micronesia, Fed. States of': 'FM',
    'West Bank and Gaza Strip': 'PS'
}

for key, value in extra.items():
    name_to_alpha_2[key] = value



name_to_alpha_2

alpha_3_to_alpha_2 = {}
for country in pycountry.countries:
    alpha_3_to_alpha_2[country.alpha_3] = country.alpha_2

# +
alpha_3_extra = {
    "XKX": "XK"
}

for key, value in alpha_3_extra.items():
    alpha_3_to_alpha_2[key] = value
# -



country_orgs = {
"EU": ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Republic of Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'],
"NAFTA" : ['Canada', 'Mexico', 'United States'],
"ECOWAS" : ['Benin', 'Burkina Faso', 'Cabo Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo'],
"African Union" : ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Democratic Republic of the Congo', 'Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sahrawi Arab Democratic Republic', 'São Tomé and Príncipe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'],
"commonwealth" : ['Antigua and Barbuda', 'Australia', 'The Bahamas', 'Bangladesh', 'Barbados', 'Belize', 'Botswana', 'Brunei Darussalam', 'Cameroon', 'Canada', 'Cyprus', 'Dominica', 'Eswatini', 'Fiji', 'The Gambia', 'Ghana', 'Grenada', 'Guyana', 'India', 'Jamaica', 'Kenya', 'Kiribati', 'Lesotho', 'Malawi', 'Malaysia', 'Maldives', 'Malta', 'Mauritius', 'Mozambique', 'Namibia', 'Nauru', 'New Zealand', 'Nigeria', 'Pakistan', 'Papua New Guinea', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Seychelles', 'Sierra Leone', 'Singapore', 'Solomon Islands', 'South Africa', 'Sri Lanka', 'Tanzania', 'Tonga', 'Trinidad and Tobago', 'Tuvalu', 'Uganda', 'United Kingdom', 'Vanuatu', 'Zambia'],
"G7" : ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States'],
'G8' : ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'Russia', 'United Kingdom', 'United States'],
"League of Arab States" : ['Algeria', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt', 'Iraq'],
"MERCOSUR" : ['Argentina', 'Brazil', 'Paraguay', 'Uruguay'],
"OIC" : ['Afghanistan', 'Albania', 'Algeria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Benin', 'Brunei', 'Burkina Faso', 'Cameroon', 'Chad', 'Comoros', 'Côte d\'Ivoire', 'Djibouti', 'Egypt', 'Gabon', 'Gambia', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Indonesia', 'Iran', 'Iraq', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Lebanon', 'Libya', 'Malaysia', 'Maldives', 'Mali', 'Mauritania', 'Morocco', 'Mozambique', 'Niger', 'Nigeria', 'Oman', 'Pakistan', 'Palestine', 'Qatar', 'Saudi Arabia', 'Senegal', 'Sierra Leone', 'Somalia', 'Sudan', 'Suriname', 'Syria', 'Tajikistan', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'United Arab Emirates', 'Uzbekistan', 'Yemen'],
"OSCE" : ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Canada', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Holy See', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kyrgyzstan', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Tajikistan', 'Turkey', 'Turkmenistan', 'Ukraine', 'United Kingdom', 'United States', 'Uzbekistan'],
"OAS" : ['Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'United States', 'Uruguay', 'Venezuela'],
'Pacific Islands Forum' : ['Australia', 'Cook Islands', 'Federated States of Micronesia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Nauru', 'New Zealand', 'Niue', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu'],
"SADC" : ['Angola', 'Botswana', 'Comoros', 'Democratic Republic of the Congo', 'Eswatini', 'Lesotho', 'Madagascar', 'Malawi', 'Mauritius', 'Mozambique', 'Namibia', 'Seychelles', 'South Africa', 'Tanzania', 'Zambia', 'Zimbabwe'],
"UNASUR" : ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']
}






    

