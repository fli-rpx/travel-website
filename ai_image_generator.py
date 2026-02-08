#!/usr/bin/env python3
"""
AI Image Generator for Travel Website
Generates or finds appropriate images for each Chinese city.
"""

import os
import json
import requests
import base64
from datetime import datetime

class AIImageGenerator:
    def __init__(self):
        self.website_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.website_dir, "ai_image_config.json")
        self.output_dir = os.path.join(self.website_dir, "ai_generated_images")
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Load or create config
        self.config = self.load_config()
    
    def load_config(self):
        """Load or create AI image configuration."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default configuration
        config = {
            "ai_services": {
                "openai_dalle": {
                    "enabled": False,
                    "api_key": "",
                    "model": "dall-e-3",
                    "style": "vivid",
                    "quality": "standard"
                },
                "stability_ai": {
                    "enabled": False,
                    "api_key": "",
                    "model": "stable-diffusion-xl-1024-v1-0"
                },
                "local_sd": {
                    "enabled": False,
                    "url": "http://localhost:7860"
                }
            },
            "image_requirements": {
                "resolution": "1792x1024",
                "aspect_ratio": "16:9",
                "style": "photorealistic",
                "color_palette": ["#2563eb", "#1e40af", "#f59e0b"],
                "mood": "professional travel photography"
            },
            "city_prompts": self.get_city_prompts(),
            "generation_status": {}
        }
        
        return config
    
    def get_city_prompts(self):
        """Get AI prompts for each city."""
        return {
            "Beijing": {
                "prompts": [
                    "Professional travel photography of the Great Wall of China at golden hour, majestic view, ancient architecture, blue sky with clouds, photorealistic, 16:9 aspect ratio",
                    "Forbidden City in Beijing, aerial view, traditional Chinese architecture, red walls and yellow tiles, tourists walking, sunny day, professional photography",
                    "Modern Beijing skyline with traditional elements, blend of old and new, professional architectural photography, blue hour lighting"
                ],
                "priority": 1,
                "needs_ai": True
            },
            "Shanghai": {
                "prompts": [
                    "Shanghai Bund skyline at night, modern skyscrapers, Huangpu River reflections, neon lights, professional cityscape photography, 16:9 aspect ratio",
                    "Oriental Pearl Tower in Shanghai, daytime, blue sky, modern architecture, professional travel photography",
                    "Lujiazui financial district aerial view, ultra-modern skyscrapers, professional architectural photography"
                ],
                "priority": 1,
                "needs_ai": True
            },
            "Chengdu": {
                "prompts": [
                    "Giant panda in Chengdu Panda Base, close-up portrait, eating bamboo, natural habitat, professional wildlife photography, green background",
                    "Traditional Chengdu street with tea houses, Sichuan architecture, people enjoying tea, warm lighting, professional travel photography",
                    "Chengdu skyline with panda-themed elements, modern city with traditional touches, professional cityscape"
                ],
                "priority": 1,  # High priority for panda images
                "needs_ai": True
            },
            "Harbin": {
                "prompts": [
                    "Harbin Ice Festival at night, magnificent ice sculptures, colorful lights, winter wonderland, professional photography, 16:9 aspect ratio",
                    "Ice and snow architecture in Harbin, detailed ice carvings, blue ice, professional winter photography",
                    "Saint Sophia Cathedral in Harbin covered in snow, Russian architecture, winter scene, professional travel photography"
                ],
                "priority": 1,  # High priority for ice festival
                "needs_ai": True
            },
            "Chongqing": {
                "prompts": [
                    "Chongqing mountain cityscape at night, buildings on hills, river reflections, neon lights, professional city photography, 16:9",
                    "Hongya Cave in Chongqing, traditional architecture on cliffs, river view, professional travel photography",
                    "Aerial view of Chongqing showing mountainous terrain and rivers, professional drone photography"
                ],
                "priority": 1,  # High priority for city view
                "needs_ai": True
            },
            "Wuxi": {
                "prompts": [
                    "Taihu Lake in Wuxi, serene water, lotus flowers, traditional boats, professional landscape photography, 16:9 aspect ratio",
                    "Lingshan Grand Buddha in Wuxi, giant bronze statue, Buddhist temple, professional travel photography",
                    "Wuxi ancient town with canals, traditional architecture, professional photography"
                ],
                "priority": 2,
                "needs_ai": False  # Can use stock photos
            },
            "Qingdao": {
                "prompts": [
                    "Qingdao beaches with European architecture, blue sea, red roofs, professional coastal photography, 16:9",
                    "Zhanqiao Pier in Qingdao, historical landmark, ocean view, professional travel photography",
                    "Tsingtao Brewery historical building, German architecture, professional photography"
                ],
                "priority": 2,
                "needs_ai": False
            },
            "Xiamen": {
                "prompts": [
                    "Gulangyu Island in Xiamen, colonial architecture, ocean view, professional island photography, 16:9",
                    "Xiamen University campus, traditional Chinese architecture with modern elements, professional photography",
                    "Xiamen coastal road, palm trees, ocean, professional travel photography"
                ],
                "priority": 2,
                "needs_ai": False
            },
            "Nanjing": {
                "prompts": [
                    "Confucius Temple in Nanjing, ancient architecture, Qinhuai River, night lights, professional travel photography",
                    "Sun Yat-sen Mausoleum in Nanjing, grand staircase, blue roofs, professional architectural photography",
                    "Nanjing city wall, historical fortress, professional photography"
                ],
                "priority": 2,
                "needs_ai": False
            },
            "Shenzhen": {
                "prompts": [
                    "Shenzhen modern skyline, glass skyscrapers, futuristic architecture, professional cityscape photography, 16:9",
                    "Shenzhen technology district, innovative buildings, professional architectural photography",
                    "Window of the World in Shenzhen, global landmarks, professional travel photography"
                ],
                "priority": 2,
                "needs_ai": False
            },
            "Guangzhou": {
                "prompts": [
                    "Canton Tower in Guangzhou, modern architecture, Pearl River, professional city photography, 16:9",
                    "Chen Clan Ancestral Hall, traditional Cantonese architecture, detailed carvings, professional photography",
                    "Guangzhou old and new contrast, traditional buildings with skyscrapers, professional travel photography"
                ],
                "priority": 2,
                "needs_ai": False
            },
            "Hongkong": {
                "prompts": [
                    "Hong Kong Victoria Harbour skyline at night, skyscrapers, neon lights, professional cityscape photography, 16:9",
                    "Hong Kong street scene, neon signs, bustling city life, professional travel photography",
                    "Hong Kong from Victoria Peak, panoramic view, professional photography"
                ],
                "priority": 2,
                "needs_ai": False
            }
        }
    
    def generate_with_dalle(self, prompt, city_name):
        """Generate image using OpenAI DALL-E."""
        # This is a placeholder - would need actual API integration
        print(f"🔧 Would generate DALL-E image for {city_name}")
        print(f"   Prompt: {prompt[:100]}...")
        
        # In a real implementation, this would call the DALL-E API
        # and return the image URL or save the image locally
        
        return None
    
    def generate_with_stability(self, prompt, city_name):
        """Generate image using Stability AI."""
        # This is a placeholder - would need actual API integration
        print(f"🔧 Would generate Stability AI image for {city_name}")
        print(f"   Prompt: {prompt[:100]}...")
        
        return None
    
    def generate_local_sd(self, prompt, city_name):
        """Generate image using local Stable Diffusion."""
        # This is a placeholder - would need local SD setup
        print(f"🔧 Would generate local Stable Diffusion image for {city_name}")
        print(f"   Prompt: {prompt[:100]}...")
        
        return None
    
    def find_stock_photo(self, city_name, query):
        """Find appropriate stock photo for a city."""
        # This would search stock photo APIs
        print(f"🔍 Searching stock photos for {city_name}: {query}")
        
        # Placeholder - in real implementation, would search Unsplash, Pexels, etc.
        # and return the best matching image URL
        
        return None
    
    def generate_city_image(self, city_name, method="best_available"):
        """Generate or find an image for a city."""
        
        if city_name not in self.config["city_prompts"]:
            print(f"❌ No prompts defined for {city_name}")
            return None
        
        city_info = self.config["city_prompts"][city_name]
        prompts = city_info["prompts"]
        
        print(f"\n🎨 Generating image for {city_name}...")
        print(f"   Priority: {city_info['priority']}")
        print(f"   Needs AI: {city_info['needs_ai']}")
        
        image_url = None
        
        # Try different methods based on priority and needs
        if city_info["needs_ai"] and city_info["priority"] == 1:
            # High priority cities that need AI (Chengdu, Harbin, Chongqing)
            print(f"   ⚡ HIGH PRIORITY - Using AI generation")
            
            # Try DALL-E if configured
            if self.config["ai_services"]["openai_dalle"]["enabled"]:
                image_url = self.generate_with_dalle(prompts[0], city_name)
            
            # Try Stability AI if DALL-E failed
            if not image_url and self.config["ai_services"]["stability_ai"]["enabled"]:
                image_url = self.generate_with_stability(prompts[0], city_name)
            
            # Try local SD if others failed
            if not image_url and self.config["ai_services"]["local_sd"]["enabled"]:
                image_url = self.generate_local_sd(prompts[0], city_name)
        
        # If AI generation not available or not needed, try stock photos
        if not image_url:
            print(f"   📸 Searching for stock photo")
            # Use the first prompt as search query
            search_query = prompts[0].split(",")[0]  # First part of prompt
            image_url = self.find_stock_photo(city_name, search_query)
        
        # Update generation status
        if city_name not in self.config["generation_status"]:
            self.config["generation_status"][city_name] = {}
        
        self.config["generation_status"][city_name].update({
            "last_attempt": datetime.now().isoformat(),
            "success": image_url is not None,
            "method_used": method
        })
        
        # Save config
        self.save_config()
        
        return image_url
    
    def save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def generate_all_city_images(self):
        """Generate images for all cities."""
        print("=" * 60)
        print("AI IMAGE GENERATION FOR ALL CITIES")
        print("=" * 60)
        
        results = {}
        
        # Sort cities by priority (highest first)
        cities_by_priority = sorted(
            self.config["city_prompts"].items(),
            key=lambda x: x[1]["priority"]
        )
        
        for city_name, city_info in cities_by_priority:
            image_url = self.generate_city_image(city_name)
            results[city_name] = {
                "success": image_url is not None,
                "url": image_url,
                "priority": city_info["priority"]
            }
            
            if image_url:
                print(f"✅ {city_name}: Generated successfully")
            else:
                print(f"❌ {city_name}: Failed to generate")
        
        # Summary
        print("\n" + "=" * 60)
        print("GENERATION SUMMARY")
        print("=" * 60)
        
        successful = sum(1 for r in results.values() if r["success"])
        total = len(results)
        
        print(f"Successful: {successful}/{total} ({successful/total*100:.1f}%)")
        
        # High priority cities status
        print("\nHigh Priority Cities (Chengdu, Harbin, Chongqing):")
        high_priority = ["Chengdu", "Harbin", "Chongqing"]
        for city in high_priority:
            if city in results:
                status = "✅" if results[city]["success"] else "❌"
                print(f"  {status} {city}")
        
        return results
    
    def setup_instructions(self):
        """Print setup instructions for AI services."""
        print("=" * 60)
        print("AI IMAGE GENERATION SETUP INSTRUCTIONS")
        print("=" * 60)
        
        print("\n🔧 To enable AI image generation, you need to:")
        
        print("\n1. OpenAI DALL-E (Recommended for quality):")
        print("   • Get API key from https://platform.openai.com/api-keys")
        print("   • Add to ai_image_config.json:")
        print('     "openai_dalle": {')
        print('       "enabled": true,')
        print('       "api_key": "your-key-here"')
        print('     }')
        
        print("\n2. Stability AI:")
        print("   • Get API key from https://platform.stability.ai/")
        print("   • Add to config file")
        
        print("\n3. Local Stable Diffusion:")
        print("   • Install Automatic1111 or ComfyUI")
        print("   • Run locally on http://localhost:7860")
        print("   • Enable in config")
        
        print("\n🎯 Priority Cities for AI Generation:")
        print("   • Chengdu - Needs panda images")
        print("   • Harbin - Needs ice festival images")
        print("   • Chongqing - Needs mountain city views")
        
        print("\n📝 Current config saved to: ai_image_config.json")

def main():
    """Main function."""
    generator = AIImageGenerator()
    
    print("🔧 AI Image Generator for Travel Website")
    print("=" * 40)
    
    # Show setup instructions
    generator.setup_instructions()
    
    print("\n" + "=" * 60)
    print("QUICK START")
    print("=" * 60)
    
    print("\nTo generate images for priority cities:")
    print("1. Enable an AI service in ai_image_config.json")
    print("2. Run: python3 ai_image_generator.py --generate")
    print("3. Images will be saved to ai_generated_images/")
    
    print("\n💡 Tip: Start with Chengdu to test panda image generation!")

if __name__ == "__main__":
    main()