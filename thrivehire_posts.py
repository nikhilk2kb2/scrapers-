import requests
import base64
import re
from bs4 import BeautifulSoup as bs
import json
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods import taxonomies
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import pandas as pd

locationTaxonomy = [
{"term_taxonomy_id":"24","term_id":"24","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Australia","slug":"australia","term_group":"0"},
{"term_taxonomy_id":"28","term_id":"28","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Canada","slug":"canada","term_group":"0"},
{"term_taxonomy_id":"37","term_id":"37","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"France","slug":"france","term_group":"0"},
{"term_taxonomy_id":"41","term_id":"41","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"India","slug":"india","term_group":"0"},
{"term_taxonomy_id":"56","term_id":"56","taxonomy":"job_location","description":"","parent":"0","count":"7","name":"United Kingdom","slug":"united-kingdom","term_group":"0"},
{"term_taxonomy_id":"57","term_id":"57","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"United States","slug":"united-states","term_group":"0"},
{"term_taxonomy_id":"90","term_id":"90","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Uganda","slug":"uganda","term_group":"0"},
{"term_taxonomy_id":"91","term_id":"91","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mali","slug":"mali","term_group":"0"},
{"term_taxonomy_id":"92","term_id":"92","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Multiple Locations","slug":"multiple-locations","term_group":"0"},
{"term_taxonomy_id":"93","term_id":"93","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"London","slug":"london","term_group":"0"},
{"term_taxonomy_id":"96","term_id":"96","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Afghanistan","slug":"afghanistan","term_group":"0"},
{"term_taxonomy_id":"97","term_id":"97","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Albania","slug":"albania","term_group":"0"},
{"term_taxonomy_id":"98","term_id":"98","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Algeria","slug":"algeria","term_group":"0"},
{"term_taxonomy_id":"99","term_id":"99","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Andorra","slug":"andorra","term_group":"0"},
{"term_taxonomy_id":"100","term_id":"100","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Angola","slug":"angola","term_group":"0"},
{"term_taxonomy_id":"101","term_id":"101","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Antigua and Barbuda","slug":"antigua-and-barbuda","term_group":"0"},
{"term_taxonomy_id":"102","term_id":"102","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Argentina","slug":"argentina","term_group":"0"},
{"term_taxonomy_id":"103","term_id":"103","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Armenia","slug":"armenia","term_group":"0"},
{"term_taxonomy_id":"104","term_id":"104","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Austria","slug":"austria","term_group":"0"},
{"term_taxonomy_id":"105","term_id":"105","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Azerbaijan","slug":"azerbaijan","term_group":"0"},
{"term_taxonomy_id":"106","term_id":"106","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"The Bahamas","slug":"the-bahamas","term_group":"0"},
{"term_taxonomy_id":"107","term_id":"107","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bahrain","slug":"bahrain","term_group":"0"},
{"term_taxonomy_id":"108","term_id":"108","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bangladesh","slug":"bangladesh","term_group":"0"},
{"term_taxonomy_id":"109","term_id":"109","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Barbados","slug":"barbados","term_group":"0"},
{"term_taxonomy_id":"110","term_id":"110","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Belarus","slug":"belarus","term_group":"0"},
{"term_taxonomy_id":"111","term_id":"111","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Belgium","slug":"belgium","term_group":"0"},
{"term_taxonomy_id":"112","term_id":"112","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Belize","slug":"belize","term_group":"0"},
{"term_taxonomy_id":"113","term_id":"113","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Benin","slug":"benin","term_group":"0"},
{"term_taxonomy_id":"114","term_id":"114","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bhutan","slug":"bhutan","term_group":"0"},
{"term_taxonomy_id":"115","term_id":"115","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bolivia","slug":"bolivia","term_group":"0"},
{"term_taxonomy_id":"116","term_id":"116","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bosnia and Herzegovina","slug":"bosnia-and-herzegovina","term_group":"0"},
{"term_taxonomy_id":"117","term_id":"117","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Botswana","slug":"botswana","term_group":"0"},
{"term_taxonomy_id":"118","term_id":"118","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Brazil","slug":"brazil","term_group":"0"},
{"term_taxonomy_id":"119","term_id":"119","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Brunei","slug":"brunei","term_group":"0"},
{"term_taxonomy_id":"120","term_id":"120","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Burkina Faso","slug":"burkina-faso","term_group":"0"},
{"term_taxonomy_id":"121","term_id":"121","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Bulgaria","slug":"bulgaria","term_group":"0"},
{"term_taxonomy_id":"122","term_id":"122","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Burundi","slug":"burundi","term_group":"0"},
{"term_taxonomy_id":"123","term_id":"123","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Cabo Verde","slug":"cabo-verde","term_group":"0"},
{"term_taxonomy_id":"124","term_id":"124","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Cambodia","slug":"cambodia","term_group":"0"},
{"term_taxonomy_id":"125","term_id":"125","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Cameroon","slug":"cameroon","term_group":"0"},
{"term_taxonomy_id":"126","term_id":"126","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Central African Republic","slug":"central-african-republic","term_group":"0"},
{"term_taxonomy_id":"127","term_id":"127","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Chad","slug":"chad","term_group":"0"},
{"term_taxonomy_id":"128","term_id":"128","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Chile","slug":"chile","term_group":"0"},
{"term_taxonomy_id":"129","term_id":"129","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"China","slug":"china","term_group":"0"},
{"term_taxonomy_id":"130","term_id":"130","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Colombia","slug":"colombia","term_group":"0"},
{"term_taxonomy_id":"131","term_id":"131","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Comoros","slug":"comoros","term_group":"0"},
{"term_taxonomy_id":"132","term_id":"132","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Congo, Democratic Republic of the","slug":"congo-democratic-republic-of-the","term_group":"0"},
{"term_taxonomy_id":"133","term_id":"133","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Congo, Republic of the","slug":"congo-republic-of-the","term_group":"0"},
{"term_taxonomy_id":"134","term_id":"134","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Costa Rica","slug":"costa-rica","term_group":"0"},
{"term_taxonomy_id":"135","term_id":"135","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"C\u00f4te d\u2019Ivoire","slug":"cote-divoire","term_group":"0"},
{"term_taxonomy_id":"136","term_id":"136","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Croatia","slug":"croatia","term_group":"0"},
{"term_taxonomy_id":"137","term_id":"137","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Cuba","slug":"cuba","term_group":"0"},
{"term_taxonomy_id":"138","term_id":"138","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Cyprus","slug":"cyprus","term_group":"0"},
{"term_taxonomy_id":"139","term_id":"139","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Czech Republic","slug":"czech-republic","term_group":"0"},
{"term_taxonomy_id":"140","term_id":"140","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Denmark","slug":"denmark","term_group":"0"},
{"term_taxonomy_id":"141","term_id":"141","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Djibouti","slug":"djibouti","term_group":"0"},
{"term_taxonomy_id":"142","term_id":"142","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Dominica","slug":"dominica","term_group":"0"},
{"term_taxonomy_id":"143","term_id":"143","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Dominican Republic","slug":"dominican-republic","term_group":"0"},
{"term_taxonomy_id":"144","term_id":"144","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"East Timor","slug":"east-timor","term_group":"0"},
{"term_taxonomy_id":"145","term_id":"145","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Ecuador","slug":"ecuador","term_group":"0"},
{"term_taxonomy_id":"146","term_id":"146","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Egypt","slug":"egypt","term_group":"0"},
{"term_taxonomy_id":"147","term_id":"147","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"El Salvador","slug":"el-salvador","term_group":"0"},
{"term_taxonomy_id":"148","term_id":"148","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Equatorial Guinea","slug":"equatorial-guinea","term_group":"0"},
{"term_taxonomy_id":"149","term_id":"149","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Eritrea","slug":"eritrea","term_group":"0"},
{"term_taxonomy_id":"150","term_id":"150","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Estonia","slug":"estonia","term_group":"0"},
{"term_taxonomy_id":"151","term_id":"151","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Ethiopia","slug":"ethiopia","term_group":"0"},
{"term_taxonomy_id":"152","term_id":"152","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Fiji","slug":"fiji","term_group":"0"},
{"term_taxonomy_id":"153","term_id":"153","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Finland","slug":"finland","term_group":"0"},
{"term_taxonomy_id":"154","term_id":"154","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Gabon","slug":"gabon","term_group":"0"},
{"term_taxonomy_id":"155","term_id":"155","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"The Gambia","slug":"the-gambia","term_group":"0"},
{"term_taxonomy_id":"156","term_id":"156","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Georgia","slug":"georgia","term_group":"0"},
{"term_taxonomy_id":"157","term_id":"157","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Germany","slug":"germany","term_group":"0"},
{"term_taxonomy_id":"158","term_id":"158","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Ghana","slug":"ghana","term_group":"0"},
{"term_taxonomy_id":"159","term_id":"159","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Greece","slug":"greece","term_group":"0"},
{"term_taxonomy_id":"160","term_id":"160","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Grenada","slug":"grenada","term_group":"0"},
{"term_taxonomy_id":"161","term_id":"161","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Guatemala","slug":"guatemala","term_group":"0"},
{"term_taxonomy_id":"162","term_id":"162","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Guinea","slug":"guinea","term_group":"0"},
{"term_taxonomy_id":"163","term_id":"163","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Guinea-Bissau","slug":"guinea-bissau","term_group":"0"},
{"term_taxonomy_id":"164","term_id":"164","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Guyana","slug":"guyana","term_group":"0"},
{"term_taxonomy_id":"165","term_id":"165","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Haiti","slug":"haiti","term_group":"0"},
{"term_taxonomy_id":"166","term_id":"166","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Honduras","slug":"honduras","term_group":"0"},
{"term_taxonomy_id":"167","term_id":"167","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Hungary","slug":"hungary","term_group":"0"},
{"term_taxonomy_id":"168","term_id":"168","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Iceland","slug":"iceland","term_group":"0"},
{"term_taxonomy_id":"169","term_id":"169","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Indonesia","slug":"indonesia","term_group":"0"},
{"term_taxonomy_id":"170","term_id":"170","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Iran","slug":"iran","term_group":"0"},
{"term_taxonomy_id":"171","term_id":"171","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Iraq","slug":"iraq","term_group":"0"},
{"term_taxonomy_id":"172","term_id":"172","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Ireland","slug":"ireland","term_group":"0"},
{"term_taxonomy_id":"173","term_id":"173","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Israel","slug":"israel","term_group":"0"},
{"term_taxonomy_id":"174","term_id":"174","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Italy","slug":"italy","term_group":"0"},
{"term_taxonomy_id":"175","term_id":"175","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Jamaica","slug":"jamaica","term_group":"0"},
{"term_taxonomy_id":"176","term_id":"176","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Japan","slug":"japan","term_group":"0"},
{"term_taxonomy_id":"177","term_id":"177","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Jordan","slug":"jordan","term_group":"0"},
{"term_taxonomy_id":"178","term_id":"178","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kazakhstan","slug":"kazakhstan","term_group":"0"},
{"term_taxonomy_id":"179","term_id":"179","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kenya","slug":"kenya","term_group":"0"},
{"term_taxonomy_id":"180","term_id":"180","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kiribati","slug":"kiribati","term_group":"0"},
{"term_taxonomy_id":"181","term_id":"181","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Korea, North","slug":"korea-north","term_group":"0"},
{"term_taxonomy_id":"182","term_id":"182","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Korea, South","slug":"korea-south","term_group":"0"},
{"term_taxonomy_id":"183","term_id":"183","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kosovo","slug":"kosovo","term_group":"0"},
{"term_taxonomy_id":"184","term_id":"184","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kuwait","slug":"kuwait","term_group":"0"},
{"term_taxonomy_id":"185","term_id":"185","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Kyrgyzstan","slug":"kyrgyzstan","term_group":"0"},
{"term_taxonomy_id":"186","term_id":"186","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Laos","slug":"laos","term_group":"0"},
{"term_taxonomy_id":"187","term_id":"187","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Latvia","slug":"latvia","term_group":"0"},
{"term_taxonomy_id":"188","term_id":"188","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Lebanon","slug":"lebanon","term_group":"0"},
{"term_taxonomy_id":"189","term_id":"189","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Lesotho","slug":"lesotho","term_group":"0"},
{"term_taxonomy_id":"190","term_id":"190","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Liberia","slug":"liberia","term_group":"0"},
{"term_taxonomy_id":"191","term_id":"191","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Libya","slug":"libya","term_group":"0"},
{"term_taxonomy_id":"192","term_id":"192","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Liechtenstein","slug":"liechtenstein","term_group":"0"},
{"term_taxonomy_id":"193","term_id":"193","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Lithuania","slug":"lithuania","term_group":"0"},
{"term_taxonomy_id":"194","term_id":"194","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Luxembourg","slug":"luxembourg","term_group":"0"},
{"term_taxonomy_id":"195","term_id":"195","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Macedonia","slug":"macedonia","term_group":"0"},
{"term_taxonomy_id":"196","term_id":"196","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Madagascar","slug":"madagascar","term_group":"0"},
{"term_taxonomy_id":"197","term_id":"197","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Malawi","slug":"malawi","term_group":"0"},
{"term_taxonomy_id":"198","term_id":"198","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Malaysia","slug":"malaysia","term_group":"0"},
{"term_taxonomy_id":"199","term_id":"199","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Maldives","slug":"maldives","term_group":"0"},
{"term_taxonomy_id":"200","term_id":"200","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Malta","slug":"malta","term_group":"0"},
{"term_taxonomy_id":"201","term_id":"201","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Marshall Islands","slug":"marshall-islands","term_group":"0"},
{"term_taxonomy_id":"202","term_id":"202","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mauritania","slug":"mauritania","term_group":"0"},
{"term_taxonomy_id":"203","term_id":"203","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mauritius","slug":"mauritius","term_group":"0"},
{"term_taxonomy_id":"204","term_id":"204","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mexico","slug":"mexico","term_group":"0"},
{"term_taxonomy_id":"205","term_id":"205","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Micronesia, Federated States of","slug":"micronesia-federated-states-of","term_group":"0"},
{"term_taxonomy_id":"206","term_id":"206","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Moldova","slug":"moldova","term_group":"0"},
{"term_taxonomy_id":"207","term_id":"207","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Monaco","slug":"monaco","term_group":"0"},
{"term_taxonomy_id":"208","term_id":"208","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mongolia","slug":"mongolia","term_group":"0"},
{"term_taxonomy_id":"209","term_id":"209","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Montenegro","slug":"montenegro","term_group":"0"},
{"term_taxonomy_id":"210","term_id":"210","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Morocco","slug":"morocco","term_group":"0"},
{"term_taxonomy_id":"211","term_id":"211","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Mozambique","slug":"mozambique","term_group":"0"},
{"term_taxonomy_id":"212","term_id":"212","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Myanmar","slug":"myanmar","term_group":"0"},
{"term_taxonomy_id":"213","term_id":"213","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Namibia","slug":"namibia","term_group":"0"},
{"term_taxonomy_id":"214","term_id":"214","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Nauru","slug":"nauru","term_group":"0"},
{"term_taxonomy_id":"215","term_id":"215","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Nepal","slug":"nepal","term_group":"0"},
{"term_taxonomy_id":"216","term_id":"216","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Netherlands","slug":"netherlands","term_group":"0"},
{"term_taxonomy_id":"217","term_id":"217","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"New Zealand","slug":"new-zealand","term_group":"0"},
{"term_taxonomy_id":"218","term_id":"218","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Nicaragua","slug":"nicaragua","term_group":"0"},
{"term_taxonomy_id":"219","term_id":"219","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Niger","slug":"niger","term_group":"0"},
{"term_taxonomy_id":"220","term_id":"220","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Nigeria","slug":"nigeria","term_group":"0"},
{"term_taxonomy_id":"221","term_id":"221","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Norway","slug":"norway","term_group":"0"},
{"term_taxonomy_id":"222","term_id":"222","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Oman","slug":"oman","term_group":"0"},
{"term_taxonomy_id":"223","term_id":"223","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Pakistan","slug":"pakistan","term_group":"0"},
{"term_taxonomy_id":"224","term_id":"224","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Palau","slug":"palau","term_group":"0"},
{"term_taxonomy_id":"225","term_id":"225","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Panama","slug":"panama","term_group":"0"},
{"term_taxonomy_id":"226","term_id":"226","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Papua New Guinea","slug":"papua-new-guinea","term_group":"0"},
{"term_taxonomy_id":"227","term_id":"227","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Paraguay","slug":"paraguay","term_group":"0"},
{"term_taxonomy_id":"228","term_id":"228","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Peru","slug":"peru","term_group":"0"},
{"term_taxonomy_id":"229","term_id":"229","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Philippines","slug":"philippines","term_group":"0"},
{"term_taxonomy_id":"230","term_id":"230","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Poland","slug":"poland","term_group":"0"},
{"term_taxonomy_id":"231","term_id":"231","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Portugal","slug":"portugal","term_group":"0"},
{"term_taxonomy_id":"232","term_id":"232","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Qatar","slug":"qatar","term_group":"0"},
{"term_taxonomy_id":"233","term_id":"233","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Romania","slug":"romania","term_group":"0"},
{"term_taxonomy_id":"234","term_id":"234","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Russia","slug":"russia","term_group":"0"},
{"term_taxonomy_id":"235","term_id":"235","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Rwanda","slug":"rwanda","term_group":"0"},
{"term_taxonomy_id":"236","term_id":"236","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Saint Kitts and Nevis","slug":"saint-kitts-and-nevis","term_group":"0"},
{"term_taxonomy_id":"237","term_id":"237","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Saint Lucia","slug":"saint-lucia","term_group":"0"},
{"term_taxonomy_id":"238","term_id":"238","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Saint Vincent and the Grenadines","slug":"saint-vincent-and-the-grenadines","term_group":"0"},
{"term_taxonomy_id":"239","term_id":"239","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Samoa","slug":"samoa","term_group":"0"},
{"term_taxonomy_id":"240","term_id":"240","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"San Marino","slug":"san-marino","term_group":"0"},
{"term_taxonomy_id":"241","term_id":"241","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sao Tome and Principe","slug":"sao-tome-and-principe","term_group":"0"},
{"term_taxonomy_id":"242","term_id":"242","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Saudi Arabia","slug":"saudi-arabia","term_group":"0"},
{"term_taxonomy_id":"243","term_id":"243","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Senegal","slug":"senegal","term_group":"0"},
{"term_taxonomy_id":"244","term_id":"244","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Serbia","slug":"serbia","term_group":"0"},
{"term_taxonomy_id":"245","term_id":"245","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Seychelles","slug":"seychelles","term_group":"0"},
{"term_taxonomy_id":"246","term_id":"246","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sierra Leone","slug":"sierra-leone","term_group":"0"},
{"term_taxonomy_id":"247","term_id":"247","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Singapore","slug":"singapore","term_group":"0"},
{"term_taxonomy_id":"248","term_id":"248","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Slovakia","slug":"slovakia","term_group":"0"},
{"term_taxonomy_id":"249","term_id":"249","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Slovenia","slug":"slovenia","term_group":"0"},
{"term_taxonomy_id":"250","term_id":"250","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Solomon Islands","slug":"solomon-islands","term_group":"0"},
{"term_taxonomy_id":"251","term_id":"251","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Somalia","slug":"somalia","term_group":"0"},
{"term_taxonomy_id":"252","term_id":"252","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"South Africa","slug":"south-africa","term_group":"0"},
{"term_taxonomy_id":"253","term_id":"253","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Spain","slug":"spain","term_group":"0"},
{"term_taxonomy_id":"254","term_id":"254","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sri Lanka","slug":"sri-lanka","term_group":"0"},
{"term_taxonomy_id":"255","term_id":"255","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sudan","slug":"sudan","term_group":"0"},
{"term_taxonomy_id":"256","term_id":"256","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sudan, South","slug":"sudan-south","term_group":"0"},
{"term_taxonomy_id":"257","term_id":"257","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Suriname","slug":"suriname","term_group":"0"},
{"term_taxonomy_id":"258","term_id":"258","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Swaziland","slug":"swaziland","term_group":"0"},
{"term_taxonomy_id":"259","term_id":"259","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Sweden","slug":"sweden","term_group":"0"},
{"term_taxonomy_id":"260","term_id":"260","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Switzerland","slug":"switzerland","term_group":"0"},
{"term_taxonomy_id":"261","term_id":"261","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Syria","slug":"syria","term_group":"0"},
{"term_taxonomy_id":"262","term_id":"262","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Taiwan","slug":"taiwan","term_group":"0"},
{"term_taxonomy_id":"263","term_id":"263","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Tajikistan","slug":"tajikistan","term_group":"0"},
{"term_taxonomy_id":"264","term_id":"264","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Tanzania","slug":"tanzania","term_group":"0"},
{"term_taxonomy_id":"265","term_id":"265","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Thailand","slug":"thailand","term_group":"0"},
{"term_taxonomy_id":"266","term_id":"266","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Togo","slug":"togo","term_group":"0"},
{"term_taxonomy_id":"267","term_id":"267","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Tonga","slug":"tonga","term_group":"0"},
{"term_taxonomy_id":"268","term_id":"268","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Trinidad and Tobago","slug":"trinidad-and-tobago","term_group":"0"},
{"term_taxonomy_id":"269","term_id":"269","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Tunisia","slug":"tunisia","term_group":"0"},
{"term_taxonomy_id":"270","term_id":"270","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Turkey","slug":"turkey","term_group":"0"},
{"term_taxonomy_id":"271","term_id":"271","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Turkmenistan","slug":"turkmenistan","term_group":"0"},
{"term_taxonomy_id":"272","term_id":"272","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Tuvalu","slug":"tuvalu","term_group":"0"},
{"term_taxonomy_id":"273","term_id":"273","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Ukraine","slug":"ukraine","term_group":"0"},
{"term_taxonomy_id":"274","term_id":"274","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"United Arab Emirates","slug":"united-arab-emirates","term_group":"0"},
{"term_taxonomy_id":"275","term_id":"275","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Uruguay","slug":"uruguay","term_group":"0"},
{"term_taxonomy_id":"276","term_id":"276","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Uzbekistan","slug":"uzbekistan","term_group":"0"},
{"term_taxonomy_id":"277","term_id":"277","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Vanuatu","slug":"vanuatu","term_group":"0"},
{"term_taxonomy_id":"278","term_id":"278","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Vatican City","slug":"vatican-city","term_group":"0"},
{"term_taxonomy_id":"279","term_id":"279","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Venezuela","slug":"venezuela","term_group":"0"},
{"term_taxonomy_id":"280","term_id":"280","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Vietnam","slug":"vietnam","term_group":"0"},
{"term_taxonomy_id":"281","term_id":"281","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Yemen","slug":"yemen","term_group":"0"},
{"term_taxonomy_id":"282","term_id":"282","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Zambia","slug":"zambia","term_group":"0"},
{"term_taxonomy_id":"283","term_id":"283","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"Zimbabwe","slug":"zimbabwe","term_group":"0"},
{"term_taxonomy_id":"284","term_id":"284","taxonomy":"job_location","description":"","parent":"0","count":"0","name":"xxxxxxx","slug":"xxxxxxx","term_group":"0"}
]

class Job:
    def __init__(self):
        self.id = ""
        self.location = ""
        self.title = ""
        self.description = ""
        self.category = ""
        self.type = ""
        self.salary = ""
        self.experience = ""
        self.url = ""
        self.organisation = ""


def connectWP():
    #print("Enter a password:")
    ####password = input()
    print('Connecting to WP')
    wp = Client('https://www.globalhealthjobs.com/xmlrpc.php', u'V-Scrape-Bot', u'HesloProVyvoj@2018')
    
    return wp

def getExistingPosts(wp):
    posts = wp.call(GetPosts({'post_type': 'noo_job', 'number': 100}))
    return posts

def jobExists(job, posts):
    for title in posts:
        if job["title"] == str(title):
            print("Job "+ job["title"] + " already exists")
            return True
        else:
            return False

def getSalaryRange(salary):
    formatSalary = salary.replace(',', '')
    salary = [float(s) for s in re.findall(r'\d+\.?\d*', formatSalary)][0]

    if salary in range(0,15000):
        salaryRange = "0-15000"
    elif salary in range(15001,20000):
        salaryRange = "15000-20000"
    elif salary in range(20001,30000):
        salaryRange = "20000-30000"
    elif salary in range(30001,50000):
        salaryRange = "30000-50000"
    elif salary in range(50001,100000):
        salaryRange = "30000-50000"
    elif salary > 100001:
        salaryRange = "100000"
    else:
        salaryRange = "poa"
    return salaryRange

def getLocationtaxonomy(loc):
    for l in locationTaxonomy:
        if l['name'] == loc:
            locationId = l['term_id']
            break
        else:
            locationId = 284
    return int(locationId)

def postJob(job, wp):
    print('----------')
    print('Post job ' + job["title"])
    wpJob = WordPressPost()
    #Post type
    wpJob.post_type = 'noo_job'
    #Post content
    wpJob.title = str(job["title"])
    wpJob.content = str(job["description"])

    #Custom fields
    wpJob.custom_fields = []
    wpJob.custom_fields.append({"key" : '_featured', "value" : "no"})
    wpJob.custom_fields.append({"key" : '_layout_style', "value" : "default"})
    wpJob.custom_fields.append({"key" : "_job_sidebar", "value" : "sidebar"})
    wpJob.custom_fields.append({"key" : "_custom_application_url", "value" : str(job["link"])})

    wpJob.custom_fields.append({"key" : "_noo_views_count", "value" : "0"}),
    wpJob.custom_fields.append({"key" : "_noo_job_applications_count", "value" : "0"})

    location = getLocationtaxonomy(job['location'])

    jobLocation =  wp.call(taxonomies.GetTerm("job_location", location))

    wpJob.terms = []
    wpJob.terms.append(jobLocation)

    print('Sending...')
    wpJob.id = wp.call(NewPost(wpJob))

    print(job["title"] + " posted with ID " + wpJob.id)


def main():
    print('start app')

    wp = connectWP()

    posts = getExistingPosts(wp)

    df = pd.read_csv('thrivehire_data.csv', sep='|')
    count = 0

    for i in range(0, len(df)):
        count += 1
        if jobExists(df.loc[i], posts):
            pass
        else:
            try:
                postJob(df.loc[i], wp)
            except Exception as e:
                print('connection to Wordpress failed')
                print(e)
                pass

        print(count)
       
    
if __name__ == "__main__":
    main()

