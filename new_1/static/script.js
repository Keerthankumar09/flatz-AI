(function () {
  const grid = document.getElementById("feed-grid");
  const loadBtn = document.getElementById("load-more");
  if (!grid) return;

  let page = 1;
  const pageSize = 8;

  async function load() {
    try {
      const res = await fetch(`/api/feed?page=${page}&page_size=${pageSize}`);
      if (!res.ok) throw new Error("Failed to load feed");
      const data = await res.json();
      render(data.items);
      if (!data.has_more) {
        loadBtn.style.display = "none";
      } else {
        loadBtn.style.display = "inline-block";
      }
      page += 1;
    } catch (e) {
      console.error(e);
    }
  }

  function render(items) {
    items.forEach(item => {
      const el = document.createElement("article");
      el.className = "card";
      el.innerHTML = `
        <img src="${item.image}" alt="${item.title}">
        <div class="card-body">
          <h4>${item.title}</h4>
          <p>${item.text}</p>
          <div class="cta">
            <a class="btn ghost" href="${item.url}">${item.cta}</a>
          </div>
        </div>
      `;
      grid.appendChild(el);
    });
  }

  load(); // initial
  loadBtn?.addEventListener("click", load);
})();
