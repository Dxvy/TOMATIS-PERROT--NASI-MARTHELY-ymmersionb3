const purchase = document.querySelector('.purchase');
const facturation = document.querySelector('.facturation-address');
document.addEventListener('DOMContentLoaded', () => {
    console.log('index.js loaded');
    purchase.addEventListener('click', () => {
      facturation.style.display = 'flex';
    });
});