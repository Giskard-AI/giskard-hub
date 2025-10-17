/**
 * Custom functionality for Giskard documentation
 * Left sidebar scroll to current item on page load
 * Enterprise trial banner management
 * Dynamic current page highlighting for sidebar navigation
 */
(function() {
  'use strict';

  // Wait for Alpine.js to be ready
  function waitForAlpine(callback) {
    if (window.Alpine) {
      callback();
    } else {
      setTimeout(() => waitForAlpine(callback), 50);
    }
  }

  // Store the current page state to persist across Alpine.js updates
  let currentPageState = {
    currentPath: null,
    currentLink: null,
    expandedSections: new Set(),
    lastSelectedNavbarItem: null
  };

  // Apply current classes immediately on page load, before Alpine.js initializes
  function applyCurrentClassesImmediately() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    const currentPath = window.location.pathname;
    currentPageState.currentPath = currentPath;
    
    // First, remove all existing current classes
    sidebar.querySelectorAll('.current').forEach(el => {
      el.classList.remove('current');
      el.removeAttribute('data-current');
    });
    
    // Find all navigation links
    const navLinks = sidebar.querySelectorAll('a[href]');
    let bestMatch = null;
    let bestMatchDepth = -1;
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href) return;
      
      // Handle different href formats
      let linkPath = href;
      
      // Remove hash from href for comparison
      if (linkPath.includes('#')) {
        linkPath = linkPath.split('#')[0];
      }
      
      // Handle relative paths
      if (linkPath.startsWith('../')) {
        // Convert relative path to absolute for comparison
        const pathSegments = currentPath.split('/').filter(seg => seg);
        const linkSegments = linkPath.split('/').filter(seg => seg);
        
        // Count how many levels up we need to go
        let upLevels = 0;
        for (const seg of linkSegments) {
          if (seg === '..') {
            upLevels++;
          } else {
            break;
          }
        }
        
        // Build the absolute path
        const remainingSegments = pathSegments.slice(0, -upLevels);
        const linkFileName = linkSegments[linkSegments.length - 1];
        linkPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
      } else if (linkPath.startsWith('./')) {
        // Handle same-directory links
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath.substring(2);
      } else if (!linkPath.startsWith('/') && !linkPath.startsWith('http')) {
        // Handle relative links without ./
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath;
      }
      
      // Normalize paths for comparison
      const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
      const normalizedLinkPath = linkPath.replace(/\/$/, '') || '/index.html';
      
      // Check if this link matches the current page
      const isExactMatch = normalizedCurrentPath === normalizedLinkPath;
      const isMainIndex = normalizedCurrentPath === '/index.html';
      
      // For main index page, only allow exact matches
      if (isMainIndex) {
        if (isExactMatch) {
          bestMatch = link;
          bestMatchDepth = 0; // Main index has highest priority
        }
      } else {
        // For other pages, use the original matching logic
        if (normalizedCurrentPath === normalizedLinkPath || 
            normalizedCurrentPath.endsWith(normalizedLinkPath) ||
            normalizedLinkPath.endsWith(normalizedCurrentPath)) {
          
          // Calculate the depth of this link (how many levels deep it is)
          const depth = linkPath.split('/').length;
          
          // Priority rules for non-index pages:
          // 1. Exact matches get highest priority
          // 2. Otherwise, deeper matches get priority
          let shouldUpdate = false;
          
          if (isExactMatch) {
            // Exact match always wins
            shouldUpdate = true;
          } else if (depth > bestMatchDepth) {
            // Deeper match gets priority
            shouldUpdate = true;
          }
          
          if (shouldUpdate) {
            bestMatch = link;
            bestMatchDepth = depth;
          }
        }
      }
    });
    
    // Apply current class only to the best match and its parents
    if (bestMatch) {
      bestMatch.classList.add('current');
      bestMatch.setAttribute('data-current', 'true');
      
      // Add current class to parent li elements
      let parentLi = bestMatch.closest('li');
      while (parentLi) {
        parentLi.classList.add('current');
        parentLi = parentLi.parentElement?.closest('li');
      }
    }
  }

  // Force expand Alpine.js sections that contain current page
  function forceExpandCurrentSections() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    // Find all Alpine.js components that should be expanded
    const alpineComponents = sidebar.querySelectorAll('[x-data]');
    
    alpineComponents.forEach(component => {
      // Check if this component or its descendants contain a current link
      const hasCurrent = component.querySelector('.current');
      
      if (hasCurrent) {
        // Wait for Alpine.js to be ready, then force expansion
        waitForAlpine(() => {
          try {
            if (window.Alpine && Alpine.$data) {
              const alpineData = Alpine.$data(component);
              if (alpineData && typeof alpineData.expanded !== 'undefined') {
                alpineData.expanded = true;
              }
            }
          } catch (e) {
            // Fallback: simulate click on expand button
            const expandButton = component.querySelector('button[type="button"]');
            if (expandButton) {
              expandButton.click();
            }
          }
        });
      }
    });
  }

  function highlightCurrentPage() {
    // Find the left sidebar
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    // Get current page URL
    const currentPath = window.location.pathname;
    currentPageState.currentPath = currentPath;
    
    // Remove any existing current classes
    sidebar.querySelectorAll('.current').forEach(el => {
      el.classList.remove('current');
      el.removeAttribute('data-current');
    });
    
    // Find all navigation links
    const navLinks = sidebar.querySelectorAll('a[href]');
    let bestMatch = null;
    let bestMatchDepth = -1;
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href) return;
      
      // Handle different href formats
      let linkPath = href;
      
      // Remove hash from href for comparison
      if (linkPath.includes('#')) {
        linkPath = linkPath.split('#')[0];
      }
      
      // Handle relative paths
      if (linkPath.startsWith('../')) {
        // Convert relative path to absolute for comparison
        const pathSegments = currentPath.split('/').filter(seg => seg);
        const linkSegments = linkPath.split('/').filter(seg => seg);
        
        // Count how many levels up we need to go
        let upLevels = 0;
        for (const seg of linkSegments) {
          if (seg === '..') {
            upLevels++;
          } else {
            break;
          }
        }
        
        // Build the absolute path
        const remainingSegments = pathSegments.slice(0, -upLevels);
        const linkFileName = linkSegments[linkSegments.length - 1];
        linkPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
      } else if (linkPath.startsWith('./')) {
        // Handle same-directory links
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath.substring(2);
      } else if (!linkPath.startsWith('/') && !linkPath.startsWith('http')) {
        // Handle relative links without ./
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath;
      }
      
      // Normalize paths for comparison
      const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
      const normalizedLinkPath = linkPath.replace(/\/$/, '') || '/index.html';
      
      // Check if this link matches the current page
      const isExactMatch = normalizedCurrentPath === normalizedLinkPath;
      const isMainIndex = normalizedCurrentPath === '/index.html';
      
      // For main index page, only allow exact matches
      if (isMainIndex) {
        if (isExactMatch) {
          bestMatch = link;
          bestMatchDepth = 0; // Main index has highest priority
        }
      } else {
        // For other pages, use the original matching logic
        if (normalizedCurrentPath === normalizedLinkPath || 
            normalizedCurrentPath.endsWith(normalizedLinkPath) ||
            normalizedLinkPath.endsWith(normalizedCurrentPath)) {
          
          // Calculate the depth of this link (how many levels deep it is)
          const depth = linkPath.split('/').length;
          
          // Priority rules for non-index pages:
          // 1. Exact matches get highest priority
          // 2. Otherwise, deeper matches get priority
          let shouldUpdate = false;
          
          if (isExactMatch) {
            // Exact match always wins
            shouldUpdate = true;
          } else if (depth > bestMatchDepth) {
            // Deeper match gets priority
            shouldUpdate = true;
          }
          
          if (shouldUpdate) {
            bestMatch = link;
            bestMatchDepth = depth;
          }
        }
      }
    });
    
    // Apply current class only to the best match and its parents
    if (bestMatch) {
      currentPageState.currentLink = bestMatch;
      
      bestMatch.classList.add('current');
      bestMatch.setAttribute('data-current', 'true');
      
      // Add current class to parent li elements
      let parentLi = bestMatch.closest('li');
      while (parentLi) {
        parentLi.classList.add('current');
        parentLi = parentLi.parentElement?.closest('li');
      }
    }
    
    // Expand parent sections using Alpine.js
    if (bestMatch) {
      // Find all parent li elements with x-data that contain this link
      const allParentLis = [];
      let currentLi = bestMatch.closest('li');
      while (currentLi) {
        allParentLis.push(currentLi);
        currentLi = currentLi.parentElement?.closest('li');
      }
      
      // For each parent li with Alpine.js, expand it
      allParentLis.forEach(li => {
        if (li.hasAttribute('x-data')) {
          // Store this section as expanded
          const sectionId = li.getAttribute('href') || li.textContent.trim();
          currentPageState.expandedSections.add(sectionId);
          
          // Wait for Alpine.js to be ready before trying to expand
          waitForAlpine(() => {
            // Try multiple approaches to expand the section
            const alpineData = li.getAttribute('x-data');
            if (alpineData && alpineData.includes('expanded')) {
              // Method 1: Direct Alpine.js access
              if (window.Alpine && Alpine.$data) {
                try {
                  const alpineComponent = Alpine.$data(li);
                  if (alpineComponent && typeof alpineComponent.expanded !== 'undefined') {
                    alpineComponent.expanded = true;
                  }
                } catch (e) {
                  // Method 2: Dispatch a custom event
                  li.dispatchEvent(new CustomEvent('alpine:expand'));
                }
              }
              
              // Method 3: Simulate a click on the expand button
              const expandButton = li.querySelector('button[type="button"]');
              if (expandButton) {
                expandButton.click();
              }
            }
          });
        }
      });
    }
  }

  // Function to manage multiple toctree sections visibility
  function manageToctreeSections() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    const currentPath = window.location.pathname;
    
    // Find all navigation sections (each nav element with caption)
    const navSections = sidebar.querySelectorAll('nav');
    
    // If there's only one nav section, don't hide anything
    if (navSections.length <= 1) return;
    
    // Find the nav section that contains a link matching the current path
    let activeNavSection = null;
    
    navSections.forEach(nav => {
      const links = nav.querySelectorAll('a[href]');
      let hasMatchingLink = false;
      
      links.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;
        
        // Handle different href formats
        let linkPath = href;
        
        // Remove hash from href for comparison
        if (linkPath.includes('#')) {
          linkPath = linkPath.split('#')[0];
        }
        
        // Handle relative paths
        if (linkPath.startsWith('../')) {
          // Convert relative path to absolute for comparison
          const pathSegments = currentPath.split('/').filter(seg => seg);
          const linkSegments = linkPath.split('/').filter(seg => seg);
          
          // Count how many levels up we need to go
          let upLevels = 0;
          for (const seg of linkSegments) {
            if (seg === '..') {
              upLevels++;
            } else {
              break;
            }
          }
          
          // Build the absolute path
          const remainingSegments = pathSegments.slice(0, -upLevels);
          const linkFileName = linkSegments[linkSegments.length - 1];
          linkPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
        } else if (linkPath.startsWith('./')) {
          // Handle same-directory links
          const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
          linkPath = currentDir + linkPath.substring(2);
        } else if (!linkPath.startsWith('/') && !linkPath.startsWith('http')) {
          // Handle relative links without ./
          const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
          linkPath = currentDir + linkPath;
        }
        
        // Normalize paths for comparison
        const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
        const normalizedLinkPath = linkPath.replace(/\/$/, '') || '/index.html';
        
        // Check if this link matches the current page
        if (normalizedCurrentPath === normalizedLinkPath || 
            normalizedCurrentPath.endsWith(normalizedLinkPath) ||
            normalizedLinkPath.endsWith(normalizedCurrentPath)) {
          hasMatchingLink = true;
        }
      });
      
      if (hasMatchingLink) {
        activeNavSection = nav;
      }
    });
    
    // Show/hide navigation sections
    navSections.forEach(nav => {
      if (nav === activeNavSection) {
        nav.style.display = 'block';
        nav.classList.remove('hidden-toctree');
      } else {
        nav.style.display = 'none';
        nav.classList.add('hidden-toctree');
      }
    });
  }

  // Function to restore state after Alpine.js updates
  function restoreSidebarState() {
    if (!currentPageState.currentPath) return;
    
    // Only restore current page highlighting, don't interfere with Alpine.js expanded state
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;
    
    // Remove any existing current classes
    sidebar.querySelectorAll('.current').forEach(el => {
      el.classList.remove('current');
      el.removeAttribute('data-current');
    });
    
    // Re-highlight current page without expanding sections
    const navLinks = sidebar.querySelectorAll('a[href]');
    const currentPath = currentPageState.currentPath;
    let bestMatch = null;
    let bestMatchDepth = -1;
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href) return;
      
      // Handle different href formats (same logic as highlightCurrentPage)
      let linkPath = href;
      
      if (linkPath.includes('#')) {
        linkPath = linkPath.split('#')[0];
      }
      
      if (linkPath.startsWith('../')) {
        const pathSegments = currentPath.split('/').filter(seg => seg);
        const linkSegments = linkPath.split('/').filter(seg => seg);
        
        let upLevels = 0;
        for (const seg of linkSegments) {
          if (seg === '..') {
            upLevels++;
          } else {
            break;
          }
        }
        
        const remainingSegments = pathSegments.slice(0, -upLevels);
        const linkFileName = linkSegments[linkSegments.length - 1];
        linkPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
      } else if (linkPath.startsWith('./')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath.substring(2);
      } else if (!linkPath.startsWith('/') && !linkPath.startsWith('http')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath;
      }
      
      const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
      const normalizedLinkPath = linkPath.replace(/\/$/, '') || '/index.html';
      
      if (normalizedCurrentPath === normalizedLinkPath || 
          normalizedCurrentPath.endsWith(normalizedLinkPath) ||
          normalizedLinkPath.endsWith(normalizedCurrentPath)) {
        
        // Calculate the depth of this link (how many levels deep it is)
        const depth = linkPath.split('/').length;
        
        // Special handling for index pages - prioritize exact matches
        const isExactMatch = normalizedCurrentPath === normalizedLinkPath;
        const isMainIndex = normalizedCurrentPath === '/index.html' && normalizedLinkPath === '/index.html';
        
        // Priority rules:
        // 1. Exact matches get highest priority
        // 2. Main index page gets priority over nested index pages
        // 3. Otherwise, deeper matches get priority
        let shouldUpdate = false;
        
        if (isExactMatch) {
          // Exact match always wins
          shouldUpdate = true;
        } else if (isMainIndex) {
          // Main index page gets priority
          shouldUpdate = true;
        } else if (depth > bestMatchDepth) {
          // Deeper match gets priority
          shouldUpdate = true;
        }
        
        if (shouldUpdate) {
          bestMatch = link;
          bestMatchDepth = depth;
        }
      }
    });
    
    // Apply current class only to the best match and its parents
    if (bestMatch) {
      bestMatch.classList.add('current');
      bestMatch.setAttribute('data-current', 'true');
      
      // Add current class to parent li elements
      let parentLi = bestMatch.closest('li');
      while (parentLi) {
        parentLi.classList.add('current');
        parentLi = parentLi.parentElement?.closest('li');
      }
    }
  }

  function scrollToCurrentItem() {
    // Find the left sidebar
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    // Find the current/active item with multiple selector fallbacks
    const currentItem = sidebar.querySelector('a.current') ||
                       sidebar.querySelector('.current a') ||
                       sidebar.querySelector('li.current a') ||
                       sidebar.querySelector('.toctree-l1.current a') ||
                       sidebar.querySelector('[aria-current="page"]');

    if (currentItem) {
      // Small delay to ensure DOM is fully rendered
      setTimeout(() => {
        // Get the position of the current item relative to the sidebar
        const sidebarRect = sidebar.getBoundingClientRect();
        const itemRect = currentItem.getBoundingClientRect();
        const relativeTop = itemRect.top - sidebarRect.top;
        const sidebarHeight = sidebar.clientHeight;

        // Calculate the scroll position to center the item in the sidebar
        const scrollTop = sidebar.scrollTop + relativeTop - (sidebarHeight / 2) + (itemRect.height / 2);

        // Scroll only the sidebar, not the entire page
        sidebar.scrollTo({
          top: scrollTop,
          behavior: 'smooth'
        });
      }, 100);
    }
  }

  // Function to highlight the most recently selected navbar item
  function highlightNavbarItem() {
    const header = document.querySelector('header');
    if (!header) return;

    const currentPath = window.location.pathname;
    
    // Find navbar links
    const navbarLinks = header.querySelectorAll('nav a[href]');
    let bestMatch = null;
    let currentSection = null;
    
    // First, determine which navbar section the current page belongs to
    navbarLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href) return;
      
      // Handle different href formats
      let linkPath = href;
      
      // Remove hash from href for comparison
      if (linkPath.includes('#')) {
        linkPath = linkPath.split('#')[0];
      }
      
      // Handle relative paths
      if (linkPath.startsWith('../')) {
        const pathSegments = currentPath.split('/').filter(seg => seg);
        const linkSegments = linkPath.split('/').filter(seg => seg);
        
        let upLevels = 0;
        for (const seg of linkSegments) {
          if (seg === '..') {
            upLevels++;
          } else {
            break;
          }
        }
        
        const remainingSegments = pathSegments.slice(0, -upLevels);
        const linkFileName = linkSegments[linkSegments.length - 1];
        linkPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
      } else if (linkPath.startsWith('./')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath.substring(2);
      } else if (!linkPath.startsWith('/') && !linkPath.startsWith('http')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        linkPath = currentDir + linkPath;
      }
      
      // Normalize paths for comparison
      const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
      const normalizedLinkPath = linkPath.replace(/\/$/, '') || '/index.html';
      
      // Check if this navbar link matches the current page or is a parent section
      if (normalizedCurrentPath === normalizedLinkPath || 
          normalizedCurrentPath.startsWith(normalizedLinkPath + '/')) {
        bestMatch = link;
        currentSection = normalizedLinkPath;
      }
    });
    
    // Check if we're still in the same section as the previously selected navbar item
    const lastSelectedHref = sessionStorage.getItem('lastSelectedNavbarItem');
    let shouldUpdateHighlighting = true;
    
    if (lastSelectedHref && currentSection) {
      // Find the previously selected navbar link
      const lastSelectedLink = Array.from(navbarLinks).find(link => link.getAttribute('href') === lastSelectedHref);
      
      if (lastSelectedLink) {
        // Check if the previously selected section still contains the current page
        let lastSelectedPath = lastSelectedHref;
        
        // Handle relative paths for the last selected link
        if (lastSelectedPath.startsWith('../')) {
          const pathSegments = currentPath.split('/').filter(seg => seg);
          const linkSegments = lastSelectedPath.split('/').filter(seg => seg);
          
          let upLevels = 0;
          for (const seg of linkSegments) {
            if (seg === '..') {
              upLevels++;
            } else {
              break;
            }
          }
          
          const remainingSegments = pathSegments.slice(0, -upLevels);
          const linkFileName = linkSegments[linkSegments.length - 1];
          lastSelectedPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
        } else if (lastSelectedPath.startsWith('./')) {
          const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
          lastSelectedPath = currentDir + lastSelectedPath.substring(2);
        } else if (!lastSelectedPath.startsWith('/') && !lastSelectedPath.startsWith('http')) {
          const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
          lastSelectedPath = currentDir + lastSelectedPath;
        }
        
        const normalizedLastSelectedPath = lastSelectedPath.replace(/\/$/, '') || '/index.html';
        
        // If current page is still within the last selected section, keep it highlighted
        if (normalizedCurrentPath === normalizedLastSelectedPath || 
            normalizedCurrentPath.startsWith(normalizedLastSelectedPath + '/')) {
          shouldUpdateHighlighting = false;
          // Keep the existing highlighting
          lastSelectedLink.classList.add('recently-selected');
          currentPageState.lastSelectedNavbarItem = lastSelectedLink;
        }
      }
    }
    
    // Only update highlighting if we're switching to a different section
    if (shouldUpdateHighlighting) {
      // Remove any existing recently-selected classes from navbar
      header.querySelectorAll('a.recently-selected').forEach(el => {
        el.classList.remove('recently-selected');
      });
      
      // Apply recently-selected class to the best match
      if (bestMatch) {
        bestMatch.classList.add('recently-selected');
        currentPageState.lastSelectedNavbarItem = bestMatch;
        
        // Store in sessionStorage for persistence across page loads
        sessionStorage.setItem('lastSelectedNavbarItem', bestMatch.getAttribute('href'));
      }
    }
  }

  // Function to restore navbar highlighting from sessionStorage
  function restoreNavbarHighlighting() {
    const header = document.querySelector('header');
    if (!header) return;
    
    const lastSelectedHref = sessionStorage.getItem('lastSelectedNavbarItem');
    if (!lastSelectedHref) return;
    
    const currentPath = window.location.pathname;
    
    // Find the navbar link that matches the stored href
    const navbarLinks = header.querySelectorAll('nav a[href]');
    const lastSelectedLink = Array.from(navbarLinks).find(link => link.getAttribute('href') === lastSelectedHref);
    
    if (lastSelectedLink) {
      // Check if the current page is still within the last selected section
      let lastSelectedPath = lastSelectedHref;
      
      // Handle relative paths for the last selected link
      if (lastSelectedPath.startsWith('../')) {
        const pathSegments = currentPath.split('/').filter(seg => seg);
        const linkSegments = lastSelectedPath.split('/').filter(seg => seg);
        
        let upLevels = 0;
        for (const seg of linkSegments) {
          if (seg === '..') {
            upLevels++;
          } else {
            break;
          }
        }
        
        const remainingSegments = pathSegments.slice(0, -upLevels);
        const linkFileName = linkSegments[linkSegments.length - 1];
        lastSelectedPath = '/' + remainingSegments.join('/') + '/' + linkFileName;
      } else if (lastSelectedPath.startsWith('./')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        lastSelectedPath = currentDir + lastSelectedPath.substring(2);
      } else if (!lastSelectedPath.startsWith('/') && !lastSelectedPath.startsWith('http')) {
        const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        lastSelectedPath = currentDir + lastSelectedPath;
      }
      
      const normalizedCurrentPath = currentPath.replace(/\/$/, '') || '/index.html';
      const normalizedLastSelectedPath = lastSelectedPath.replace(/\/$/, '') || '/index.html';
      
      // Only restore highlighting if current page is still within the last selected section
      if (normalizedCurrentPath === normalizedLastSelectedPath || 
          normalizedCurrentPath.startsWith(normalizedLastSelectedPath + '/')) {
        lastSelectedLink.classList.add('recently-selected');
        currentPageState.lastSelectedNavbarItem = lastSelectedLink;
      } else {
        // Clear the stored selection if we're no longer in that section
        sessionStorage.removeItem('lastSelectedNavbarItem');
      }
    }
  }

  function createEnterpriseTrialBanner() {
    // Check if banner already exists to avoid duplicates
    if (document.querySelector('.enterprise-trial-banner')) {
      return;
    }

    // Check if banner was closed in this tab session
    if (sessionStorage.getItem('enterprise-trial-banner-closed') === 'true') {
      return;
    }

    // Create banner element
    const banner = document.createElement('div');
    banner.className = 'enterprise-trial-banner';
    const baseUrl = window.location.origin;
    banner.innerHTML = `
      <span>🚀 Ready to scale your AI testing? <a href="${baseUrl}/start/enterprise-trial.html">Request your free enterprise trial today! 🛡️</a> </span>
      <button class="close-btn" aria-label="Close banner">×</button>
    `;

    // Add banner to page
    document.body.appendChild(banner);
    document.body.classList.add('banner-visible');

    // Handle close button
    const closeBtn = banner.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
      // Hide banner with smooth animation
      banner.style.transform = 'translateY(-100%)';
      banner.style.opacity = '0';

      // Remove banner and update body class after animation
      setTimeout(() => {
        if (banner.parentNode) {
          banner.remove();
          document.body.classList.remove('banner-visible');
          // Remember that banner was closed in this tab session
          sessionStorage.setItem('enterprise-trial-banner-closed', 'true');
        }
      }, 300);
    });

    // Update banner theme when page theme changes
    function updateBannerTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      banner.classList.toggle('dark', isDark);
    }

    // Initial theme check
    updateBannerTheme();

    // Watch for theme changes
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          updateBannerTheme();
        }
      });
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
  }

  // Handle Sphinx navigation events to ensure banner persists
  function handleSphinxNavigation() {
    // Small delay to ensure DOM is ready after navigation
    setTimeout(() => {
      // Manage toctree sections visibility first
      manageToctreeSections();
      
      // Apply current classes immediately
      applyCurrentClassesImmediately();
      
      // Highlight navbar item
      highlightNavbarItem();
      
      // Wait for Alpine.js and then expand sections
      waitForAlpine(() => {
        highlightCurrentPage();
        forceExpandCurrentSections();
        scrollToCurrentItem();
      });
      
      // Only create banner if it wasn't previously closed in this tab
      if (sessionStorage.getItem('enterprise-trial-banner-closed') !== 'true') {
        createEnterpriseTrialBanner();
      }
    }, 100);
  }

  // Listen for Sphinx navigation events
  document.addEventListener('DOMContentLoaded', () => {
    // Manage toctree sections visibility first
    manageToctreeSections();
    
    // Apply current classes IMMEDIATELY, before Alpine.js initializes
    applyCurrentClassesImmediately();
    
    // Restore navbar highlighting from sessionStorage
    restoreNavbarHighlighting();
    
    // Highlight navbar item for current page
    highlightNavbarItem();
    
    // Initial banner creation
    createEnterpriseTrialBanner();

    // Wait for Alpine.js to be ready before highlighting current page
    waitForAlpine(() => {
      highlightCurrentPage();
      forceExpandCurrentSections();
      scrollToCurrentItem();
    });

    // Remove the aggressive MutationObserver that was interfering with Alpine.js
    // Alpine.js will handle its own state management

    // Listen for all navigation events more comprehensively
    document.addEventListener('click', (e) => {
      // Check if this is a documentation link
      if (e.target.matches('a[href*=".html"], a[href*="#"], a[href*="/"]')) {
        // Don't handle external links or anchor-only links
        const href = e.target.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('mailto:') && !href.startsWith('tel:')) {
          setTimeout(handleSphinxNavigation, 300);
        }
      }
      
      // Check if this is an expand/collapse button click
      if (e.target.matches('button[type="button"]') && e.target.closest('[x-data]')) {
        // Let Alpine.js handle the expansion/collapse naturally
        // We don't need to interfere with its state management
      }
    });

    // Listen for popstate events (browser back/forward)
    window.addEventListener('popstate', () => {
      setTimeout(handleSphinxNavigation, 200);
    });

    // Listen for Sphinx's internal navigation more aggressively
    const observer = new MutationObserver((mutations) => {
      let shouldRecreateBanner = false;

      mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
          // Check if this looks like a page navigation
          const hasNewContent = Array.from(mutation.addedNodes).some(node =>
            node.nodeType === Node.ELEMENT_NODE &&
            (node.classList?.contains('document') ||
             node.querySelector?.('.document') ||
             node.classList?.contains('section') ||
             node.querySelector?.('.section'))
          );

          if (hasNewContent) {
            shouldRecreateBanner = true;
          }
        }
      });

      if (shouldRecreateBanner) {
        setTimeout(handleSphinxNavigation, 100);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Also listen for URL changes
    let currentUrl = window.location.href;
    setInterval(() => {
      if (window.location.href !== currentUrl) {
        currentUrl = window.location.href;
        setTimeout(handleSphinxNavigation, 200);
      }
    }, 100);

    // Listen for Sphinx's page load events
    document.addEventListener('DOMContentLoaded', handleSphinxNavigation, true);

    // Listen for Sphinx's navigation completion
    if (window.SphinxRtdTheme) {
      // For ReadTheDocs theme
      document.addEventListener('click', (e) => {
        if (e.target.matches('a[href*=".html"]')) {
          setTimeout(handleSphinxNavigation, 500);
        }
      });
    }
  });

  // Also handle cases where DOM is already loaded
  if (document.readyState !== 'loading') {
    // Manage toctree sections visibility first
    manageToctreeSections();
    
    // Apply current classes IMMEDIATELY, before Alpine.js initializes
    applyCurrentClassesImmediately();
    
    // Restore navbar highlighting from sessionStorage
    restoreNavbarHighlighting();
    
    // Highlight navbar item for current page
    highlightNavbarItem();
    
    createEnterpriseTrialBanner();
    waitForAlpine(() => {
      highlightCurrentPage();
      forceExpandCurrentSections();
      scrollToCurrentItem();
    });
  }

})();