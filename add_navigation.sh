#!/bin/bash

# This script adds the navigation system to HTML files

# Navigation CSS to be added before </style>
NAV_CSS='
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
            font-family: '"'"'Inter'"'"', '"'"'Segoe UI'"'"', Tahoma, Geneva, Verdana, sans-serif;
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

        /* Mobile Menu Overlay */
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

        /* Mobile Styles */
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
'

echo "Navigation CSS prepared"
echo "This is a placeholder script - actual implementation will use Edit tool"
