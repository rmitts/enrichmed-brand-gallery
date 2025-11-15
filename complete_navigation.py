#!/usr/bin/env python3
"""
Script to add full navigation system to remaining HTML files
"""

import re
import os

# Navigation CSS block
NAV_CSS = '''
        /* Navigation Styles */
        .navigation {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(82, 111, 245, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            height: 70px;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
            color: #1c1a33;
            font-weight: 600;
            font-size: 18px;
        }

        .nav-brand-text {
            color: #1c1a33;
            font-weight: 600;
        }

        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }

        .nav-dropdown {
            position: relative;
        }

        .nav-dropdown-btn {
            background: none;
            border: none;
            color: #1c1a33;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            padding: 8px 16px;
            border-radius: 8px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .nav-dropdown-btn:hover {
            background: rgba(82, 111, 245, 0.1);
            color: #526ff5;
        }

        .nav-arrow {
            font-size: 12px;
            transition: transform 0.3s ease;
        }

        .nav-dropdown:hover .nav-arrow {
            transform: rotate(180deg);
        }

        .nav-dropdown-content {
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            min-width: 250px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(82, 111, 245, 0.1);
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            z-index: 1001;
        }

        .nav-dropdown:hover .nav-dropdown-content {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .nav-link {
            display: block;
            padding: 12px 20px;
            color: #64748b;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            border-radius: 8px;
            margin: 4px 8px;
        }

        .nav-link:hover {
            background: rgba(82, 111, 245, 0.1);
            color: #526ff5;
            transform: translateX(5px);
        }

        .nav-link.active {
            background: linear-gradient(135deg, #526ff5 0%, #7FB8E5 100%);
            color: white;
        }

        .nav-link.active:hover {
            background: linear-gradient(135deg, #4158d0 0%, #6ba3d6 100%);
            transform: translateX(5px);
        }

        .mobile-menu-btn {
            display: none;
            flex-direction: column;
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px;
        }

        .mobile-menu-btn span {
            width: 25px;
            height: 3px;
            background: #526ff5;
            margin: 3px 0;
            border-radius: 2px;
            transition: 0.3s;
        }

        .mobile-menu {
            position: fixed;
            top: 0;
            left: -100%;
            width: 85%;
            max-width: 400px;
            height: 100vh;
            background: white;
            z-index: 2000;
            transition: left 0.3s ease;
            overflow-y: auto;
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
        }

        .mobile-menu.active {
            left: 0;
        }

        .mobile-menu-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1999;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }

        .mobile-menu-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .mobile-menu-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }

        .mobile-menu-close {
            background: none;
            border: none;
            font-size: 28px;
            color: #526ff5;
            cursor: pointer;
            padding: 5px;
            line-height: 1;
        }

        .mobile-nav-section {
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }

        .mobile-nav-section-title {
            padding: 15px 20px;
            font-weight: 600;
            color: #526ff5;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .mobile-nav-link {
            display: block;
            padding: 12px 20px 12px 40px;
            color: #64748b;
            text-decoration: none;
            font-size: 15px;
            transition: all 0.2s ease;
        }

        .mobile-nav-link:hover,
        .mobile-nav-link.active {
            background: rgba(82, 111, 245, 0.1);
            color: #526ff5;
        }

        .mobile-menu-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(6px, 6px);
        }

        .mobile-menu-btn.active span:nth-child(2) {
            opacity: 0;
        }

        .mobile-menu-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(6px, -6px);
        }

        @media (max-width: 768px) {
            .nav-container {
                padding: 0 20px;
            }

            .nav-brand-text {
                display: none;
            }

            .nav-links {
                display: none;
            }

            .mobile-menu-btn {
                display: flex;
            }
        }
'''

