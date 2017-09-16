import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pymongo
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import csv
import pandas as pd
from sklearn import datasets
from sklearn.cluster import KMeans
'''
creating list of word to be ignored
'''
#Access nucleus Database for Companies, Founders and investors
#MONGODB_HOST = os.environ.get('MONGO_PORT_27017_TCP_ADDR', '127.0.0.1:27017')
MONGODB_HOST = '52.74.117.77:27017'

client = pymongo.MongoClient("mongodb://nucleus42Root:#42root@{}".format(MONGODB_HOST))
dbn = client['nucleus42']


company_list = list()
investor_list = list()
founder_list = list()
city_list = list()

#make a list of companies
for document in dbn.companies.find():
    company_list.append(document.get('name').lower())

company_list = list(set(company_list))
print(company_list)


#make a list of founders
for document in dbn.companies.find():
    for i in document.get('founders', []):
        founder_list.append(i.get('name').lower())

founder_list = list(set(founder_list))
print(founder_list)


#make the list of investors
for document in dbn.investors.find():
    investor_list.append(document.get('name').lower())

investor_list = list(set(investor_list))
print(investor_list)

#make a list of cities

for document in dbn.companies.find():
    if document.get('city'):
        city_list.append(document.get('city').lower())
    # else:
    #     import ipdb; ipdb.set_trace();

city_list = list(set(city_list))
print(city_list)

#make a list of stopwords
stop = stopwords.words('english')
#remove it if you need punctuation
for i in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|']:
    stop += i
print(stop)

'''
creating the array of list of words from document
'''

