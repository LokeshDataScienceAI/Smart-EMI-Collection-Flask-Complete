document.addEventListener("DOMContentLoaded", function () {

    const scoreInput =
        document.getElementById("customer_score");

    const badge =
        document.getElementById("cibil-badge");

    if (!scoreInput || !badge) {
        return;
    }


    function updateCibilCategory() {

        const score =
            Number(scoreInput.value || 650);

        badge.classList.remove(
            "high",
            "medium",
            "low"
        );

        if (score <= 500) {

            badge.textContent =
                "CIBIL Category: High Risk";

            badge.classList.add("high");

        } else if (score <= 650) {

            badge.textContent =
                "CIBIL Category: Medium Risk";

            badge.classList.add("medium");

        } else {

            badge.textContent =
                "CIBIL Category: Low Risk";

            badge.classList.add("low");
        }
    }


    scoreInput.addEventListener(
        "input",
        updateCibilCategory
    );

    updateCibilCategory();

});
