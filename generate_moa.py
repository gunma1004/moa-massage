import os
import urllib.parse
import itertools  # 템플릿 로테이션을 위해 추가

BASE_URL = "https://moa-massage.netlify.app"
BRAND_NAME = "모아"

MAIN_TITLE = "모아 — 모든 마사지를 모았다 | 모마"
MAIN_DESC = "모아 — 모든 마사지를 모아서. 전국 마사지·홈케어를 지역별로 검색하고 바로 예약하세요."

# --- SEO 템플릿 로테이션 설정 (다양성 확보) ---
TITLE_TEMPLATES = itertools.cycle([
    "{full_dong} 홈케어 마사지·출장 — {short_dong} 마사지 | {brand}",
    "{short_dong} 출장 24시간 마사지 | {full_dong} 프리미엄 홈케어 — {brand}",
    "{full_dong} 내주변 마사지 추천 | {short_dong} 스웨디시·타이 출장 — {brand}",
    "{brand} | {full_dong} 마사지·출장 — {short_dong} 100% 안심 후불제"
])

DESC_TEMPLATES = itertools.cycle([
    "퇴근길 복잡한 {dist} 일대가 막히는 저녁에도 {full_dong} 오피스텔로 오는 24시간 출장 마사지를 찾으시나요?",
    "{full_dong} 지역 내 자택, 레지던스 어디든 신속 방문! 선입금 없는 {short_dong} 안심 출장 마사지를 예약하세요.",
    "{short_dong} 주변에서 피로를 풀고 싶다면? {full_dong} 전문 테라피스트가 직접 방문하는 출장마사지를 경험해보세요.",
    "비 오고 나가기 귀찮을 때 {dist} {short_dong} 어디든 찾아가는 마사지. {full_dong} 내주변 24시간 후불제 출장 마사지 추천."
])

# 6개 업체 풀 (텍스트용 연락처)
SHOPS_DATA = [
    {"name": "퀸즈홈테라피", "phone": "0507-1280-3296", "desc": "전문 힐러진의 체형 맞춤 피로회복 특화 프로그램 및 천연 에센셜 오일 관리", "price": "80,000원부터~", "score": "4.9", "img": "/images/shop1.jpg"},
    {"name": "한국미인테라피", "phone": "0507-1280-3140", "desc": "지친 일상에 맞춤형 피로회복 케어! 베테랑 한국인 테라피스트의 프라이빗 릴렉싱", "price": "70,000원부터~", "score": "4.9", "img": "/images/shop2.jpg"},
    {"name": "오늘밤테라피", "phone": "0507-1280-3199", "desc": "선입금 없는 100% 안심 후불제! 타이, 전신아로마 및 VIP 감성힐링 전문", "price": "60,000원부터~", "score": "4.9", "img": "/images/shop3.jpg"},
    {"name": "주주테라피", "phone": "0507-1280-3197", "desc": "재방문율 높은 안심 케어! 철저한 위생 관리와 최고급 럭셔리 스웨디시 프로그램", "price": "60,000원부터~", "score": "4.8", "img": "/images/shop4.jpg"},
    {"name": "기쁨테라피", "phone": "0507-1280-3183", "desc": "몸과 마음에 활력을 채워주는 세심하고 품격 있는 전신 힐링 테라피", "price": "60,000원부터~", "score": "4.9", "img": "/images/shop5.jpg"},
    {"name": "미인클럽테라피", "phone": "0507-1280-3180", "desc": "젊고 세련된 감각의 테라피스트들이 제공하는 스페셜 감성 아로마 테라피", "price": "70,000원부터~", "score": "4.9", "img": "/images/shop6.jpg"}
]