links = [
         "https://inc42.com/flash-feed/veqta-raises-500k-in-seed-funding/",
         "https://inc42.com/flash-feed/taxivaxi-raises-500k-seed-funding/",
         "https://inc42.com/flash-feed/appie-raises-1-mn-funding/",
         "https://inc42.com/flash-feed/wow-express-pre-series-a-funding/",
         "https://inc42.com/flash-feed/zenify-raises-900k-pre-series-funding-hnis/",
         "https://inc42.com/flash-feed/mobikwik-raises-funding-from-japanese-and-taiwanese-investors/",
         # "https://inc42.com/flash-feed/qikship-angel-funding/",
         # "https://inc42.com/buzz/unacademy-funding/",
         # "https://inc42.com/flash-feed/lifcare-funding/",
         # "https://inc42.com/buzz/olacabs-close-raise-funding-steadview-capital/",
         # "https://inc42.com/flash-feed/einsite-seed-funding/",
         # "https://inc42.com/buzz/timesaverz-raises-angel-funding/",
         # "https://inc42.com/flash-feed/cookaroo-raises-angel-funding/",
         # "https://inc42.com/flash-feed/murgency-raises-funding/",
         # "https://inc42.com/flash-feed/wheelstreet-funding/",
         # "https://inc42.com/flash-feed/gapoon-funding/",
         # "https://inc42.com/startups/vanitycube-funding/",
         # "https://inc42.com/flash-feed/snapdeal-freecharge-funding/",
         # "https://inc42.com/flash-feed/hello-curry-bridge-funding/",
         # "https://inc42.com/flash-feed/igrenenergi-funding/",
         # "https://inc42.com/flash-feed/remidio-funding/",
         # "https://inc42.com/flash-feed/fitso-raises-angel-funding/",
         # "https://inc42.com/flash-feed/stylflip-raises-seed-funding/",
         # "https://inc42.com/flash-feed/gray-routes-funding/",
         # "https://inc42.com/flash-feed/cityshor-funding/",
         # "https://inc42.com/flash-feed/derbii-angel-funding/",
         # "https://inc42.com/flash-feed/workindia-raises-funding/",
         # "https://inc42.com/flash-feed/naaptol-raises-51-mn/",
         # "https://inc42.com/flash-feed/kartrocket-closes-series-b-funding/",
         # "https://inc42.com/flash-feed/actonmagic-raises-seed-funding/",
         # "http://techcrunch.com/2016/05/25/europe-eyes-new-rules-for-online-platforms/",
         # "http://techcrunch.com/2016/05/25/xiaomi-mi-drone/",
         # "http://techcrunch.com/2016/05/25/playlists-not-blogs/",
         # "http://techcrunch.com/2016/05/25/demisto-emerges-from-stealth-with-smart-security-bot-to-improve-security-ops/",
         # "http://techcrunch.com/2016/05/25/eero-inks-50-million-funding-deal-with-menlos-opportunity-fund-plans-to-sell-products-at-bestbuy/",
         # "http://techcrunch.com/2016/05/25/equipmentshare-raises-5-5-million-for-peer-to-peer-marketplace-for-heavy-equipment/",
         # "http://techcrunch.com/2016/05/25/password-and-id-startup-dashlane-now-with-5m-users-raises-22-5m-led-by-transunion/",
         # "http://techcrunch.com/2016/05/25/playlists-not-blogs/",
         # "http://techcrunch.com/2016/05/24/bloomz-raises-2-3-million-to-connect-teachers-and-students-families/",
         # "http://techcrunch.com/2016/05/24/varsity-tutors-the-online-platform-for-learning-launches-a-mobile-app/",
         # "http://techcrunch.com/2016/05/24/menu-next-door-grabs-2-million-for-its-home-cooking-platform/",
         # "http://techcrunch.com/2016/05/24/wrios-roomier-keyboard-app-launches-on-android-ios/",
         # "http://techcrunch.com/2016/05/23/penny-raises-1-2m-in-seed-funding-for-its-personal-finance-bot/",
         # "http://techcrunch.com/2016/05/23/syndicateroom-raises-4-5m-series-a/",
         # "http://techcrunch.com/2016/05/23/zzish/",
         # "http://techcrunch.com/2016/05/23/comparably-glassdoor/",
         # "http://techcrunch.com/2016/05/23/steve-the-jumping-dinosaur-lands-on-his-feet/",
         # "http://techcrunch.com/2016/05/23/seamlessdocs-raises-7-million-series-b-to-help-governments-go-digital/",
         # "http://techcrunch.com/2016/05/23/new-subscription-service-circle-go-lets-parents-manage-kids-devices-outside-the-home/",
         # "http://techcrunch.com/2016/05/23/ziro-is-a-nifty-hand-controlled-robotics-kit-for-kids/",
         # "http://techcrunch.com/2016/05/20/metadata-seed-funding/",
         # "http://techcrunch.com/2016/05/20/twitter-and-betaworks-are-teaming-up-in-a-new-fund/",
         # "http://techcrunch.com/2016/05/20/flashfunders-relaunches-with-crowdfunding-support-with-the-pass-of-title-iii-of-the-jobs-act/",
         # "http://techcrunch.com/2016/05/20/fitbit-finally-gets-design-with-the-alta-sports-tracker/",
         # "http://techcrunch.com/2016/05/20/the-europas-its-time-for-different-type-of-tech-conference/",
         # "http://techcrunch.com/2016/05/19/chemists-create-an-app-that-can-tell-if-your-beer-is-skunked/",
         # "http://techcrunch.com/2016/05/19/reddit-embeds/",
         # "http://techcrunch.com/2016/05/19/edyn-debuts-smart-water-valve-to-put-home-gardens-on-autopilot/",
         # "http://techcrunch.com/2016/05/19/tally-raises-15-million-for-app-to-make-credit-cards-less-expensive-easier-to-manage/",
         # "http://techcrunch.com/2016/05/19/watch-alchemists-accelerators-demo-day-right-here/",
         # "http://techcrunch.com/2016/05/19/afero-raises-20-3-million-to-secure-connected-devices-whether-wifi-is-working-or-not/",
         # "http://techcrunch.com/2016/05/19/prx-spins-out-radiopublic/",
         # "http://techcrunch.com/2016/05/19/afero-raises-20-3-million-to-secure-connected-devices-whether-wifi-is-working-or-not/",
         # "http://techcrunch.com/2016/05/19/prx-spins-out-radiopublic/",
         # "http://techcrunch.com/2016/05/19/distrokids-music-payment-system-now-lets-you-send-cash-to-everyone-on-a-track/",
         # "http://techcrunch.com/2016/05/19/uber-confirms-its-testing-self-driving-cars-in-pittsburgh/",
         # "http://techcrunch.com/2016/05/19/boosteds-v2-electric-skateboards-go-12-miles-with-swappable-batteries/",
         # "http://techcrunch.com/2016/05/19/product-hunt-is-ready-to-rake-in-revenue-by-selling-goods-directly-on-the-platform/",
         # "http://techcrunch.com/2016/05/19/laugh-ly-is-a-streaming-radio-app-dedicated-comedy/",
         # "http://techcrunch.com/2016/05/19/tink-scores-10m-for-its-virtual-banking-app/",
         # "http://techcrunch.com/2016/05/19/zenly-solomoyolo/",
         # "http://techcrunch.com/2016/05/19/dojo-madness-raises-4-5m-to-turn-your-mobile-phone-into-an-esports-coach/",
         # "http://techcrunch.com/2016/05/19/keep-your-eyes-on-the-prize/",
         # "http://techcrunch.com/2016/05/18/three-startups-to-watch-from-hax-hardware-accelerator-batch-viii/",
         # "http://techcrunch.com/2016/05/18/shift-technology-grabs-10-million-to-prevent-fraudulent-insurance-claims/",
         # "http://techcrunch.com/2016/05/18/right-sizing-the-development-process-for-startups/",
         # "http://techcrunch.com/2016/05/18/wunwun-founder-lee-hnetinka-launches-darkstore-an-on-demand-delivery-fulfillment-platform/",
         # "http://techcrunch.com/2016/05/18/glu-mobile-launches-britney-spears-american-dream/",
         # "http://techcrunch.com/2016/05/17/socialrank-the-startup-that-analyzes-your-followers-adds-premium-features-and-pricing/",
         # "http://techcrunch.com/2016/05/17/apply-now-the-tc-meetup-pitch-off-is-coming-to-austin-and-seattle/",
         # "http://techcrunch.com/2016/05/17/dedrone-raises-10-million-to-detect-aerial-intruders/",
         # "http://techcrunch.com/2016/05/17/jifitis-new-messenger-chatbot-api-will-find-you-a-gift-even-when-youre-out-of-ideas/",
         # "http://techcrunch.com/2016/05/17/affirm-is-partnering-with-expedia-and-eventbrite-so-you-can-pay-for-experiences-over-time/",
         # "http://techcrunch.com/2016/05/17/allurion-offers-gastric-bypass-surgery-in-a-pill/",
         # "http://techcrunch.com/2016/05/17/capsule-launches-to-reinvent-the-pharmacy-complete-with-med-delivery/",
         # "http://techcrunch.com/2016/05/17/sketchfab-now-supports-all-vr-headsets-for-its-3d-model-sharing-platform/",
         # "http://techcrunch.com/2016/05/17/snips-is-a-personal-assistant-that-combines-all-your-data-in-one-app/",
         # "http://techcrunch.com/2016/05/17/this-is-your-last-chance-to-apply-to-the-techcrunch-pitch-off-in-stockholm/",
         # "http://techcrunch.com/2016/05/17/hundredrooms/",
         # "http://techcrunch.com/2016/05/17/weschool/",
         # "http://techcrunch.com/2016/05/16/angel-ai/",
         # "http://techcrunch.com/2016/05/16/meet-500startups-17th-batch-of-companies/",
         # "http://techcrunch.com/2016/05/16/blockchain-open-sources-thunder-network-paving-the-way-for-instant-bitcoin-transactions/",
         # "http://techcrunch.com/2016/05/14/what-startups-are-saying-about-raising-cash-in-latin-america/",
         # "http://techcrunch.com/2016/05/14/author-raj-raghunathan-talks-about-what-it-takes-for-smart-people-to-be-happy/",
         # "http://techcrunch.com/2016/05/13/why-britain-is-beating-the-us-at-financial-innovation/",
         # "http://techcrunch.com/2016/05/13/interesting-trends-in-angel-investing/",
         # "http://techcrunch.com/gallery/our-favorite-companies-from-500startups-16th-demo-day/",
         # "http://techcrunch.com/2016/05/13/why-incident-response-plans-fail/",
         # "http://techcrunch.com/2016/05/13/three-ways-tech-is-reinventing-a-surprising-sector/",
         # "http://techcrunch.com/2016/05/12/south-koreas-government-launches-its-first-accelerator-program-for-international-startups/",
         # "http://techcrunch.com/2016/05/12/four-ways-african-countries-can-ensure-digital-innovation-benefits-the-entire-population/",
         # "http://techcrunch.com/2016/05/12/the-technology-driven-transformation-of-wealth-management/",
         # "http://techcrunch.com/2016/05/12/european-online-travel-marketplace-evaneos-picks-up-21m-funding/",
         # "http://techcrunch.com/2016/05/12/theranos-coo-retires-as-the-troubled-bio-tech-startup-overhauls-its-organizational-structure/",
         # "http://techcrunch.com/2016/05/12/capital-float-b/",
         # "http://techcrunch.com/2016/05/11/disrupting-healthcare-is-a-tough-task-for-startups-and-venture-capital/",
         # "http://techcrunch.com/2016/05/11/beam-wins-techcrunch-disrupt-ny-2016/",
         # "http://techcrunch.com/2016/05/11/jeremy-hitchcock-steps-down/",
         # "http://techcrunch.com/2016/05/11/sunrise-will-sunset-on-august-31st/",
         # "http://techcrunch.com/2016/05/11/justin-kan-accepts-y-combinator-fellowship-pitches-over-snapchat/",
         # "http://techcrunch.com/2016/05/11/bolt-threads-raises-50-million-to-brew-spider-silk-inks-deal-with-patagonia/",
         # "http://techcrunch.com/2016/05/11/front-makes-email-collaboration-much-smoother/",
         # "http://techcrunch.com/2016/05/11/dont-copy-the-valley-copy-brooklyn/",
         # "http://techcrunch.com/2016/05/11/charged/",
         # "http://techcrunch.com/2016/05/11/monetization-churn-and-how-to-stand-out-in-the-mobile-dating-space/",
         # "http://techcrunch.com/2016/05/11/why-doordash-has-to-strike-a-balance-between-profitability-and-growth/",
         # "http://techcrunch.com/2016/05/11/jessica-alba-on-the-past-present-and-future-of-the-honest-company/",
         # "http://techcrunch.com/2016/05/11/former-citigroup-cfo-sallie-krawcheck-launches-ellevest-a-digital-investment-platform-for-women/",
         # "http://techcrunch.com/2016/05/11/soracom-an-iot-platform-provider-based-in-japan-scores-22m-to-break-into-the-u-s-market/",
         # "http://techcrunch.com/2016/05/11/german-ipad-point-of-sale-startup-orderbird-closes-20m-series-c/",
         # "http://techcrunch.com/2016/05/11/drayson-technologies-raises-8m-for-energy-harvesting-tech-aimed-at-iot-devices-and-wearables/",
         # "http://techcrunch.com/2016/05/10/software-piracy-claims-can-ruin-your-business-and-reward-those-responsible/",
         # "http://techcrunch.com/2016/05/10/the-tc-disrupt-ny-battlefield-finalists-are-bark-beam-bitpagos-ritual-seadrone-and-watero/",
         # "http://techcrunch.com/2016/05/10/3dprintler-lets-you-order-a-3d-print-via-chatbot/",
         # "http://techcrunch.com/2016/05/10/bark-helps-parents-keep-kids-safe-online-without-invading-their-privacy/",
         # "http://techcrunch.com/2016/05/10/seadrone-simplifies-underwater-exploration-and-inspection/",
         # "http://techcrunch.com/2016/05/10/bitpagos-uses-the-blockchain-to-enable-credit-for-online-payments-in-emerging-markets/",
         # "http://techcrunch.com/2016/05/10/homeme-looks-to-help-pre-approve-apartment-hunters-for-rentals/",
         # "http://techcrunch.com/2016/05/10/slack-debuts-sign-in-with-slack-the-collaboration-platforms-answer-to-facebook-connect/",
         # "http://techcrunch.com/2016/05/10/blue-apron-sweetgreen-maple-founders-on-how-to-grow-your-food-startup/",
         # "http://techcrunch.com/2016/05/10/reserve-for-restaurants/"
         ]

