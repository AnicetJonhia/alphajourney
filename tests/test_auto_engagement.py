import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import asyncio
from app.services.facebook_service import get_facebook_service
from app.data.comments import get_first_comment

async def test_engagement():
    """Test du like et commentaire automatiques."""
    
    fb_service = get_facebook_service()
    
    # Remplace par un vrai post_id de test
    test_post_id = "929184316952659_122100446307260840"
    
    print("🧪 Test auto-engagement\n")
    
    # Test 1 : Like
    print("1️⃣ Test like...")
    like_ok = await fb_service.like_post(test_post_id)
    print(f"   {'✅' if like_ok else '❌'} Like\n")
    
    # Test 2 : Commentaire
    print("2️⃣ Test commentaire...")
    comment = get_first_comment("finance")
    print(f"   Commentaire : {comment[:50]}...\n")
    
    comment_id = await fb_service.comment_post(test_post_id, comment)
    print(f"   {'✅' if comment_id else '❌'} Commentaire\n")
    
    if comment_id:
        print(f"🎉 Auto-engagement fonctionnel !")
        print(f"   Comment ID : {comment_id}")
    else:
        print("⚠️ Vérifier les permissions Facebook")

if __name__ == "__main__":
    asyncio.run(test_engagement())