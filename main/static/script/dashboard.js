function modalSetup() {
    // Modal setup for adding transactions    
    const modal = document.getElementById("transactionModal");
    const openBtn = document.getElementById("addTransactionBtn");
    const closeBtn = document.querySelector(".close-button");
    const cancelBtn = document.querySelector(".btn-cancel");

    const openModal = () => { modal.style.display = "block"; };
    const closeModal = () => { modal.style.display = "none"; };

    openBtn.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);
    cancelBtn.addEventListener("click", closeModal);

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeModal();
        }
    })
}