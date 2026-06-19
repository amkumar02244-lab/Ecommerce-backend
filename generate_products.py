import csv
import os
import uuid
from datetime import datetime

# Curated Women's Fashion Data Pool for Riya's Boutique
data_pools = {
    "Ethnic Wear": [
        {"name": "Varanasi Silk Saree", "brand": "Sabyasachi", "price": 45000.00, "description": "Exquisite handwoven Banarasi pure silk saree featuring heritage floral bootis in real gold zari work.", "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&auto=format&fit=crop&q=60"},
        {"name": "Floral Organza Saree", "brand": "Anita Dongre", "price": 24900.00, "description": "Delicate pastel organza saree featuring hand-painted botanical designs and fine gota patti borders.", "image": "https://images.unsplash.com/photo-1610030470298-db0952d7e008?w=500&auto=format&fit=crop&q=60"},
        {"name": "Royal Velvet Anarkali", "brand": "Riya's Couture", "price": 18500.00, "description": "Regal deep emerald velvet Anarkali suit set decorated with hand-embroidered tilla work on neck and sleeves.", "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&auto=format&fit=crop&q=60"},
        {"name": "Ivory Chikankari Kurta", "brand": "Fabindia", "price": 4999.00, "description": "Classic Lucknowi hand-embroidered georgette kurta set in a pristine ivory white tone with slip.", "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=500&auto=format&fit=crop&q=60"},
        {"name": "Crimson Silk Lehenga Set", "brand": "Sabyasachi", "price": 85000.00, "description": "Heirloom crimson red silk lehenga skirt featuring floral motifs, matching choli, and sheer organza dupatta.", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&auto=format&fit=crop&q=60"},
        {"name": "Peach Georgette Sharara Set", "brand": "Biba", "price": 6999.00, "description": "Flowy layered pastel peach sharara pants paired with a short sequined kurta and matching dupatta.", "image": "https://images.unsplash.com/photo-1608748010899-18f300247112?w=500&auto=format&fit=crop&q=60"},
        {"name": "Indigo Blockprint Kurti", "brand": "Fabindia", "price": 2499.00, "description": "Daily-wear A-line hand block printed cotton kurti dyed in organic indigo shades.", "image": "https://images.unsplash.com/photo-1605763240000-7e93b172d754?w=500&auto=format&fit=crop&q=60"},
        {"name": "Hand-embroidered Kaftan", "brand": "Anita Dongre", "price": 14999.00, "description": "Silk crepe luxury kaftan printed with traditional Rajasthani architecture motifs, hand-beaded neckline.", "image": "https://images.unsplash.com/photo-1596783074918-c84cb06531ca?w=500&auto=format&fit=crop&q=60"},
        {"name": "Banarasi Brocade Kurta", "brand": "Riya's Couture", "price": 8999.00, "description": "Rich magenta silk brocade straight kurta paired with gold woven tissue palazzo pants.", "image": "https://images.unsplash.com/photo-1583391265517-35bbdad01209?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pastel Mint Gharara", "brand": "Biba", "price": 7500.00, "description": "Elegant festive mint green gharara set printed with silver foil details and pink border accents.", "image": "https://images.unsplash.com/photo-1610030469668-93535c17b6b3?w=500&auto=format&fit=crop&q=60"}
    ],
    "Western Wear": [
        {"name": "Satin Slip Dress", "brand": "Zara", "price": 3990.00, "description": "Fluid cowl neck satin midi slip dress in luxury emerald green, featuring delicate spaghetti straps.", "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=500&auto=format&fit=crop&q=60"},
        {"name": "Linen Wrap Sun Dress", "brand": "H&M", "price": 2499.00, "description": "Breathable pure organic linen wrap dress featuring a tie belt waist and vintage flared skirt.", "image": "https://images.unsplash.com/photo-1544441893-675973e31985?w=500&auto=format&fit=crop&q=60"},
        {"name": "Tweed Double Blazer", "brand": "Zara", "price": 6990.00, "description": "Textured tweed blazer jacket with structured padded shoulders and polished gold-crest buttons.", "image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500&auto=format&fit=crop&q=60"},
        {"name": "Silk Georgette Blouse", "brand": "Mango", "price": 3590.00, "description": "Elegant semi-sheer high-neck silk blouse featuring ruffled neck detail and mother-of-pearl buttons.", "image": "https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pleated Satin Skirt", "brand": "H&M", "price": 2999.00, "description": "High-waist champagne gold accordion-pleated midi skirt with a comfortable elasticated waistband.", "image": "https://images.unsplash.com/photo-1582142306909-195724d33ab9?w=500&auto=format&fit=crop&q=60"},
        {"name": "Sateen Wide Leg Trousers", "brand": "Zara", "price": 3290.00, "description": "Sleek flowing sateen wide-leg trousers in classic cream white, with front pockets and zip fly.", "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&auto=format&fit=crop&q=60"},
        {"name": "Lace Trim Cami Top", "brand": "Mango", "price": 1990.00, "description": "Premium silk cami top detailed with delicate black eyelash lace trimming on the neckline.", "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&auto=format&fit=crop&q=60"},
        {"name": "Ribbed Knit Bodycon Dress", "brand": "Zara", "price": 4590.00, "description": "Sophisticated long sleeve ribbed knit midi dress contouring the body, styled with a high collar.", "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500&auto=format&fit=crop&q=60"},
        {"name": "Floral Chiffon Wrap Dress", "brand": "H&M", "price": 3499.00, "description": "Flowing floral printed chiffon midi wrap dress styled with sheer balloon sleeves and ruffle hem.", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&auto=format&fit=crop&q=60"},
        {"name": "Classic Trench Coat", "brand": "Mango", "price": 8990.00, "description": "Double-breasted water-resistant beige trench coat with storm flaps and a detachable waist belt.", "image": "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=500&auto=format&fit=crop&q=60"}
    ],
    "Handbags": [
        {"name": "Leather Satchel Bag", "brand": "Riya's Signature", "price": 12500.00, "description": "Structured top-handle genuine leather satchel bag with luxury polished gold-tone locking hardware.", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&auto=format&fit=crop&q=60"},
        {"name": "Suede Crossbody Bag", "brand": "Fossil", "price": 8999.00, "description": "Minimalist premium soft suede sling crossbody bag detailed with an adjustable leather shoulder strap.", "image": "https://images.unsplash.com/photo-1566150905458-1bf1fc15aae9?w=500&auto=format&fit=crop&q=60"},
        {"name": "Silk Brocade Box Clutch", "brand": "Anita Dongre", "price": 6500.00, "description": "Elegant traditional box clutch wrapped in heritage Banarasi silk brocade, finished with a metallic clasp.", "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&auto=format&fit=crop&q=60"},
        {"name": "Quilted Chain Tote Bag", "brand": "Zara", "price": 4990.00, "description": "Quilted luxury faux leather shoulder bag styled with interlocked gold chain-link straps and double pocket.", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&auto=format&fit=crop&q=60"},
        {"name": "Canvas Utility Tote", "brand": "Mango", "price": 3290.00, "description": "Spacious woven structured canvas tote bag with contrast leather handles and magnetic button closure.", "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&auto=format&fit=crop&q=60"},
        {"name": "Luxury Envelope Clutch", "brand": "Riya's Signature", "price": 7900.00, "description": "Sleek envelope foldover clutch in pebble-grained calfskin leather, features card slots and chain strap.", "image": "https://images.unsplash.com/photo-1598532187856-3c09e3905cfc?w=500&auto=format&fit=crop&q=60"},
        {"name": "Saddle Crossbody Bag", "brand": "Fossil", "price": 10500.00, "description": "Heritage saddle bag in rich cognac leather, featuring brass buckles and front slip pockets.", "image": "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=500&auto=format&fit=crop&q=60"},
        {"name": "Woven Straw Beach Bag", "brand": "H&M", "price": 1999.00, "description": "Bohemian summer straw shoulder bag woven with geometric panels, perfect for summer outings.", "image": "https://images.unsplash.com/photo-1576053139778-7e32f2ae3cf4?w=500&auto=format&fit=crop&q=60"},
        {"name": "Designer Bucket Bag", "brand": "Zara", "price": 3990.00, "description": "Mini drawstring leather bucket bag with top carry handle and gold hardware eyelets.", "image": "https://images.unsplash.com/photo-1611085583191-a3b1a8a89b70?w=500&auto=format&fit=crop&q=60"},
        {"name": "Metallic Evening Pouch", "brand": "Mango", "price": 2990.00, "description": "Glittering rose gold metallic woven mesh pouch with drawcord lock, perfect for weddings.", "image": "https://images.unsplash.com/photo-1566150905458-1bf1fc15aae9?w=500&auto=format&fit=crop&q=60"}
    ],
    "Footwear": [
        {"name": "Zardozi Leather Juttis", "brand": "Fizzy Goblet", "price": 3200.00, "description": "Handcrafted leather juttis detailed with traditional gold zardozi leaf embroidery and pearls.", "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&auto=format&fit=crop&q=60"},
        {"name": "Ankle Strap Leather Heels", "brand": "Steve Madden", "price": 8999.00, "description": "Classic pointed toe high-heeled pumps detailed with adjustable cross-ankle straps in nude patent leather.", "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&auto=format&fit=crop&q=60"},
        {"name": "Satin Mule Flats", "brand": "Charles & Keith", "price": 4590.00, "description": "Sophisticated pointed-toe flat slide mules featuring a crystal-embellished decorative front buckle.", "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500&auto=format&fit=crop&q=60"},
        {"name": "Strappy Suede Sandals", "brand": "Steve Madden", "price": 6999.00, "description": "Lace-up block-heeled sandals crafted in soft black suede leather with tassels.", "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&auto=format&fit=crop&q=60"},
        {"name": "Embellished Wedding Heels", "brand": "Riya's Signature", "price": 11500.00, "description": "Elegant bridal kitten heels wrapped in champagne satin and hand-beaded with premium glass beads.", "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=60"},
        {"name": "Braided Leather Slides", "brand": "Charles & Keith", "price": 3290.00, "description": "Comfortable chic slides with a padded footbed and woven strap detail in tan leather.", "image": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=500&auto=format&fit=crop&q=60"},
        {"name": "Gilded Kohlapuri Wedges", "brand": "Fizzy Goblet", "price": 3800.00, "description": "Traditional Kohlapuri sandal styled with a modern comfortable cork wedge heel and gold straps.", "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&auto=format&fit=crop&q=60"},
        {"name": "Velvet Embroidered Loafers", "brand": "Charles & Keith", "price": 5490.00, "description": "Chic smoking slippers in black velvet, embroidered with customized gold monogram details.", "image": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500&auto=format&fit=crop&q=60"},
        {"name": "Metallic Strappy Flats", "brand": "H&M", "price": 1499.00, "description": "Minimalist slip-on flat sandals featuring slim intersecting gold straps and square toe.", "image": "https://images.unsplash.com/photo-1562273138-f46be4ebdf33?w=500&auto=format&fit=crop&q=60"},
        {"name": "Leather Chelsea Boots", "brand": "Zara", "price": 7990.00, "description": "Classic black leather Chelsea boots featuring elasticated panels and low block heel.", "image": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=500&auto=format&fit=crop&q=60"}
    ],
    "Jewelry & Accessories": [
        {"name": "Polki Kundan Necklace Set", "brand": "Riya's Fine Jewelry", "price": 35000.00, "description": "Stunning heritage Choker necklace set in gold-plating, inlaid with uncut glass Polki and hanging green emerald beads.", "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pave Crystal Hoop Earrings", "brand": "Swarovski", "price": 6990.00, "description": "Sparkling pave-set crystal hoop earrings cast in a modern high-polish rose gold plating.", "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&auto=format&fit=crop&q=60"},
        {"name": "Oversized Acetate Sunglasses", "brand": "Prada", "price": 18500.00, "description": "Statement designer square-frame black sunglasses with premium scratch-resistant UV400 lenses.", "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&auto=format&fit=crop&q=60"},
        {"name": "Pearl Drop Earrings", "brand": "Riya's Fine Jewelry", "price": 4500.00, "description": "Classic freshwater baroque pearl drops suspended from elegant sterling silver gold-plated studs.", "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&auto=format&fit=crop&q=60"},
        {"name": "Silk Hair Scarf Set", "brand": "Mango", "price": 1590.00, "description": "Three pack of organic mulberry silk square neck scarves printed in vintage chic patterns.", "image": "https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?w=500&auto=format&fit=crop&q=60"},
        {"name": "Filigree Cuff Bangle", "brand": "Anita Dongre", "price": 8900.00, "description": "Handcrafted adjustable brass cuff bangle detailed with traditional Indian filigree design.", "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=500&auto=format&fit=crop&q=60"},
        {"name": "Classic Rose Gold Watch", "brand": "Fossil", "price": 12499.00, "description": "Chic women's timepiece featuring a minimal rose gold dial case and premium mesh strap.", "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&auto=format&fit=crop&q=60"},
        {"name": "Emerald Ring 18k Gold", "brand": "Riya's Fine Jewelry", "price": 28900.00, "description": "Dainty 18k solid yellow gold ring set with a faceted natural oval-cut green emerald gemstone.", "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=500&auto=format&fit=crop&q=60"},
        {"name": "Wool Felt Fedora Hat", "brand": "Zara", "price": 2990.00, "description": "Classic autumn fedora hat styled with a structured wide brim and contrast grosgrain band.", "image": "https://images.unsplash.com/photo-1533827432537-70133748f5c8?w=500&auto=format&fit=crop&q=60"},
        {"name": "Delicate Coin Anklet", "brand": "Swarovski", "price": 3990.00, "description": "Minimalist rose gold double chain anklet detailed with tiny polished geometric metal coin drops.", "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&auto=format&fit=crop&q=60"}
    ]
}

def generate_100_products():
    csv_rows = []
    
    # We want exactly 100 items. We have 5 categories, each has 10 base products.
    # We will expand the pool by dynamically creating variations (e.g. colors, capacities, bundles, editions)
    # until we hit exactly 100 unique commercial products.
    
    variations = [
        {"suffix": "", "price_mult": 1.0, "stock_mult": 1.0, "desc_addon": "", "sku_addon": ""},
        {"suffix": " (Rose Gold Edition)", "price_mult": 1.05, "stock_mult": 0.8, "desc_addon": " Finished in our signature luxury rose-gold details.", "sku_addon": "-RG"},
        {"suffix": " (Midnight Velvet)", "price_mult": 1.0, "stock_mult": 0.7, "desc_addon": " Available in elegant Midnight Black colorway.", "sku_addon": "-MV"},
        {"suffix": " Festive Gift Set", "price_mult": 1.25, "stock_mult": 0.5, "desc_addon": " Wrapped in a luxury gold-embossed keepsake storage box.", "sku_addon": "-GIFTSET"},
        {"suffix": " (Pastel Pearl Edition)", "price_mult": 1.10, "stock_mult": 0.6, "desc_addon": " Embellished with hand-selected pastel freshwater pearls.", "sku_addon": "-PEARL"},
    ]

    target_count = 100
    current_count = 0
    
    categories_list = list(data_pools.keys())
    
    # Track which variation index to apply to each product in each category
    var_indexes = {cat: [0] * len(data_pools[cat]) for cat in categories_list}
    
    while current_count < target_count:
        for cat in categories_list:
            if current_count >= target_count:
                break
                
            base_products = data_pools[cat]
            for idx, base in enumerate(base_products):
                if current_count >= target_count:
                    break
                    
                var_idx = var_indexes[cat][idx]
                if var_idx >= len(variations):
                    continue # exhausted variations for this product
                    
                var = variations[var_idx]
                var_indexes[cat][idx] += 1
                
                # Build variation product
                name = f"{base['name']}{var['suffix']}"
                # Convert price to integer INR values
                price = int(round(base['price'] * var['price_mult']))
                stock = int(max(5, 50 * var['stock_mult'] * (1.1 - 0.1 * var_idx)))
                sku_clean = base['name'].replace(" ", "").replace("'", "").replace("&", "").upper()[:10]
                sku = f"{cat[:2].upper()}-{sku_clean}{var['sku_addon']}"
                description = f"{base['description']}{var['desc_addon']}"
                
                product_id = str(uuid.uuid4())
                created_at = datetime.utcnow().isoformat()
                
                row = {
                    "id": product_id,
                    "name": name,
                    "description": description,
                    "price": str(price),
                    "stock": str(stock),
                    "category": cat,
                    "is_active": "True",
                    "image_url": base["image"],
                    "brand": base["brand"],
                    "sku": sku,
                    "created_at": created_at,
                    "updated_at": ""
                }
                csv_rows.append(row)
                current_count += 1
                
    # Save to products.csv
    csv_file_path = os.path.join("data", "products.csv")
    os.makedirs("data", exist_ok=True)
    
    fieldnames = [
        "id", "name", "description", "price", "stock", "category", 
        "is_active", "image_url", "brand", "sku", "created_at", "updated_at"
    ]
    
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
        
    print(f"Successfully populated {len(csv_rows)} products into {csv_file_path}")

if __name__ == "__main__":
    generate_100_products()
