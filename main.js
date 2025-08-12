document.addEventListener('DOMContentLoaded', function() {
    const newsletterList = document.querySelector('.newsletter-list');
    
    // Dodaj timestamp, aby uniknąć cachowania JSON
    const timestamp = new Date().getTime();
    
    // Pobierz dane z pliku JSON
    fetch(`js/newsletters.json?t=${timestamp}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Nie udało się pobrać listy newsletterów');
            }
            return response.json();
        })
        .then(data => {
            // Wyczyść listę
            newsletterList.innerHTML = '';
            
            // Sprawdź, czy mamy jakieś newslettery
            if (data.length === 0) {
                const li = document.createElement('li');
                li.textContent = 'Brak dostępnych newsletterów';
                newsletterList.appendChild(li);
                return;
            }
            
            // Dodaj każdy newsletter do listy
            data.forEach(newsletter => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = `pdfs/${newsletter.file}`;
                a.className = 'pdf-link';
                a.textContent = newsletter.title;
                
                li.appendChild(a);
                newsletterList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Błąd:', error);
            newsletterList.innerHTML = `<li>Błąd podczas wczytywania newsletterów: ${error.message}</li>`;
        });
});