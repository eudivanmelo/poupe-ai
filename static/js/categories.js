const handleSubmitForm = (form) => {
    form.preventDefault();

    const formData = new FormData(form.target);
    const activeTab = document.querySelector("#categoryTabs .nav-link.active").id;
    const type = activeTab.includes("despesas") ? "expense" : "income";

    formData.append("type", type);
    localStorage.setItem("activeTab", activeTab);

    fetch(form.target.action, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(true);
            } else {
                alert("Erro ao criar categoria: " + JSON.stringify(data.errors));
            }
        })
        .catch(error => console.error("Erro:", error));
};

const CategoryManager = {
    init() {
        this.bindEvents();
        this.restoreActiveTab();
    },

    bindEvents() {
        $(document).ready(() => {
            this.handleDeleteCategory();
            this.handleColorSelection();
            this.handleTabChange();
            this.handleAddCategoryModal();
            this.handleEditCategoryModal();
            this.handleDropdownAnimation();
            this.handleAddCategory();
        });
    },

    handleDeleteCategory() {
        $(document).on("click", '[id^="delete-category-"]', function () {
            const url = $(this).data("url");
            const itemName = $(this).data("item-name");
            const activeTab = document.querySelector("#categoryTabs .nav-link.active").id;

            localStorage.setItem("activeTab", activeTab);

            swal({
                title: "Excluir essa categoria?",
                text: `Ao apagar a categoria "${itemName}", todas as transações vinculadas a ela também serão apagadas. Esta ação não pode ser desfeita!`,
                buttons: {
                    cancel: { text: "Cancelar", visible: true, className: "btn btn-secondary" },
                    confirm: { text: "Excluir", className: "btn btn-primary" },
                },
            }).then(shouldDelete => {
                if (shouldDelete && url) {
                    fetch(url, {
                        method: "DELETE",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                    })
                        .then(response => response.json())
                        .then(data => {
                            swal({
                                title: data.success ? "Deletada!" : "Erro!",
                                text: data.message,
                                icon: data.success ? "success" : "error",
                                buttons: { confirm: { className: data.success ? "btn btn-success" : "btn btn-danger" } },
                            }).then(() => {
                                if (data.success) location.reload(true);
                            });
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });
        });
    },

    handleColorSelection() {
        $("#colorInput, #colorInputEdit").on("input", function () {
            const color = $(this).val();
            $("#colorPicker, #colorPickerEdit").css("background-color", color);
        });

        $("#colorPicker, #colorPickerEdit").click(function () {
            $(`#${this.id === "colorPicker" ? "colorInput" : "colorInputEdit"}`).click();
        });
    },

    handleTabChange() {
        $("#categoryTabs .nav-link").on("shown.bs.tab", function (event) {
            $("#total-value").text(`R$ ${$(event.target).data("total")}`);
            $("#total-categorias").text($(event.target).data("total-cat"));
            console.log("Categoria selecionada:", $(event.target).text());
        });
    },

    restoreActiveTab() {
        const activeTab = localStorage.getItem("activeTab");
        if (activeTab) {
            const tabElement = document.querySelector(`#${activeTab}`);
            if (tabElement) {
                new bootstrap.Tab(tabElement).show();
                $("#total-value").text(`R$ ${$(tabElement).data("total")}`);
                $("#total-categorias").text($(tabElement).data("total-cat"));
            }
            localStorage.removeItem("activeTab");
        } else {
            const defaultTab = document.querySelector("#categoryTabs .nav-link.active");
            if (defaultTab) {
                $("#total-value").text(`R$ ${$(defaultTab).data("total")}`);
                $("#total-categorias").text($(defaultTab).data("total-cat"));
            }
        }
    },

    handleAddCategoryModal() {
        $("#add-category").click(() => $("#addCategoryModal").modal("show"));
    },

    handleEditCategoryModal() {
        $(document).on("click", '[id^="edit-category-"]', function () {
            const url = $(this).data("url");
            const modal = $("#editCategoryModal");
            const activeTab = document.querySelector("#categoryTabs .nav-link.active").id;

            localStorage.setItem("activeTab", activeTab);

            fetch(url, { method: "GET", headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        modal.find("#nameInput").val(data.category.name);
                        modal.find("#colorInputEdit").val(data.category.color);
                        modal.find("#colorPickerEdit").css("background-color", data.category.color);
                        modal.find("#editCategoryForm").attr("action", url);
                        modal.modal("show");
                    } else {
                        alert("Erro ao carregar os dados da categoria");
                    }
                })
                .catch(error => console.error("Erro:", error));
        });

        const editForm = document.getElementById("editCategoryForm");
        if (editForm) {
            editForm.addEventListener("submit", event => {
                event.preventDefault();
                const activeTab = document.querySelector("#categoryTabs .nav-link.active").id;
                localStorage.setItem("activeTab", activeTab);

                fetch(event.target.action, {
                    method: "POST",
                    body: new FormData(event.target),
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            location.reload(true);
                        } else {
                            alert("Erro ao editar categoria: " + JSON.stringify(data.errors));
                        }
                    })
                    .catch(error => console.error("Erro:", error));
            });
        }
    },

    handleDropdownAnimation() {
        document.querySelectorAll(".dropdown").forEach(dropdown => {
            dropdown.addEventListener("show.bs.dropdown", () => dropdown.closest(".category-card").classList.add("dropdown-open"));
            dropdown.addEventListener("hide.bs.dropdown", () => dropdown.closest(".category-card").classList.remove("dropdown-open"));
        });
    },

    handleAddCategory() {
        document.getElementById("addCategoryForm")?.addEventListener("submit", handleSubmitForm);
    },
};

CategoryManager.init();