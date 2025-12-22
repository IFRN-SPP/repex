document.addEventListener('DOMContentLoaded', function() {
  
  const SCROLL_AMOUNT = 300; 
  const HIDE_CLASS = 'd-none'; 
  
  const carousels = document.querySelectorAll('.carousel-shell');

  function checkScrollPosition(track, prevBtn, nextBtn) {
    const maxScroll = track.scrollWidth - track.clientWidth;
    
    if (track.scrollLeft <= 5) { 
      prevBtn.classList.add(HIDE_CLASS); 
    } else {
      prevBtn.classList.remove(HIDE_CLASS); 
    }

    if (track.scrollLeft >= maxScroll - 5) {  
      nextBtn.classList.add(HIDE_CLASS); 
    } else {
      nextBtn.classList.remove(HIDE_CLASS);  
    }
  }

  carousels.forEach(carousel => {
    const track = carousel.querySelector('.carousel-track');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');

    if (!track || !prevBtn || !nextBtn) {
      console.warn('Carrossel ignorado: elementos de navegação não encontrados.');
      return;
    }
    
    track.style.scrollBehavior = 'smooth'; 

    checkScrollPosition(track, prevBtn, nextBtn);

    track.addEventListener('scroll', () => {
      checkScrollPosition(track, prevBtn, nextBtn);
    });

    prevBtn.addEventListener('click', () => {
      track.scrollLeft -= SCROLL_AMOUNT;
    });

    nextBtn.addEventListener('click', () => {
      track.scrollLeft += SCROLL_AMOUNT;
    });
  });
});