# (주의: 너무 길어 지면상 서울/경기 일부만 예시로 남깁니다. 실제 사용 시 기존의 전체 REGION_DATA를 그대로 붙여넣으세요)
REGION_DATA = {
    'seoul': {
        'name': '서울특별시',
        'districts': {
            'gangnam': {'name': '강남구', 'dongs': ['역삼1동', '논현1동', '청담동']}
        }
    }
}

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="Yeti" content="index,follow,max-image-preview:large">
  <title>{page_title}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{canonical_url}">
  
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{brand}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="/images/gallery1.jpg">

  <script type="application/ld+json">
  {json_ld}
  </script>

  <style>
    :root {{
      --bg-dark: #121013;
      --card-bg: #1c181d;
      --card-inner: #151218;
      --card-border: #2c252f;
      --text-main: #f3eff5;
      --text-muted: #9e93a2;
      --accent-brand: #7952b3;
      --star-color: #f59e0b;
      --font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: var(--font-family); line-height: 1.6; }}
    a {{ color: inherit; text-decoration: none; }}
    .wrap {{ max-width: 1040px; margin: 0 auto; padding: 0 16px; }}
    
    header.top {{ border-bottom: 1px solid var(--card-border); background: rgba(18, 16, 19, 0.96); position: sticky; top: 0; z-index: 100; backdrop-filter: blur(8px); }}
    .header-row {{ display: flex; align-items: center; justify-content: space-between; height: 64px; }}
    .brand {{ font-size: 1.35rem; font-weight: 800; color: #fff; }}
    .brand span {{ color: var(--accent-brand); }}
    
    .page-head {{ padding: 24px 0 16px; }}
    .breadcrumbs {{ font-size: 0.82rem; color: var(--text-muted); margin-bottom: 8px; }}
    .title-line h1 {{ font-size: 1.75rem; font-weight: 800; margin-bottom: 4px; }}
    .page-description {{ font-size: 0.95rem; color: var(--text-muted); margin-top: 8px; line-height: 1.5; }}
    
    .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
    .tag {{ background: var(--card-inner); border: 1px solid var(--card-border); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; transition: 0.2s; }}
    
    .panel {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 24px; margin-bottom: 20px; }}
    .panel h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 16px; color: #fff; }}
    
    .shop-list {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 10px; }}
    .shop-card-item {{ background: var(--card-inner); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; display: flex; gap: 16px; align-items: center; }}
    .shop-card-item img {{ width: 120px; height: 120px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
    .shop-card-info {{ flex: 1; min-width: 0; }}
    .shop-card-info h3 {{ font-size: 1.1rem; font-weight: 800; color: #fff; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .shop-card-info p {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px; line-height: 1.4; }}
    
    .shop-card-bottom {{ display: flex; justify-content: space-between; align-items: center; background: #1a171d; padding: 8px 12px; border-radius: 6px; border: 1px solid #2d2631; }}
    .shop-card-bottom .price {{ color: var(--star-color); font-weight: 800; font-size: 1rem; }}
    .shop-card-bottom .phone-text {{ font-size: 0.95rem; font-weight: bold; color: #fff; letter-spacing: 0.5px; }}

    .type-box {{ background: var(--card-inner); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px; margin-bottom: 12px; }}
    .type-box h3 {{ color: var(--accent-brand); font-size: 1rem; margin-bottom: 6px; }}
    
    .review-item {{ background: var(--card-inner); border: 1px solid var(--card-border); border-radius: 8px; padding: 14px; margin-bottom: 10px; }}
    .review-top {{ display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px; }}
    .review-top strong {{ color: #fff; }}
    
    .map-frame {{ width: 100%; height: 320px; border: 0; border-radius: 8px; margin-top: 12px; }}
    footer {{ border-top: 1px solid var(--card-border); padding: 30px 0; text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 40px; }}
    
    @media (max-width: 768px) {{
      .shop-card-item {{ flex-direction: column; align-items: flex-start; }}
      .shop-card-item img {{ width: 100%; height: 160px; }}
      .shop-card-bottom {{ flex-direction: column; align-items: flex-start; gap: 6px; width: 100%; }}
    }}
  </style>
</head>
<body>
  <header class="top">
    <div class="wrap header-row">
      <a class="brand" href="/">모아<span>.</span></a>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
      <div class="page-head">
        <div class="breadcrumbs">{breadcrumbs}</div>
        <div class="title-line">
          <h1>{page_title_h1}</h1>
          <p class="page-description">{meta_description}</p>
        </div>
      </div>

      {tag_section}

      <div class="content-area">
        <section class="panel">
          <h2>{location_title} 추천 마사지·홈케어 (6곳)</h2>
          <div class="shop-list">
            {shop_cards_html}
          </div>
        </section>

        <section class="panel">
          <h2>{location_title} 홈케어·출장 마사지 특징</h2>
          <div class="type-box">
            <h3>📍 어디서나 편리한 프라이빗 홈케어</h3>
            <p>{location_title} 지역 내 오피스텔, 자택, 레지던스 어디든 늦은 저녁이나 새벽 시간에도 교통 체증 걱정 없이 편안하게 이용할 수 있습니다.</p>
          </div>
          <div class="type-box">
            <h3>📍 빠르고 안전한 지역맞춤 서비스</h3>
            <p>퇴근길 복잡한 {location_title} 인근에서도 신속하게 방문하는 전문 테라피스트 진을 통해 하루의 피로를 즉각적으로 풀어보세요.</p>
          </div>
        </section>

        <section class="panel">
          <h2>{location_title} 이용 고객 생생 후기</h2>
          <div class="review-item">
            <div class="review-top">
              <strong>김*우 고객님</strong>
              <span style="color:var(--star-color); font-weight:bold;">★★★★★ 5.0</span>
            </div>
            <p style="font-size:0.85rem; color:#d1c9d4;">{location_title} 주변에서 바로 예약할 수 있어서 편리했습니다. 피곤한 날 밖에 나가지 않고 홈케어로 받으니 최고네요.</p>
          </div>
          <div class="review-item">
            <div class="review-top">
              <strong>이*진 고객님</strong>
              <span style="color:var(--star-color); font-weight:bold;">★★★★★ 5.0</span>
            </div>
            <p style="font-size:0.85rem; color:#d1c9d4;">퇴근하고 너무 늦은 시간이라 샵 가기 애매했는데, 24시간 출장으로 {location_title} 집까지 찾아와주셔서 정말 잘 쉬었습니다.</p>
          </div>
        </section>

        <section class="panel">
          <h2>{location_title} 지역 지도 안내</h2>
          <iframe class="map-frame" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_query}&output=embed" title="{location_title} 지도"></iframe>
        </section>
      </div>
    </div>
  </main>

  <footer>
    <div class="wrap">
      <p>© 2026 {brand} — 모든 마사지를 모았다. All Rights Reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

def generate_shop_cards(location_name):
    cards = []
    for shop in SHOPS_DATA:
        card = f"""
        <div class="shop-card-item">
          <img src="{shop['img']}" alt="{location_name} {shop['name']}">
          <div class="shop-card-info">
            <h3>{shop['name']} <span style="font-size:0.75rem; color:#f59e0b;">★ {shop['score']}</span></h3>
            <p>{shop['desc']}</p>
            <div class="shop-card-bottom">
              <span class="price">{shop['price']}</span>
              <span class="phone-text">문의: {shop['phone']}</span>
            </div>
          </div>
        </div>
        """
        cards.append(card)
    return "".join(cards)

def build_json_ld(brand, page_title_h1, meta_description, canonical_url):
    return f"""{{
      "@context": "https://schema.org",
      "@type": "HealthAndBeautyBusiness",
      "name": "{page_title_h1} - {brand}",
      "description": "{meta_description}",
      "url": "{canonical_url}",
      "priceRange": "60,000원 ~ 180,000원",
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "320",
        "bestRating": "5",
        "worstRating": "1"
      }}
    }}"""

def make_page(path, html_content):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

urls = [f"{BASE_URL}/"]
print(f"{BRAND_NAME} SEO 최적화 페이지 생성을 시작합니다...")

# 메인 페이지 생성
make_page(".", HTML_TEMPLATE.format(
    brand=BRAND_NAME,
    map_query=urllib.parse.quote("대한민국"),
    page_title=MAIN_TITLE,
    page_title_h1="모아 — 모든 마사지를 모았다",
    meta_description=MAIN_DESC,
    canonical_url=f"{BASE_URL}/",
    json_ld=build_json_ld(BRAND_NAME, "모아 — 모든 마사지를 모았다", MAIN_DESC, f"{BASE_URL}/"),
    location_title="전국",
    breadcrumbs='홈',
    tag_section="",
    shop_cards_html=generate_shop_cards("전국")
))

# 지역별 동적 생성 루프
for reg_key, reg_val in REGION_DATA.items():
    reg_name = reg_val['name']
    
    for dist_key, dist_val in reg_val['districts'].items():
        dist_name = dist_val['name']
        
        for dong in dist_val['dongs']:
            dong_dir = os.path.join("region", reg_key, dist_key, dong)
            encoded_dong = urllib.parse.quote(dong)
            dong_url = f"{BASE_URL}/region/{reg_key}/{dist_key}/{encoded_dong}/"
            urls.append(dong_url)
            
            full_dong_title = f"{dist_name} {dong}" 
            short_dong = dong 
            
            # --- 템플릿 로테이션 적용 ---
            t_template = next(TITLE_TEMPLATES)
            d_template = next(DESC_TEMPLATES)
            
            p_title = t_template.format(full_dong=full_dong_title, short_dong=short_dong, brand=BRAND_NAME)
            m_desc = d_template.format(full_dong=full_dong_title, short_dong=short_dong, dist=dist_name, brand=BRAND_NAME)
            p_h1 = f"{full_dong_title} 홈케어 마사지·출장"
            
            make_page(dong_dir, HTML_TEMPLATE.format(
                brand=BRAND_NAME,
                map_query=urllib.parse.quote(full_dong_title),
                page_title=p_title,
                page_title_h1=p_h1,
                meta_description=m_desc,
                canonical_url=dong_url,
                json_ld=build_json_ld(BRAND_NAME, p_h1, m_desc, dong_url),
                location_title=full_dong_title,
                breadcrumbs=f'홈 › {reg_name} › {dist_name} › {dong}',
                tag_section="",
                shop_cards_html=generate_shop_cards(full_dong_title)
            ))

# sitemap.xml 생성
sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap_xml.append(f"  <url><loc>{u}</loc><priority>0.8</priority></url>")
sitemap_xml.append('</urlset>')

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_xml))

# robots.txt 생성
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

print(f"작업 완료! 4종의 SEO 템플릿이 순환 적용된 {len(urls)}개의 URL에 대한 정적 HTML 생성이 완료되었습니다.")