results = []

for link in links:

    '''
    creating the list of words from document
    '''

    #request to access webpage
    page = requests.get(link)

    #assign the content of the webpage to soup
    soup = BeautifulSoup(page.content, "html.parser")

    #extract the article to an str variable raw_text
    raw_text = str()
    for hit in soup.findAll("p"):
        raw_text+=str(hit)

    #check the content of raw_text
    # print(raw_text)

    #Modified text stored in a mod_text
    mod_text = str()
    mod_text = re.sub('<.*?>', '', raw_text)

    #check the content of mod_text
    # print(mod_text)

    #split the text into words
    word_text = mod_text.split()

    '''
    removing common words and nouns form the list of words
    '''
    #Tokenize the doc
    words = nltk.word_tokenize(mod_text.strip().lower())

    #stopword free list
    stopwordsfree_words = [word for word in words if word not in stop]
    #Company name free list
    companyfree_words = [word for word in stopwordsfree_words if word not in company_list]
    #Founder name free list
    founderfree_words = [word for word in companyfree_words if word not in founder_list]
    #investor name free list
    investorfree_words = [word for word in founderfree_words if word not in investor_list]
    #city name free list
    cityfree_words = [word for word in investorfree_words if word not in city_list]

    #convert counter to dictionary
    word_count = dict(Counter(cityfree_words))
    #print (word_count)
    results.append(word_count)

