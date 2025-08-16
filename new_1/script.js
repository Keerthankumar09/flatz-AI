document.addEventListener("DOMContentLoaded", () => {
    const feedContainer = document.getElementById("feed-container");

    fetch("/api/feed") // Change to your actual feed API route
        .then(res => res.json())
        .then(data => {
            feedContainer.innerHTML = "";
            data.forEach(item => {
                const card = document.createElement("div");
                card.className = "col-md-4 mb-3";
                card.innerHTML = `
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${item.title}</h5>
                            <p class="card-text">${item.description}</p>
                        </div>
                    </div>
                `;
                feedContainer.appendChild(card);
            });
        })
        .catch(err => {
            feedContainer.innerHTML = `<div class="alert alert-danger">Error loading feed</div>`;
            console.error(err);
        });
});
