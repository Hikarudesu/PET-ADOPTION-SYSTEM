document.addEventListener('DOMContentLoaded', function() {
    initMenu();
    initAlerts();
    initSearch();
    initDelete();
});

// Initialize menu toggle
function initMenu() {
    var hamburger = document.getElementById('hamburger');
    var navMenu = document.getElementById('navMenu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
}

// Initialize alert close buttons
function initAlerts() {
    var buttons = document.querySelectorAll('.close-alert');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
}

// Initialize search functionality
function initSearch() {
    var searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        var query = e.target.value.trim();
        if (query.length > 2) {
            searchPets(query);
        }
    });
}

// Search for pets via AJAX
function searchPets(query) {
    var url = '/pets/search/?q=' + encodeURIComponent(query);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            try {
                var data = JSON.parse(xhr.responseText);
                displayResults(data.pets);
            } catch(e) {
                console.log('Error parsing response');
            }
        }
    };
    
    xhr.onerror = function() {
        console.log('Search request failed');
    };
    
    xhr.send();
}

// Display search results
function displayResults(pets) {
    var grid = document.querySelector('.pets-grid');
    if (!grid) return;
    
    if (pets.length === 0) {
        grid.innerHTML = '<p>No pets found</p>';
        return;
    }
    
    var html = '';
    for (var i = 0; i < pets.length; i++) {
        var pet = pets[i];
        var image = pet.image ? '<img src="' + pet.image + '" class="pet-image">' : '<div class="pet-image">No image</div>';
        
        html += '<div class="pet-card">' +
                image +
                '<div class="pet-info">' +
                '<h3>' + pet.name + '</h3>' +
                '<p>' + pet.breed + '</p>' +
                '<a href="/pets/' + pet.id + '/" class="btn">View</a>' +
                '</div>' +
                '</div>';
    }
    
    grid.innerHTML = html;
}

// Initialize delete confirmation
function initDelete() {
    var deleteLinks = document.querySelectorAll('a[href*="/delete/"]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var confirmed = confirm('Are you sure?');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
}
