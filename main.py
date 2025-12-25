import os, json
from modules.product_scraper import fetch_trending_products
from modules.keyword_research import generate_seo_keywords
from modules.publisher_wp import publish_to_wordpress
from modules.blog_generator import generate_blog_post

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    print("📌 Step 1: Fetching trending products from FakeStore API...")
    products = fetch_trending_products(limit=10)

    with open("output/products.json", "w") as f:
        json.dump(products, f, indent=2)

    print("✅ Saved: output/products.json")
    print("\n✅ Sample Product:\n", json.dumps(products[0], indent=2))



    

print("\n📌 Step 2: Generating SEO keywords (3–4 per product)...")

# Load products
with open("output/products.json", "r") as f:
    products = json.load(f)

seo_data = []

for i, product in enumerate(products):
    title = product["title"]
    category = product.get("category")

    print(f"🔍 Keywords for ({i+1}/{len(products)}): {title[:50]}...")

    keywords = generate_seo_keywords(title, category)

    seo_data.append({
        "title": title,
        "category": category,
        "keywords": keywords
    })

# Save output
with open("output/seo_keywords.json", "w") as f:
    json.dump(seo_data, f, indent=2)

print("✅ Saved: output/seo_keywords.json")



print("\n📌 Step 3: Generating SEO blog posts (150–200 words)...")

# Load products
with open("output/products.json", "r") as f:
    products = json.load(f)

# Load keywords
with open("output/seo_keywords.json", "r") as f:
    seo_data = json.load(f)

blog_posts = []

for i, product in enumerate(products):
    keywords = seo_data[i]["keywords"]

    print(f"✍️ Blog ({i+1}/{len(products)}): {product['title'][:50]}...")

    content = generate_blog_post(product, keywords)

    blog_posts.append({
        "blog_title": f"Why {product['title'][:60]} is Worth Buying in 2025",
        "product_title": product["title"],
        "keywords": keywords,
        "content": content,
        "product_url": product.get("product_url"),
        "image_url": product.get("image_url"),
        "price": product.get("price"),
        "category": product.get("category")
    })

# Save output
with open("output/blog_posts.json", "w") as f:
    json.dump(blog_posts, f, indent=2)

print("✅ Saved: output/blog_posts.json")





from modules.html_exporter import export_blog_as_html

print("\n📌 Step 4: Exporting blog posts as HTML for WordPress manual publishing...")

with open("output/blog_posts.json", "r") as f:
    blog_posts = json.load(f)

html_posts = []
os.makedirs("output/html_posts", exist_ok=True)

for i, post in enumerate(blog_posts):
    html_path = f"output/html_posts/post_{i}.html"
    export_blog_as_html(post, html_path)

    html_posts.append({
        "title": post["blog_title"],
        "html_file": html_path
    })

with open("output/published_links.json", "w") as f:
    json.dump(html_posts, f, indent=2)

print("✅ HTML posts saved to output/html_posts/")
print("✅ Saved: output/published_links.json")