def get_nav_html(active_page):
    """Generate navigation HTML with appropriate active class"""
    # Determine which link should be active based on filename
    active_links = {
        'enrichmed_final_logo_package.html': 'enrichmed_final_logo_package.html',
        'enrichmed_final_logo_package23.html': 'enrichmed_final_logo_package.html',
        'hybrid_concept_preview.html': 'hybrid_concept_preview.html',
        'Interactive logo design tool .html': 'Interactive logo design tool .html',
        'Logo Refinement Tool .html': 'Logo Refinement Tool .html',
        'logo symbol exploration.html': 'logo symbol exploration.html',
    }

    active_file = active_links.get(active_page, active_page)

    return f'''
    <!-- Navigation -->
    <nav class="navigation">
        <div class="nav-container">
            <div class="nav-brand">
                <svg width="40" height="40" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="navLogo" x1="0%" y1="50%" x2="100%" y2="50%">
                            <stop offset="0%" style="stop-color:#7FB8E5"/>
                            <stop offset="50%" style="stop-color:#526ff5"/>
                            <stop offset="100%" style="stop-color:#5DCAE3"/>
                        </linearGradient>
                    </defs>
                    <ellipse cx="100" cy="100" rx="70" ry="35" fill="url(#navLogo)" opacity="0.15"/>
                    <ellipse cx="100" cy="100" rx="35" ry="70" fill="url(#navLogo)" opacity="0.15"/>
                    <path d="M 100 40 A 60 60 0 0 1 160 100 L 140 100 A 40 40 0 0 0 100 60 Z" fill="#7FB8E5" opacity="0.9"/>
                    <path d="M 160 100 A 60 60 0 0 1 100 160 L 100 140 A 40 40 0 0 0 140 100 Z" fill="#5DCAE3" opacity="0.9"/>
                    <path d="M 100 160 A 60 60 0 0 1 40 100 L 60 100 A 40 40 0 0 0 100 140 Z" fill="#526ff5" opacity="0.9"/>
                    <path d="M 40 100 A 60 60 0 0 1 100 40 L 100 60 A 40 40 0 0 0 60 100 Z" fill="#64B5F6" opacity="0.9"/>
                    <path d="M 100 80 L 100 95" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 100 95 L 88 108 M 100 95 L 112 108" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
                    <circle cx="100" cy="95" r="5" fill="#ffffff"/>
                </svg>
                <span class="nav-brand-text">EnrichMed Brand Gallery</span>
            </div>
            <div class="nav-links">
                <div class="nav-dropdown">
                    <button class="nav-dropdown-btn">Logo Variations <span class="nav-arrow">▼</span></button>
                    <div class="nav-dropdown-content">
                        <a href="index.html" class="nav-link">Main Logo Package</a>
                        <a href="symbol-variations.html" class="nav-link">Symbol Variations Explorer</a>
                        <a href="logo symbol exploration.html" class="nav-link{'active' if active_file == 'logo symbol exploration.html' else ''}">Logo Symbol Exploration</a>
                        <a href="enrichmed_final_logo_package.html" class="nav-link{' active' if active_file == 'enrichmed_final_logo_package.html' else ''}">Final Logo Package</a>
                        <a href="hybrid_concept_preview.html" class="nav-link{' active' if active_file == 'hybrid_concept_preview.html' else ''}">Hybrid Concept Preview</a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="nav-dropdown-btn">Design Tools <span class="nav-arrow">▼</span></button>
                    <div class="nav-dropdown-content">
                        <a href="Interactive logo design tool .html" class="nav-link{' active' if active_file == 'Interactive logo design tool .html' else ''}">Interactive Design Tool</a>
                        <a href="Logo Refinement Tool .html" class="nav-link{' active' if active_file == 'Logo Refinement Tool .html' else ''}">Logo Refinement Tool</a>
                        <a href="color_palette_preview.html" class="nav-link">Color Palette Preview</a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="nav-dropdown-btn">Concepts <span class="nav-arrow">▼</span></button>
                    <div class="nav-dropdown-content">
                        <a href="Geometric Growth Hybrid.html" class="nav-link">Geometric Growth Hybrid</a>
                        <a href="pulmonary_nodule_management.html" class="nav-link">Medical Applications</a>
                    </div>
                </div>
            </div>
            <button class="mobile-menu-btn" id="mobileMenuBtn">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <!-- Mobile Menu Overlay -->
    <div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>

    <!-- Mobile Menu -->
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-header">
            <div class="nav-brand">
                <svg width="35" height="35" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="mobileLogo" x1="0%" y1="50%" x2="100%" y2="50%">
                            <stop offset="0%" style="stop-color:#7FB8E5"/>
                            <stop offset="50%" style="stop-color:#526ff5"/>
                            <stop offset="100%" style="stop-color:#5DCAE3"/>
                        </linearGradient>
                    </defs>
                    <ellipse cx="100" cy="100" rx="70" ry="35" fill="url(#mobileLogo)" opacity="0.15"/>
                    <ellipse cx="100" cy="100" rx="35" ry="70" fill="url(#mobileLogo)" opacity="0.15"/>
                    <path d="M 100 40 A 60 60 0 0 1 160 100 L 140 100 A 40 40 0 0 0 100 60 Z" fill="#7FB8E5" opacity="0.9"/>
                    <path d="M 160 100 A 60 60 0 0 1 100 160 L 100 140 A 40 40 0 0 0 140 100 Z" fill="#5DCAE3" opacity="0.9"/>
                    <path d="M 100 160 A 60 60 0 0 1 40 100 L 60 100 A 40 40 0 0 0 100 140 Z" fill="#526ff5" opacity="0.9"/>
                    <path d="M 40 100 A 60 60 0 0 1 100 40 L 100 60 A 40 40 0 0 0 60 100 Z" fill="#64B5F6" opacity="0.9"/>
                    <path d="M 100 80 L 100 95" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 100 95 L 88 108 M 100 95 L 112 108" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
                    <circle cx="100" cy="95" r="5" fill="#ffffff"/>
                </svg>
                <span style="color: #1c1a33; font-weight: 600;">EnrichMed</span>
            </div>
            <button class="mobile-menu-close" id="mobileMenuClose">&times;</button>
        </div>

        <div class="mobile-nav-section">
            <div class="mobile-nav-section-title">Logo Variations</div>
            <a href="index.html" class="mobile-nav-link">Main Logo Package</a>
            <a href="symbol-variations.html" class="mobile-nav-link">Symbol Variations Explorer</a>
            <a href="logo symbol exploration.html" class="mobile-nav-link{' active' if active_file == 'logo symbol exploration.html' else ''}">Logo Symbol Exploration</a>
            <a href="enrichmed_final_logo_package.html" class="mobile-nav-link{' active' if active_file == 'enrichmed_final_logo_package.html' else ''}">Final Logo Package</a>
            <a href="hybrid_concept_preview.html" class="mobile-nav-link{' active' if active_file == 'hybrid_concept_preview.html' else ''}">Hybrid Concept Preview</a>
        </div>

        <div class="mobile-nav-section">
            <div class="mobile-nav-section-title">Design Tools</div>
            <a href="Interactive logo design tool .html" class="mobile-nav-link{' active' if active_file == 'Interactive logo design tool .html' else ''}">Interactive Design Tool</a>
            <a href="Logo Refinement Tool .html" class="mobile-nav-link{' active' if active_file == 'Logo Refinement Tool .html' else ''}">Logo Refinement Tool</a>
            <a href="color_palette_preview.html" class="mobile-nav-link">Color Palette Preview</a>
        </div>

        <div class="mobile-nav-section">
            <div class="mobile-nav-section-title">Concepts</div>
            <a href="Geometric Growth Hybrid.html" class="mobile-nav-link">Geometric Growth Hybrid</a>
            <a href="pulmonary_nodule_management.html" class="mobile-nav-link">Medical Applications</a>
        </div>
    </div>
'''

