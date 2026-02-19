#!/usr/bin/env python3
"""
Batch image optimization script for travel website
Optimizes all images listed in the database as pending tasks
"""

import os
import sys
from PIL import Image
import subprocess
import json
from datetime import datetime

def get_pending_image_tasks():
    """Get all pending image optimization tasks from database"""
    try:
        # Query database for pending image optimization tasks
        cmd = [
            'psql', '-d', 'travel_website', '-U', 'fudongli', '-h', 'localhost',
            '-c', "SELECT id, idea FROM travel.travel_development_ideas WHERE is_fixed = false AND idea LIKE 'Optimize image%' ORDER BY id;",
            '-t', '-A', '-F', '|'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error querying database: {result.stderr}")
            return []
        
        tasks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 2:
                    task_id = parts[0].strip()
                    idea = parts[1].strip()
                    
                    # Extract image path from idea
                    # Format: "Optimize image ../images/user_photos/filename.jpg for city Cityname"
                    if 'Optimize image ' in idea and ' for city ' in idea:
                        image_path = idea.replace('Optimize image ', '').split(' for city ')[0].strip()
                        city = idea.split(' for city ')[1].strip()
                        
                        # Fix path if it starts with ../
                        if image_path.startswith('../'):
                            image_path = image_path[3:]  # Remove ../
                        
                        tasks.append({
                            'id': task_id,
                            'image_path': image_path,
                            'city': city,
                            'idea': idea
                        })
        
        return tasks
        
    except Exception as e:
        print(f"Error getting tasks from database: {e}")
        return []

def optimize_image(image_path, quality=85):
    """Optimize a single image"""
    if not os.path.exists(image_path):
        print(f"  ❌ File not found: {image_path}")
        return None
    
    original_size = os.path.getsize(image_path)
    
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get image info
            width, height = img.size
            format_info = img.format
            
            # Create temp path
            temp_path = image_path + '.optimized'
            
            # Save with optimization
            img.save(
                temp_path,
                'JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )
            
            optimized_size = os.path.getsize(temp_path)
            savings = original_size - optimized_size
            savings_percent = (savings / original_size) * 100 if original_size > 0 else 0
            
            # Replace if smaller
            if optimized_size < original_size:
                os.replace(temp_path, image_path)
                return {
                    'success': True,
                    'original_size': original_size,
                    'optimized_size': optimized_size,
                    'savings': savings,
                    'savings_percent': savings_percent,
                    'dimensions': f"{width}x{height}",
                    'format': format_info,
                    'message': f"Reduced by {savings_percent:.1f}%"
                }
            else:
                os.remove(temp_path)
                return {
                    'success': True,
                    'original_size': original_size,
                    'optimized_size': original_size,
                    'savings': 0,
                    'savings_percent': 0,
                    'dimensions': f"{width}x{height}",
                    'format': format_info,
                    'message': "Already optimized"
                }
                
    except Exception as e:
        print(f"  ❌ Error optimizing {image_path}: {e}")
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return {
            'success': False,
            'error': str(e)
        }

def mark_task_completed(task_id):
    """Mark a task as completed in the database"""
    try:
        cmd = [
            'psql', '-d', 'travel_website', '-U', 'fudongli', '-h', 'localhost',
            '-c', f"UPDATE travel.travel_development_ideas SET is_fixed = true, fixed_at = NOW() WHERE id = {task_id};"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ Database update failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error updating database: {e}")
        return False

def main():
    print("🖼️  BATCH IMAGE OPTIMIZATION")
    print("=" * 50)
    
    # Get pending tasks
    print("📋 Fetching pending image optimization tasks...")
    tasks = get_pending_image_tasks()
    
    if not tasks:
        print("✅ No pending image optimization tasks found!")
        return
    
    print(f"📊 Found {len(tasks)} images to optimize")
    print()
    
    # Process each task
    completed = 0
    failed = 0
    total_savings = 0
    total_original = 0
    total_optimized = 0
    
    for i, task in enumerate(tasks, 1):
        task_id = task['id']
        image_path = task['image_path']
        city = task['city']
        
        print(f"🔹 Task {i}/{len(tasks)}: {os.path.basename(image_path)} ({city})")
        print(f"   ID: {task_id}, Path: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"   ❌ File not found, skipping...")
            failed += 1
            continue
        
        # Optimize image
        result = optimize_image(image_path, quality=85)
        
        if result and result['success']:
            # Update totals
            total_original += result['original_size']
            total_optimized += result['optimized_size']
            total_savings += result['savings']
            
            # Mark task as completed
            if mark_task_completed(task_id):
                print(f"   ✅ {result['message']}")
                print(f"   📏 {result['dimensions']}, {result['format']}")
                print(f"   📊 {result['original_size']:,} → {result['optimized_size']:,} bytes")
                if result['savings'] > 0:
                    print(f"   💾 Saved: {result['savings']:,} bytes ({result['savings_percent']:.1f}%)")
                completed += 1
            else:
                print(f"   ⚠️  Optimized but database update failed")
                failed += 1
        else:
            print(f"   ❌ Optimization failed")
            if result and 'error' in result:
                print(f"   Error: {result['error']}")
            failed += 1
        
        print()
    
    # Print summary
    print("=" * 50)
    print("📈 OPTIMIZATION SUMMARY")
    print(f"✅ Completed: {completed} images")
    print(f"❌ Failed: {failed} images")
    print(f"📊 Total original size: {total_original:,} bytes")
    print(f"📊 Total optimized size: {total_optimized:,} bytes")
    
    if total_original > 0:
        overall_savings = total_original - total_optimized
        overall_savings_percent = (overall_savings / total_original) * 100
        print(f"💾 Total savings: {overall_savings:,} bytes ({overall_savings_percent:.1f}%)")
    
    # Update overall database stats
    print()
    print("📊 DATABASE STATUS UPDATE")
    try:
        cmd = [
            'psql', '-d', 'travel_website', '-U', 'fudongli', '-h', 'localhost',
            '-c', "SELECT COUNT(*) as total, COUNT(CASE WHEN is_fixed THEN 1 END) as completed, COUNT(CASE WHEN NOT is_fixed THEN 1 END) as pending FROM travel.travel_development_ideas;"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
    except:
        pass

if __name__ == "__main__":
    main()