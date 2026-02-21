#!/usr/bin/env python3
"""
Script to update all city JSON files with comprehensive cuisine data
"""

import json
import os

# Load cuisine data
cuisine_data = {
    "beijing": {
        "signature_dishes": [
            {"name": "Peking Duck (北京烤鸭)", "description": "Crispy skin duck served with thin pancakes, hoisin sauce, and scallions"},
            {"name": "Zhajiangmian (炸酱面)", "description": "Noodles with fermented soybean paste, vegetables, and minced pork"},
            {"name": "Jianbing (煎饼)", "description": "Crispy breakfast crepe with egg, cilantro, and crunchy cracker"},
            {"name": "Chuan'r (串儿)", "description": "Grilled lamb skewers with cumin and chili"},
            {"name": "Baozi (包子)", "description": "Steamed buns filled with pork, vegetables, or sweet bean paste"}
        ],
        "street_food": ["Jianbing", "Chuan'r", "Tanghulu", "Douzhi", "Lǘdagun"],
        "famous_restaurants": ["Quanjude", "Bianyifang", "Huguosi Snack Bar"]
    },
    "shanghai": {
        "signature_dishes": [
            {"name": "Xiaolongbao (小笼包)", "description": "Soup dumplings with pork filling and hot broth inside"},
            {"name": "Shengjianbao (生煎包)", "description": "Pan-fried pork buns with crispy bottom and juicy filling"},
            {"name": "Hongshao Rou (红烧肉)", "description": "Braised pork belly in soy sauce and sugar"},
            {"name": "Scallion Oil Noodles (葱油拌面)", "description": "Simple noodles tossed with fragrant scallion oil"},
            {"name": "Beggar's Chicken (叫花鸡)", "description": "Whole chicken stuffed with herbs and baked in clay"}
        ],
        "street_food": ["Shengjianbao", "Cifantuan", "Da Bing", "You Tiao"],
        "famous_restaurants": ["Jia Jia Tang Bao", "Yang's Fry Dumpling", "Lu Bo Lang"]
    },
    "guangzhou": {
        "signature_dishes": [
            {"name": "Dim Sum (点心)", "description": "Variety of small dishes including har gow, siu mai, and char siu bao"},
            {"name": "White Cut Chicken (白切鸡)", "description": "Poached chicken served with ginger-scallion sauce"},
            {"name": "Char Siu (叉烧)", "description": "Barbecued pork with sweet maltose glaze"},
            {"name": "Wonton Noodles (云吞面)", "description": "Egg noodles with shrimp wontons in clear broth"},
            {"name": "Cantonese Roast Goose (烧鹅)", "description": "Crispy skin goose with sweet plum sauce"}
        ],
        "street_food": ["Cheung Fun", "Egg Tarts", "Fish Balls", "Double Skin Milk"],
        "famous_restaurants": ["Panxi Restaurant", "Lianxianglou", "Taotaoju"]
    },
    "shenzhen": {
        "signature_dishes": [
            {"name": "Seafood Hotpot (海鲜火锅)", "description": "Fresh seafood cooked at table in flavorful broth"},
            {"name": "Claypot Rice (煲仔饭)", "description": "Rice with toppings cooked in clay pot with crispy bottom"},
            {"name": "Oyster Omelette (蚝仔烙)", "description": "Crispy omelette with fresh oysters"},
            {"name": "Cantonese BBQ (烧腊)", "description": "Assorted roasted meats including duck, pork, and chicken"},
            {"name": "Dim Sum (早茶)", "description": "Morning tea with variety of steamed and fried dishes"}
        ],
        "street_food": ["Fish Balls", "Stinky Tofu", "Egg Waffles", "Bubble Tea"],
        "famous_restaurants": ["Spring Bamboo", "The Kitchen", "Tequila Coyote's"]
    },
    "chengdu": {
        "signature_dishes": [
            {"name": "Sichuan Hot Pot (四川火锅)", "description": "Spicy bubbling broth with various meats and vegetables"},
            {"name": "Mapo Tofu (麻婆豆腐)", "description": "Soft tofu in spicy sauce with minced pork and Sichuan pepper"},
            {"name": "Kung Pao Chicken (宫保鸡丁)", "description": "Diced chicken with peanuts, chili, and Sichuan peppercorns"},
            {"name": "Dan Dan Noodles (担担面)", "description": "Noodles in spicy sesame and peanut sauce"},
            {"name": "Chuan Chuan Xiang (串串香)", "description": "Skewered ingredients cooked in spicy hot pot broth"}
        ],
        "street_food": ["Chuan Chuan", "Rabbit Heads", "Ice Jelly", "Egg Baked Cake"],
        "famous_restaurants": ["Chen Mapo Tofu", "Shu Jiu Xiang", "Long Chao Shou"]
    },
    "hangzhou": {
        "signature_dishes": [
            {"name": "Dongpo Pork (东坡肉)", "description": "Braised pork belly with soy sauce and rock sugar"},
            {"name": "West Lake Fish in Vinegar (西湖醋鱼)", "description": "Fresh grass carp in sweet and sour sauce"},
            {"name": "Longjing Shrimp (龙井虾仁)", "description": "Stir-fried shrimp with Longjing tea leaves"},
            {"name": "Beggar's Chicken (叫花鸡)", "description": "Chicken stuffed with herbs and baked in lotus leaves"},
            {"name": "Bamboo Shoot Soup (腌笃鲜)", "description": "Soup with bamboo shoots, pork, and salted ham"}
        ],
        "street_food": ["Shengjian", "Cong Bao Hui", "Pian Er Chuan", "You Mao Er"],
        "famous_restaurants": ["Lou Wai Lou", "Zhi Wei Guan", "Kui Yuan Guan"]
    },
    "wuhan": {
        "signature_dishes": [
            {"name": "Hot Dry Noodles (热干面)", "description": "Sesame paste noodles, Wuhan's signature breakfast"},
            {"name": "Wuchang Fish (武昌鱼)", "description": "Steamed fish with chili and fermented black beans"},
            {"name": "Doupi (豆皮)", "description": "Pan-fried bean skin with sticky rice and pork"},
            {"name": "Mian Wo (面窝)", "description": "Crispy fried dough with scallions"},
            {"name": "Jingwu Duck (精武鸭脖)", "description": "Spicy braised duck neck"}
        ],
        "street_food": ["Hot Dry Noodles", "Xiaolongbao", "Fried Dumplings", "Rice Wine"],
        "famous_restaurants": ["Cai Lin Ji", "Lao Tong Cheng", "Xiao Tao Yuan"]
    },
    "xian": {
        "signature_dishes": [
            {"name": "Roujiamo (肉夹馍)", "description": "Chinese hamburger with braised pork in crispy bread"},
            {"name": "Yangrou Paomo (羊肉泡馍)", "description": "Mutton soup with hand-torn flatbread"},
            {"name": "Biangbiang Noodles (biangbiang面)", "description": "Wide, hand-pulled noodles with chili oil"},
            {"name": "Liangpi (凉皮)", "description": "Cold skin noodles with sesame sauce and chili"},
            {"name": "Hulutou (葫芦头)", "description": "Pork intestine soup with bread"}
        ],
        "street_food": ["Roujiamo", "Yangrou Paomo", "Liangpi", "Persimmon Cake"],
        "famous_restaurants": ["Lao Tong Guan", "De Fa Chang", "Jia San"]
    },
    "nanjing": {
        "signature_dishes": [
            {"name": "Salted Duck (盐水鸭)", "description": "Cold poached duck with subtle salt flavor"},
            {"name": "Duck Blood Soup (鸭血粉丝汤)", "description": "Vermicelli soup with duck blood and organs"},
            {"name": "Lion's Head Meatballs (狮子头)", "description": "Large pork meatballs with vegetables"},
            {"name": "Nanjing Roast Duck (南京烤鸭)", "description": "Crispy duck with sweet bean sauce"},
            {"name": "Tofu Dumplings (豆腐涝)", "description": "Soft tofu with savory toppings"}
        ],
        "street_food": ["Salted Duck", "Sesame Pancake", "Tofu Dumplings", "Sugar Porridge"],
        "famous_restaurants": ["De Ji", "Ma Xiang Xing", "Liu Feng Ju"]
    },
    "chongqing": {
        "signature_dishes": [
            {"name": "Chongqing Hot Pot (重庆火锅)", "description": "Fiery hot pot with Sichuan pepper and chili oil"},
            {"name": "Spicy Chicken (辣子鸡)", "description": "Fried chicken buried in mountain of dried chilies"},
            {"name": "Chuan Chuan (串串)", "description": "Skewered ingredients in spicy broth"},
            {"name": "Xiaomian (小面)", "description": "Spicy noodles with numbing Sichuan pepper"},
            {"name": "Mao Xue Wang (毛血旺)", "description": "Spicy duck blood soup with various ingredients"}
        ],
        "street_food": ["Xiaomian", "Chuan Chuan", "Spicy Rabbit", "Fried Potatoes"],
        "famous_restaurants": ["Qi Qi Hot Pot", "Hua Shi Wan", "Qin Ma"]
    },
    "tianjin": {
        "signature_dishes": [
            {"name": "Goubuli Baozi (狗不理包子)", "description": "Famous steamed buns with 18 pleats"},
            {"name": "Jianbing Guozi (煎饼果子)", "description": "Crispy crepe with fried cracker inside"},
            {"name": "Ear-Hole Fried Cake (耳朵眼炸糕)", "description": "Sweet fried glutinous rice cake"},
            {"name": "Mahua (麻花)", "description": "Twisted crispy fried dough sticks"},
            {"name": "Caobing (槽糕)", "description": "Traditional steamed sponge cake"}
        ],
        "street_food": ["Jianbing", "Mahua", "Fried Cake", "Tanghulu"],
        "famous_restaurants": ["Goubuli", "Shi Ba Jie", "Er Duo Yan"]
    },
    "suzhou": {
        "signature_dishes": [
            {"name": "Squirrel Fish (松鼠桂鱼)", "description": "Deep-fried fish in sweet and sour sauce"},
            {"name": "Biluochun Shrimp (碧螺虾仁)", "description": "Shrimp with local Biluochun tea"},
            {"name": "Sweet and Sour Pork (糖醋排骨)", "description": "Tender pork ribs in sweet and sour glaze"},
            {"name": "Osmanthus Cake (桂花糕)", "description": "Sweet rice cake with osmanthus flowers"},
            {"name": "Suzhou Noodles (苏式面)", "description": "Delicate noodles with various toppings"}
        ],
        "street_food": ["Osmanthus Cake", "Suzhou Noodles", "Green Dumplings", "Sugar Porridge"],
        "famous_restaurants": ["De Yue Lou", "Song He Lou", "De Tai Feng"]
    },
    "qingdao": {
        "signature_dishes": [
            {"name": "Seafood Feast (海鲜大餐)", "description": "Fresh local seafood including clams, oysters, and fish"},
            {"name": "Tsingtao Beer (青岛啤酒)", "description": "World-famous local lager beer"},
            {"name": "Stewed Clams (辣炒蛤蜊)", "description": "Spicy stir-fried clams with chili"},
            {"name": "Sea Cucumber (葱烧海参)", "description": "Braised sea cucumber with scallions"},
            {"name": "Qingdao Dumplings (青岛饺子)", "description": "Fresh seafood-filled dumplings"}
        ],
        "street_food": ["Grilled Seafood", "Beer Snacks", "Clams", "Squid"],
        "famous_restaurants": ["Chunhe Lou", "Wanhechun", "Da Huai Shu"]
    },
    "harbin": {
        "signature_dishes": [
            {"name": "Guo Bao Rou (锅包肉)", "description": "Sweet and sour crispy pork slices"},
            {"name": "Harbin Sausage (哈尔滨红肠)", "description": "Smoked Russian-style sausage"},
            {"name": "Stewed Chicken with Mushrooms (小鸡炖蘑菇)", "description": "Hearty chicken stew with wild mushrooms"},
            {"name": "Braised Pork with Vermicelli (猪肉炖粉条)", "description": "Pork belly with glass noodles"},
            {"name": "Russian Bread (大列巴)", "description": "Large dense rye bread"}
        ],
        "street_food": ["Grilled Cold Noodles", "Sugar Gourd", "Ice Cream", "Sausage"],
        "famous_restaurants": ["Lao Chang Chun", "Hua Mei", "Da Lie Ba"]
    },
    "hongkong": {
        "signature_dishes": [
            {"name": "Dim Sum (点心)", "description": "Variety of steamed and fried small dishes"},
            {"name": "Roast Goose (烧鹅)", "description": "Crispy Cantonese-style roast goose"},
            {"name": "Wonton Noodles (云吞面)", "description": "Shrimp wontons in egg noodle soup"},
            {"name": "Egg Tart (蛋挞)", "description": "Flaky pastry with creamy egg custard"},
            {"name": "Pineapple Bun (菠萝包)", "description": "Sweet bun with crispy sugar topping"}
        ],
        "street_food": ["Egg Waffles", "Fish Balls", "Stinky Tofu", "Milk Tea"],
        "famous_restaurants": ["Yung Kee", "Tim Ho Wan", "One Dim Sum"]
    },
    "kunming": {
        "signature_dishes": [
            {"name": "Crossing Bridge Noodles (过桥米线)", "description": "Rice noodle soup with ingredients added at table"},
            {"name": "Steam Pot Chicken (汽锅鸡)", "description": "Chicken steamed in special clay pot"},
            {"name": "Yunnan Rice Noodles (小锅米线)", "description": "Spicy rice noodles in small copper pot"},
            {"name": "Wild Mushroom Hot Pot (野生菌火锅)", "description": "Seasonal wild mushroom hot pot"},
            {"name": "Er Kuai (饵块)", "description": "Rice cakes with various fillings"}
        ],
        "street_food": ["Rice Noodles", "Grilled Tofu", "Flower Cake", "Dairy Fan"],
        "famous_restaurants": ["Jian Xin Yuan", "Fu Zhao Lou", "Lao Fang Zi"]
    },
    "xiamen": {
        "signature_dishes": [
            {"name": "Oyster Omelette (海蛎煎)", "description": "Crispy omelette with fresh oysters"},
            {"name": "Satay Noodles (沙茶面)", "description": "Noodles in spicy peanut satay sauce"},
            {"name": "Peanut Soup (花生汤)", "description": "Sweet creamy peanut soup"},
            {"name": "Fish Balls (鱼丸汤)", "description": "Handmade fish balls in clear soup"},
            {"name": "Spring Roll (春卷)", "description": "Crispy rolls with vegetable filling"}
        ],
        "street_food": ["Oyster Omelette", "Shacha Noodles", "Tusu Jelly", "Meat Wraps"],
        "famous_restaurants": ["Wu Zai Tian", "Hao Qing Xiang", "Lao Xiamen"]
    },
    "dali": {
        "signature_dishes": [
            {"name": "Dali Clay Pot Fish (大理砂锅鱼)", "description": "Fish stewed in clay pot with tofu and vegetables"},
            {"name": "Rushan (乳扇)", "description": "Fried cheese made from cow's milk"},
            {"name": "Bai Ethnic Sour Fish (白族酸辣鱼)", "description": "Sour and spicy fish with papaya"},
            {"name": "Crossing Bridge Noodles (过桥米线)", "description": "Local version of famous Yunnan noodles"},
            {"name": "Wild Mushroom Hot Pot (野生菌火锅)", "description": "Seasonal mushroom hot pot"}
        ],
        "street_food": ["Rushan", "Grilled Erkuai", "Rose Cake", "Yogurt"],
        "famous_restaurants": ["Yang Can Zi", "Mei Zi Jing", "Xiao Pi Jiu"]
    },
    "datong": {
        "signature_dishes": [
            {"name": "Datong Knife-Cut Noodles (大同刀削面)", "description": "Hand-cut noodles with savory sauce"},
            {"name": "Stuffed Duck (大同扒肉条)", "description": "Braised pork belly slices"},
            {"name": "Fried Dough Twists (大同麻花)", "description": "Crispy twisted fried dough"},
            {"name": "Sour Porridge (酸粥)", "description": "Fermented millet porridge"},
            {"name": "Yanggao Apricot (阳高杏脯)", "description": "Dried apricots from Yanggao county"}
        ],
        "street_food": ["Knife-Cut Noodles", "Fried Dough", "Apricots", "Sour Porridge"],
        "famous_restaurants": ["Liu Yuan", "Hua Mei", "De Yi Ju"]
    },
    "guilin": {
        "signature_dishes": [
            {"name": "Guilin Rice Noodles (桂林米粉)", "description": "Rice noodles with braised meat and pickled vegetables"},
            {"name": "Beer Fish (啤酒鱼)", "description": "Fresh river fish cooked with beer"},
            {"name": "Stuffed Li River Snails (田螺酿)", "description": "Snails stuffed with pork and mint"},
            {"name": "Oil Tea (油茶)", "description": "Traditional tea with fried rice and peanuts"},
            {"name": "Bamboo Rice (竹筒饭)", "description": "Rice cooked in fresh bamboo tubes"}
        ],
        "street_food": ["Rice Noodles", "Stuffed Snails", "Water Chestnut Cake", "Taro Cake"],
        "famous_restaurants": ["Chong Shan Mi Fen", "Xie San Jie", "Lao Dong Jiang"]
    },
    "guiyang": {
        "signature_dishes": [
            {"name": "Sour Soup Fish (酸汤鱼)", "description": "Fish in sour tomato-based soup"},
            {"name": "Siwawa (丝娃娃)", "description": "Vegetable wraps with spicy dipping sauce"},
            {"name": "Changwang Noodles (肠旺面)", "description": "Noodles with pork intestines and blood"},
            {"name": "La Rou (腊肉)", "description": "Smoked and cured pork"},
            {"name": "Spicy Chicken (辣子鸡)", "description": "Fried chicken with chili and Sichuan pepper"}
        ],
        "street_food": ["Siwawa", "Tofu Balls", "Rice Tofu", "Grilled Tofu"],
        "famous_restaurants": ["Lao Kai Li", "Yang Ming Can", "He Ji"]
    },
    "jinan": {
        "signature_dishes": [
            {"name": "Sweet and Sour Carp (糖醋鲤鱼)", "description": "Yellow River carp in sweet and sour sauce"},
            {"name": "Braised Intestines (九转大肠)", "description": "Pork intestines braised with spices"},
            {"name": "Jinan Dumplings (济南饺子)", "description": "Handmade dumplings with various fillings"},
            {"name": "Oil Spinach (油旋)", "description": "Layered flaky scallion bread"},
            {"name": "Yellow River Carp (黄河鲤鱼)", "description": "Fresh carp from the Yellow River"}
        ],
        "street_food": ["Oil Spinach", "Sweet Foam", "Roujiamo", "Tofu Jelly"],
        "famous_restaurants": ["De Xing She", "Yan Xi", "Ju Feng De"]
    },
    "kaifeng": {
        "signature_dishes": [
            {"name": "Kaifeng Dumplings (开封灌汤包)", "description": "Soup-filled dumplings with pork filling"},
            {"name": "Peanut Cake (花生糕)", "description": "Crispy peanut candy"},
            {"name": "Almond Tea (杏仁茶)", "description": "Sweet almond-flavored drink"},
            {"name": "Bucket Chicken (桶子鸡)", "description": "Braised chicken in special sauce"},
            {"name": "Sweet Potato Noodles (红薯面条)", "description": "Noodles made from sweet potato starch"}
        ],
        "street_food": ["Dumplings", "Peanut Cake", "Almond Tea", "Rice Cakes"],
        "famous_restaurants": ["Di Yi Lou", "Xiao Song Cheng", "Lao Bian Jiao Zi"]
    },
    "kashi": {
        "signature_dishes": [
            {"name": "Pilaf (抓饭)", "description": "Uyghur rice dish with lamb and carrots"},
            {"name": "Lamb Kebabs (烤羊肉串)", "description": "Grilled lamb skewers with cumin"},
            {"name": "Naan Bread (馕)", "description": "Traditional Uyghur flatbread"},
            {"name": "Laghman Noodles (拉条子)", "description": "Hand-pulled noodles with lamb and vegetables"},
            {"name": "Hui BanMian (拌面)", "description": "Stir-fried noodles with meat and vegetables"}
        ],
        "street_food": ["Kebabs", "Naan", "Pilaf", "Yogurt", "Melons"],
        "famous_restaurants": ["Ou Yi Da", "Mi Ji Ti", "Ka Wa Pu"]
    },
    "linyi": {
        "signature_dishes": [
            {"name": "Linyi Fried Chicken (临沂炒鸡)", "description": "Spicy stir-fried chicken with potatoes"},
            {"name": "Pancake (沂蒙煎饼)", "description": "Crispy millet pancakes"},
            {"name": "Donkey Meat (驴肉)", "description": "Braised donkey meat, local specialty"},
            {"name": "Braised Fish (红烧鱼)", "description": "Yi River fish in soy sauce"},
            {"name": "Sweet Potato (烤地瓜)", "description": "Roasted sweet potatoes"}
        ],
        "street_food": ["Pancake", "Grilled Corn", "Sweet Potato", "Fried Dough"],
        "famous_restaurants": ["Wang Shi", "Lao Di Fang", "Yi Meng Shan"]
    },
    "taiyuan": {
        "signature_dishes": [
            {"name": "Taiyuan Noodles (太原头脑)", "description": "Traditional breakfast soup with mutton"},
            {"name": "Mature Vinegar (老陈醋)", "description": "Famous Shanxi aged vinegar"},
            {"name": "Sliced Noodles (刀削面)", "description": "Hand-sliced noodles with meat sauce"},
            {"name": "Youmian Kaolaoli (莜面栲栳栳)", "description": "Oat flour rolled noodles"},
            {"name": "Guoyou Rou (过油肉)", "description": "Deep-fried pork with vegetables"}
        ],
        "street_food": ["Sliced Noodles", "Vinegar Peanuts", "Fried Dough", "Tofu"],
        "famous_restaurants": ["Qing He Yuan", "Lao Xi Fan", "Hao Gang Gang"]
    },
    "urumqi": {
        "signature_dishes": [
            {"name": "Pilaf (抓饭)", "description": "Uyghur rice with lamb, carrots, and raisins"},
            {"name": "Lamb Kebabs (烤羊肉串)", "description": "Spicy grilled lamb skewers"},
            {"name": "Hui BanMian (新疆拌面)", "description": "Xinjiang-style hand-pulled noodles"},
            {"name": "Naan (馕)", "description": "Traditional Uyghur bread"},
            {"name": "Roasted Whole Lamb (烤全羊)", "description": "Whole lamb roasted over open fire"}
        ],
        "street_food": ["Kebabs", "Naan", "Yogurt", "Melons", "Pilaf"],
        "famous_restaurants": ["Hai Li", "Mi Ji Ti", "A Yi Lai"]
    },
    "wuxi": {
        "signature_dishes": [
            {"name": "Wuxi Spareribs (无锡排骨)", "description": "Sweet and savory braised pork ribs"},
            {"name": "Wuxi Xiaolongbao (无锡小笼包)", "description": "Sweet soup dumplings with pork"},
            {"name": "Lake Tai Whitebait (太湖银鱼)", "description": "Delicate whitefish from Lake Tai"},
            {"name": "Yangchun Noodles (阳春面)", "description": "Simple noodles in clear broth"},
            {"name": "Wuxi Fried Rice (无锡炒饭)", "description": "Fried rice with local ingredients"}
        ],
        "street_food": ["Spareribs", "Soup Dumplings", "Oil Gluten", "Rice Cakes"],
        "famous_restaurants": ["San Feng Qiao", "Wang Xing Ji", "De Tai Feng"]
    }
}

# Update each city JSON file
data_dir = '/root/.openclaw/workspace/travel-website/data'

cities = [
    'beijing', 'shanghai', 'guangzhou', 'shenzhen', 'chengdu', 'hangzhou', 'wuhan', 'xian',
    'nanjing', 'chongqing', 'tianjin', 'suzhou', 'qingdao', 'harbin', 'hongkong', 'kunming',
    'xiamen', 'dali', 'datong', 'guilin', 'guiyang', 'jinan', 'kaifeng', 'kashi', 'linyi',
    'taiyuan', 'urumqi', 'wuxi'
]

for city in cities:
    json_file = os.path.join(data_dir, f'{city}.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add cuisine data if available
        if city in cuisine_data:
            if 'cuisine' not in data:
                data['cuisine'] = {}
            
            # Add new fields
            data['cuisine']['signature_dishes'] = cuisine_data[city]['signature_dishes']
            data['cuisine']['street_food'] = cuisine_data[city]['street_food']
            data['cuisine']['famous_restaurants'] = cuisine_data[city]['famous_restaurants']
            
            # Write back
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Updated {city}.json")
        else:
            print(f"No cuisine data for {city}")
    else:
        print(f"File not found: {json_file}")

print("\nAll cities updated!")