MOBILE_JS = '''
        // Mobile Menu Toggle
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const mobileMenu = document.getElementById('mobileMenu');
        const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
        const mobileMenuClose = document.getElementById('mobileMenuClose');

        function toggleMobileMenu() {
            mobileMenuBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            mobileMenuOverlay.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        }

        function closeMobileMenu() {
            mobileMenuBtn.classList.remove('active');
            mobileMenu.classList.remove('active');
            mobileMenuOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
        mobileMenuClose.addEventListener('click', closeMobileMenu);
        mobileMenuOverlay.addEventListener('click', closeMobileMenu);

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

        // Close mobile menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
                closeMobileMenu();
            }
        });
'''

def process_file(filepath):
    """Add navigation to a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract just the filename for active link matching
    filename = os.path.basename(filepath)

    # 1. Add CSS before </style>
    if NAV_CSS not in content:
        content = content.replace('</style>', NAV_CSS + '    </style>')

    # 2. Add HTML after <body>
    nav_html = get_nav_html(filename)
    if '<!-- Navigation -->' not in content:
        # Find <body> tag (might have attributes)
        body_pattern = r'(<body[^>]*>)'
        content = re.sub(body_pattern, r'\1' + nav_html, content)

    # 3. Add JavaScript at beginning of <script> section
    if MOBILE_JS not in content and '<script>' in content:
        content = content.replace('<script>', '<script>' + MOBILE_JS, 1)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated: {filepath}")

# List of files to process
files = [
    'enrichmed_final_logo_package.html',
    'enrichmed_final_logo_package23.html',
    'hybrid_concept_preview.html',
    'Interactive logo design tool .html',
    'Logo Refinement Tool .html',
    'logo symbol exploration.html',
    'Variations/enrichmed_final_logo_package.html',
]

print("Starting navigation updates...\n")

for filepath in files:
    if os.path.exists(filepath):
        try:
            process_file(filepath)
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
    else:
        print(f"✗ File not found: {filepath}")

print("\n✓ Navigation update complete!")
