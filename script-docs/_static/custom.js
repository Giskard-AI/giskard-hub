/**
 * Custom functionality for Giskard documentation
 * Minimal implementation to prevent sidebar jitter
 */
(function () {
  'use strict';

  // Inject Google Tag Manager if not already present
  if (!document.querySelector('script[src*="googletagmanager.com/gtm.js"]')) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'gtm.start': new Date().getTime(),
      event: 'gtm.js'
    });

    var gtmScript = document.createElement('script');
    gtmScript.async = true;
    gtmScript.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-PQ9MJ64';
    var head = document.head || document.getElementsByTagName('head')[0];
    var firstScript = head.querySelector('script');
    if (firstScript) {
      head.insertBefore(gtmScript, firstScript);
    } else {
      head.appendChild(gtmScript);
    }

    if (!document.querySelector('noscript iframe[src*="googletagmanager.com/ns.html"]')) {
      var noscript = document.createElement('noscript');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.googletagmanager.com/ns.html?id=GTM-PQ9MJ64';
      iframe.height = '0';
      iframe.width = '0';
      iframe.style.display = 'none';
      iframe.style.visibility = 'hidden';
      noscript.appendChild(iframe);
      document.body.insertBefore(noscript, document.body.firstChild);
    }
  }

  // Expand parent sections that contain the current page - runs BEFORE Alpine initializes
  function preExpandCurrentSections() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    const currentPath = window.location.pathname.replace(/\/$/, '') || '/index.html';

    // Find the link matching current page
    const navLinks = sidebar.querySelectorAll('a[href]');
    let currentLink = null;

    for (const link of navLinks) {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('http')) continue;

      const linkPath = href.split('#')[0].replace(/\/$/, '') || '/index.html';

      if (currentPath === linkPath || currentPath.endsWith(linkPath)) {
        currentLink = link;
        break;
      }
    }

    if (!currentLink) return;

    // Mark all parent <li> elements with data-expand attribute BEFORE Alpine.js initializes
    let parentLi = currentLink.closest('li');
    while (parentLi) {
      if (parentLi.hasAttribute('x-data')) {
        // Modify the x-data attribute to start expanded
        const currentXData = parentLi.getAttribute('x-data');
        if (currentXData.includes('expanded: false')) {
          parentLi.setAttribute('x-data', currentXData.replace('expanded: false', 'expanded: true'));
        }
      }
      parentLi.classList.add('current');
      parentLi = parentLi.parentElement?.closest('li');
    }

    currentLink.classList.add('current');
  }

  // Save expanded state and scroll position before navigation
  function saveExpandedState() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    // Save scroll position
    sessionStorage.setItem('sidebarScrollTop', sidebar.scrollTop);

    // Save expanded dropdowns
    const expandedHrefs = [];
    sidebar.querySelectorAll('[x-data]').forEach(element => {
      const link = element.querySelector('a');
      if (link && link.href && element._x_dataStack && element._x_dataStack[0]?.expanded) {
        expandedHrefs.push(link.href);
      }
    });

    if (expandedHrefs.length > 0) {
      sessionStorage.setItem('expandedDropdowns', JSON.stringify(expandedHrefs));
    }
  }

  // Restore expanded state after navigation
  function restoreExpandedState() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    const savedState = sessionStorage.getItem('expandedDropdowns');
    if (!savedState) return;

    const expandedHrefs = new Set(JSON.parse(savedState));

    sidebar.querySelectorAll('[x-data]').forEach(element => {
      const link = element.querySelector('a');
      if (link && expandedHrefs.has(link.href)) {
        // Modify x-data before Alpine initializes
        const currentXData = element.getAttribute('x-data');
        if (currentXData.includes('expanded: false')) {
          element.setAttribute('x-data', currentXData.replace('expanded: false', 'expanded: true'));
        }
      }
    });
  }

  // Restore scroll position
  function restoreScrollPosition() {
    const sidebar = document.querySelector('#left-sidebar');
    if (!sidebar) return;

    const savedScrollTop = sessionStorage.getItem('sidebarScrollTop');
    if (savedScrollTop !== null) {
      sidebar.scrollTop = parseInt(savedScrollTop, 10);
    }
  }

  // Run BEFORE Alpine.js initializes to prevent jitter
  preExpandCurrentSections();
  restoreExpandedState();

  // Restore scroll position immediately
  restoreScrollPosition();

  // Save state on navigation
  document.addEventListener('click', (e) => {
    if (e.target.matches('a[href*=".html"]')) {
      const href = e.target.getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('mailto:')) {
        saveExpandedState();
      }
    }
  });

})();