print(results)

'''
Creating a list of tags
'''

wb = xlrd.open_workbook('/Users/Ankan/PycharmProjects/Pyprogrammes/tag_list.xlsx')

worksheet = wb.sheet_by_name('Market_list')

tag_excel_list = []

for row in range(1072):
    if worksheet.cell(row,0):
        tag_excel_list.append(worksheet.cell(row,0).value)
    else:
        break

print(tag_excel_list)

# #read a file of tags
# tag_raw = open("/Users/Ankan/PycharmProjects/Pyprogrammes/inc42media.wordpress.2016-05-23.xml" , 'r')
# tag_soup = BeautifulSoup(tag_raw, "lxml")
#
# #print(tag_soup.prettify())
#
# #Strip the tags individually
# stripped_tag_list = list()
# for line in tag_soup.find_all('wp:tag_slug'):
#     stripped_tag_list.append(line.text)


'''
remove common words and noun form a list of tags
'''
tag_word = list()

for w in tag_excel_list:
    tag_word.append(w.replace("/" , " "))

my_tag_list = list()

for wo in tag_word:
    my_tag_list.append(wo.lower())

#print(my_tag_list)
#
# #make tags stopword free
# stopwordsfree_tags = [word for word in tag_words if word not in stop]
# #Company name free list
# companyfree_tags = [word for word in stopwordsfree_tags if word not in company_list]
# #Founder name free list
# founderfree_tags = [word for word in companyfree_tags if word not in founder_list ]
# #investor name free list
# investorfree_tags = [word for word in founderfree_tags if word not in investor_list]
# #city name free list
# cityfree_tags = [word for word in investorfree_tags if word not in city_list]

