"""
Database Seed Script for Hero Templates
This script populates the hero_templates table with all 200 Three Kingdoms heroes.
"""
from typing import List, Dict, Any
from decimal import Decimal

from app.data.hero_data import get_all_heroes, get_hero_count


def get_hero_templates_seed_data() -> List[Dict[str, Any]]:
    """
    Get hero template data ready for database insertion.
    
    Returns:
        List of dictionaries with hero template data matching the HeroTemplate model.
    """
    heroes = get_all_heroes()
    seed_data = []
    
    for hero in heroes:
        template = {
            "id": hero["id"],
            "name": hero["name"],
            "title": hero.get("title", ""),
            "element": hero["element"],
            "base_rarity": hero["base_rarity"],
            "hero_class": hero["hero_class"],
            "base_hp": hero["base_hp"],
            "base_atk": hero["base_atk"],
            "base_def": hero["base_def"],
            "base_spd": hero["base_spd"],
            "base_crit": hero["base_crit"],
            "base_dex": hero["base_dex"],
            "growth_hp": Decimal(str(hero["growth_hp"])),
            "growth_atk": Decimal(str(hero["growth_atk"])),
            "growth_def": Decimal(str(hero["growth_def"])),
            "growth_spd": Decimal(str(hero["growth_spd"])),
            "growth_crit": Decimal(str(hero["growth_crit"])),
            "growth_dex": Decimal(str(hero["growth_dex"])),
            "description": hero.get("description", ""),
            "lore": hero.get("lore", ""),
            "icon_url": hero.get("icon_url", ""),
            "model_url": hero.get("model_url", ""),
        }
        seed_data.append(template)
    
    return seed_data


def print_seed_summary() -> None:
    """Print a summary of seed data"""
    counts = get_hero_count()
    print("=" * 50)
    print("Hero Templates Seed Data Summary")
    print("=" * 50)
    print(f"Kim (Metal) heroes:  {counts['KIM']}")
    print(f"Mộc (Wood) heroes:   {counts['MOC']}")
    print(f"Thủy (Water) heroes: {counts['THUY']}")
    print(f"Hỏa (Fire) heroes:   {counts['HOA']}")
    print(f"Thổ (Earth) heroes:  {counts['THO']}")
    print("-" * 50)
    print(f"Total heroes:        {counts['TOTAL']}")
    print("=" * 50)


async def seed_hero_templates(db_session) -> int:
    """
    Seed hero templates into the database.
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        Number of heroes seeded
    """
    from app.models.hero import HeroTemplate
    from sqlalchemy import select
    
    seed_data = get_hero_templates_seed_data()
    seeded_count = 0
    
    for template_data in seed_data:
        # Check if template already exists
        stmt = select(HeroTemplate).where(HeroTemplate.id == template_data["id"])
        result = await db_session.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing is None:
            # Create new template
            template = HeroTemplate(**template_data)
            db_session.add(template)
            seeded_count += 1
    
    await db_session.commit()
    return seeded_count


if __name__ == "__main__":
    print_seed_summary()
    
    # Print sample data
    seed_data = get_hero_templates_seed_data()
    print("\nSample hero data (first 3):")
    for hero in seed_data[:3]:
        print(f"\n{hero['name']} ({hero['element']}):")
        print(f"  Class: {hero['hero_class']}, Rarity: {hero['base_rarity']}⭐")
        print(f"  HP: {hero['base_hp']}, ATK: {hero['base_atk']}, DEF: {hero['base_def']}")
        print(f"  Icon: {hero['icon_url']}")
