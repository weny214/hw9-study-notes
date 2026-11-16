const search = document.querySelector("#search");
const filters = [...document.querySelectorAll("[data-filter]")];
const cards = [...document.querySelectorAll(".card")];
let category = "全部";
function filterNotes() {
  const query = search.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const card of cards) {
    const visible =
      (category === "全部" || card.dataset.category === category) &&
      card.textContent.toLocaleLowerCase().includes(query);
    card.hidden = !visible;
    if (visible) count++;
  }
  document.querySelector("#empty").hidden = count !== 0;
  document.querySelector("#count").textContent = `顯示 ${count} 篇筆記`;
}
search.addEventListener("input", filterNotes);
for (const button of filters)
  button.addEventListener("click", () => {
    category = button.dataset.filter;
    for (const item of filters) item.setAttribute("aria-pressed", String(item === button));
    filterNotes();
  });