#my_tag_list = list(set(cityfree_tags))


#Check the tag list
print(my_tag_list)

occurrence_list = list()
cooccurrence_list = list()
p=0
q=0
'''
checking occourance and co-occourance
'''
text_file = open("Output.txt", "w")

tag_tuple = list()
for x in itertools.combinations(my_tag_list, 2):
    tag_tuple.append(x)

#print(tag_tuple)


for doc in results:
    #Check Occurance

    for tag in my_tag_list:
        if doc.get(tag):
            p +=doc.get(tag)
            occurrence_list.append([tag, p])


    #Check Co-Occourance

    for tags in tag_tuple:
        if doc.get(tags[0]) and doc.get(tags[1]):
            q +=min(doc.get(tags[0]),doc.get(tags[1]))
            cooccurrence_list.append([tags[0],tags[1],q])


print(occurrence_list)
print(cooccurrence_list)



x = pd.DataFrame(cooccurrence_list, columns = ["Tag1", "Tag2", "Cooccurance"])

print(x)

x1 = x[['Cooccurance']]

print(x1)

# K Means Cluster
model = KMeans(n_clusters=3)
model.fit(x1)

# This is what KMeans thought
Labels = model.labels_

plt.title('K Mean Classification')

plt.show()






# csv_writer = csv.writer(text_file)
#
# for item in cooccurrence_list:
#     csv_writer.writerow(item)
#     # text_file.write("%s\n" % item)



'''
Network Diagram
'''
#
#
# G = nx.Graph()
# for item in occurrence_list:
#     G.add_node(item[0], weight=item[1])
#
# G.add_weighted_edges_from(cooccurrence_list)
#
# # for item in cooccurrence_list:
# #     for i, j, w in item:
# #         G.add_edge(i, j, weight = w)
#
# pos = nx.random_layout(G)
#
# nodes = G.nodes()
# edges = G.edges()
#
# weights = [G[u][v]['weight'] for u,v in edges]
#
# nx.draw(G, pos, with_labels=nodes, edges=edges, width=weights)
#
# #plt.show()
#
# nx.write_graphml(G,"tags_C_I_154.graphml")
