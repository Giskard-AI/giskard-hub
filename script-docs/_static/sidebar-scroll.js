/**
 * Simple Sidebar Scroll to Current Item
 * Scrolls to the currently selected item in the sidebar on page load
 */
(function() {
  'use strict';
  
  function scrollToCurrentItem() {
    // Find the sidebar
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
  
  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scrollToCurrentItem);
  } else {
    scrollToCurrentItem();
  }
  
})();