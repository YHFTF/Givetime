function showPopup(message, duration = 3000) {
  const popup = document.getElementById("popupMessage");
  if (!popup) return;
  popup.textContent = message;
  popup.classList.add("show");

  setTimeout(() => {
    popup.classList.remove("show");
    setTimeout(() => {
      popup.style.display = "none";
    }, 500); // transition 끝난 후 hide
  }, duration);

  popup.style.display = "block";
}

document.addEventListener("DOMContentLoaded", () => {
  const msg = sessionStorage.getItem("popupMessage");
  if (msg) {
    showPopup(msg, 3000);
    sessionStorage.removeItem("popupMessage");
  }
});
