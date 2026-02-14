import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from app.database import SessionLocal
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service

async def test_full_post():
    """Test complet : contenu + hashtags + image."""
    
    db = SessionLocal()
    
    try:
        content_service = ContentService(db)
        fb_service = get_facebook_service()
        
        category = "threads"
        topic = "Tiktok vs Threads : qui gagne ?"
        
        print(f"📝 Génération post : {topic}\n")
        
        # 1. Contenu + hashtags
        content, llm = await content_service.generate_post_content(
            category, topic
        )
        
        print("=" * 60)
        print(content)
        print("=" * 60)
        print(f"\n✅ Généré avec : {llm}\n")
        
        # 2. Image
        image_url = await content_service.get_post_image(category)
        
        if image_url:
            print(f"📸 Image : {image_url}\n")
        else:
            print("⚠️ Pas d'image disponible\n")
        
        # 3. Publier (optionnel)
        choice = input("Publier sur Facebook ? (o/n) : ")
        
        if choice.lower() == 'o':
            post_id = await fb_service.publish(content, image_url)
            print(f"\n✅ Publié ! ID : {post_id}")
            print("🔗 Va voir sur ta page Facebook !")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_full_post())